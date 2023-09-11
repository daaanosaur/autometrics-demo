# Utilities for getting git metdata
import subprocess

def get_git_commit():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.STDOUT).decode("utf-8").strip()
        return commit
    except:
        return None

def get_git_branch():
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.STDOUT).decode("utf-8").strip()
        return branch
    except:
        return None

