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
