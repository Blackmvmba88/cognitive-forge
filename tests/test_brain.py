from blackmamba_cognitive.brain import build_graph


def test_brain_builds_deterministic_graph(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "a.py").write_text("import json\nfrom pathlib import Path\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    first = build_graph(tmp_path)
    second = build_graph(tmp_path)

    assert first == second
    assert first["graph_sha256"] == second["graph_sha256"]
    assert any(edge["relation"] == "contains" for edge in first["edges"])
    assert any(edge["relation"] == "imports" for edge in first["edges"])
