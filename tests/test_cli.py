from typer.testing import CliRunner
from gitradar.cli import app

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "GitRadar CLI Sürümü" in result.output


def test_cli_config_show():
    result = runner.invoke(app, ["config", "--show"])
    assert result.exit_code == 0
    assert "Mevcut GitRadar Yapılandırması" in result.output
