import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app


def setup_temp_file(tmp_path, monkeypatch):
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr(app, "DATA_FILE", data_file)
    return data_file


def test_add_and_list_tasks(tmp_path, monkeypatch, capsys):
    setup_temp_file(tmp_path, monkeypatch)

    app.add_task("学习 Git")
    app.list_tasks()

    out = capsys.readouterr().out
    assert "已添加任务 #1: 学习 Git" in out
    assert "1. ⬜ 学习 Git" in out


def test_mark_done_and_delete(tmp_path, monkeypatch, capsys):
    data_file = setup_temp_file(tmp_path, monkeypatch)

    app.add_task("任务A")
    app.mark_done(1)
    app.list_tasks()
    out = capsys.readouterr().out
    assert "任务 #1 已完成" in out
    assert "1. ✅ 任务A" in out

    app.delete_task(1)
    assert data_file.exists()
    assert app.load_tasks() == []


def test_not_found_messages(tmp_path, monkeypatch, capsys):
    setup_temp_file(tmp_path, monkeypatch)

    app.mark_done(99)
    app.delete_task(99)

    out = capsys.readouterr().out
    assert "未找到任务 #99" in out
