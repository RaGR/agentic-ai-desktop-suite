
import subprocess
from src.policy.safety import check_ps_allowlist, check_bash_allowlist
from src.common.logging import audit

def run(shell: str, cmd: str, cwd: str, mode: str, allow_ps, allow_bash):
    if shell=="powershell":
        if mode!="allowlist" or not check_ps_allowlist(cmd, allow_ps):
            res={"ok":False,"error":"denied"}
            audit("shell.ps", {"cmd":cmd,"cwd":cwd}, res); return res
        ps = ["pwsh","-NoLogo","-NoProfile","-Command", cmd]
        cp = subprocess.run(ps, cwd=cwd or None, capture_output=True, text=True)
    else:
        if mode!="allowlist" or not check_bash_allowlist(cmd, allow_bash):
            res={"ok":False,"error":"denied"}
            audit("shell.bash", {"cmd":cmd,"cwd":cwd}, res); return res
        cp = subprocess.run(cmd.split(), cwd=cwd or None, capture_output=True, text=True)
    res={"ok":cp.returncode==0,"stdout":cp.stdout[-8000:],"stderr":cp.stderr[-2000:],"exit_code":cp.returncode}
    audit(f"shell.{shell}", {"cmd":cmd,"cwd":cwd}, {"ok":res['ok'],"exit":cp.returncode}); return res
