import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_DIR = Path.home() / ".config" / "gitradar"
CONFIG_FILE = CONFIG_DIR / "config.env"


class Settings(BaseSettings):
    groq_api_key: Optional[str] = None
    github_token: Optional[str] = None
    default_model: str = "groq/llama-3.1-8b-instant"
    max_repos_to_analyze: int = 10

    model_config = SettingsConfigDict(
        env_file=(str(CONFIG_FILE), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


def load_settings() -> Settings:
    """Load settings from env vars or config files."""
    return Settings()


def save_setting(key: str, value: str) -> None:
    """Save a setting key-value pair to user config file (~/.config/gitradar/config.env)."""
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


settings = load_settings()
