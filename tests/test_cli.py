from typer.testing import CliRunner
from gitradar.cli import app

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "GitRadar CLI Version" in result.output


def test_cli_config_show():
    result = runner.invoke(app, ["config", "--show"])
    assert result.exit_code == 0
    assert "Current GitRadar Configuration" in result.output
    assert "OPENAI_API_KEY" in result.output
    assert "OPENAI_BASE_URL" in result.output


def test_cli_config_set_openai_options(tmp_path, monkeypatch):
    test_config_file = tmp_path / "config.env"
    monkeypatch.setattr("gitradar.config.CONFIG_FILE", test_config_file)
    monkeypatch.setattr("gitradar.config.CONFIG_DIR", tmp_path)

    result = runner.invoke(app, ["config", "--openai-api-key", "sk-test-12345", "--base-url", "https://api.openai.com/v1"])
    assert result.exit_code == 0
    assert "OPENAI_API_KEY successfully saved" in result.output
    assert "OPENAI_BASE_URL saved" in result.output
