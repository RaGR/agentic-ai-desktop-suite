
from src.policy.safety import normalize_path, is_in_sandboxes, deny_traversal
def test_traversal_denied():
    assert deny_traversal(r"..\evil") is True
def test_sandbox_check(tmp_path):
    s = [str(tmp_path)]
    p = tmp_path/"ok.txt"; p.write_text("x")
    assert is_in_sandboxes(str(p), s) is True
    assert is_in_sandboxes(r"C:\Windows\System32", s) is False
