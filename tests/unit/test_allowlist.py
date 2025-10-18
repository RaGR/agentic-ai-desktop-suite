
from src.policy.safety import check_ps_allowlist, check_bash_allowlist
def test_ps_allow():
    allow=["Get-Content","git status"]
    assert check_ps_allowlist("Get-Content foo.txt", allow)
    assert not check_ps_allowlist("Remove-Item * -Recurse", allow)
def test_bash_allow():
    allow=["ls","cat"]
    assert check_bash_allowlist("ls -la", allow)
    assert not check_bash_allowlist("rm -rf /", allow)
