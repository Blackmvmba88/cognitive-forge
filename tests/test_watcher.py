import json

from blackmamba_cognitive.watcher import main, scan


def test_scan_is_deterministic_and_ignores_git(tmp_path):
    (tmp_path / "b.txt").write_text("beta", encoding="utf-8")
    (tmp_path / "a.py").write_text("print('alpha')\n", encoding="utf-8")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "noise").write_text("ignore me", encoding="utf-8")

    first = scan(tmp_path)
    second = scan(tmp_path)

    assert first == second
    assert [item["path"] for item in first["files"]] == ["a.py", "b.txt"]
    assert first["file_count"] == 2
    assert first["extensions"] == {".py": 1, ".txt": 1}


def test_snapshot_hash_changes_when_observed_content_changes(tmp_path):
    target = tmp_path / "state.txt"
    target.write_text("state-a", encoding="utf-8")
    before = scan(tmp_path)["snapshot_sha256"]

    target.write_text("state-b", encoding="utf-8")
    after = scan(tmp_path)["snapshot_sha256"]

    assert before != after


def test_cli_emits_valid_json(tmp_path, capsys):
    (tmp_path / "evidence.txt").write_text("signal", encoding="utf-8")

    exit_code = main(["scan", str(tmp_path)])
    captured = capsys.readouterr()

    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["file_count"] == 1
    assert payload["files"][0]["path"] == "evidence.txt"
