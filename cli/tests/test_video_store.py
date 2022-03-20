from typer.testing import CliRunner

from video_store.main import app

runner = CliRunner()


def test_upload():
    result = runner.invoke(app, ["upload", "tests/data/video1.mp4"])
    assert result.exit_code == 0


def test_delete():
    result = runner.invoke(app, ["delete", "123"])
    assert result.exit_code == 0


def test_download():
    result = runner.invoke(app, ["download", "123"])
    assert result.exit_code == 0


def test_list():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    # assert "Here is something" in result.stdout
