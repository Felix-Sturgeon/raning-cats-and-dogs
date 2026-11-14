import sys
from pathlib import Path

def dir_parent():
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).parent

def resource_path(*parts: str) ->Path:
    return dir_parent().joinpath(*parts)
    