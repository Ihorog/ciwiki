import json, pathlib, re

def test_index_shape():
    p = pathlib.Path("docs/assets/knowledge.index.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, list) and data
    for item in data:
        assert set(item).issuperset({"path","title","tags","updated"})
        assert item["path"].endswith(".md")
        assert isinstance(item["title"], str) and item["title"]
        assert isinstance(item["tags"], list)
        assert item["updated"] is None or re.match(r"^\d{4}-\d{2}-\d{2}$", str(item["updated"]))
