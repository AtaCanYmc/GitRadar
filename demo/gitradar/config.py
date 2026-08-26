import os
from pathlib import Path
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_DIR = Path.home() / ".config" / "gitradar"
CONFIG_FILE = CONFIG_DIR / "config.env"


class Settings(BaseSettings):
    groq_api_key: Optional[str] = None
    github_token: Optional[str] = None
    default_model: str = "groq/llama-3.1-8b-instant"
    default_language: str = "English"
    max_repos_to_analyze: int = 50
    min_relevance_threshold: int = 50

    model_config = SettingsConfigDict(
        env_file=(str(CONFIG_FILE), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("max_repos_to_analyze", "min_relevance_threshold", mode="before")
    @classmethod
    def validate_int_settings(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return 50 if "min_relevance" in str(v) else 10
        try:
            return int(v)
        except (ValueError, TypeError):
            return 50

    @field_validator("groq_api_key", "github_token", "default_model", "default_language", mode="before")
    @classmethod
    def validate_empty_strings(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        return v


def load_settings() -> Settings:
    """Load settings from env vars or config files safely."""
    try:
        return Settings()
    except Exception:
        try:
            return Settings(_env_file=None)
        except Exception:
            return Settings.model_construct(
                groq_api_key=None,
                github_token=None,
                default_model="groq/llama-3.1-8b-instant",
                default_language="English",
                max_repos_to_analyze=50,
            )


def save_setting(key: str, value: str) -> None:
    """Save a setting key-value pair to user config file (~/.config/gitradar/config.env)."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        existing_lines = []
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                existing_lines = f.readlines()
                
        key_upper = key.upper()
        found = False
        new_lines = []
        
        for line in existing_lines:
            if line.strip().startswith(f"{key_upper}="):
                new_lines.append(f"{key_upper}={value}\n")
                found = True
            else:
                new_lines.append(line)
                
        if not found:
            if new_lines and not new_lines[-1].endswith("\n"):
                new_lines.append("\n")
            new_lines.append(f"{key_upper}={value}\n")
            
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    except Exception:
        pass


settings = load_settings()
