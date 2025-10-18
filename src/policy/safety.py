
import os, re, pathlib
from typing import List

_BAD = re.compile(r"[;&|><`$]")  # deny shell metas by default

def normalize_path(p: str) -> str:
    p = os.path.expandvars(p)
    p = os.path.abspath(os.path.normpath(p))
    return p

def is_in_sandboxes(p: str, sandboxes: List[str]) -> bool:
    p = pathlib.Path(normalize_path(p))
    for s in sandboxes:
        try:
            if p.resolve().is_relative_to(pathlib.Path(normalize_path(s)).resolve()):
                return True
        except AttributeError:
            try:
                p.resolve().relative_to(pathlib.Path(normalize_path(s)).resolve())
                return True
            except Exception:
                pass
    return False

def deny_traversal(p: str) -> bool:
    return (".." in pathlib.Path(p).parts)

def check_ps_allowlist(cmd: str, allow: List[str]) -> bool:
    if _BAD.search(cmd): return False
    head = cmd.strip().split()[0].lower()
    return any(head.lower() == a.lower() for a in allow)

def check_bash_allowlist(cmd: str, allow: List[str]) -> bool:
    if _BAD.search(cmd): return False
    head = cmd.strip().split()[0]
    return head in allow
