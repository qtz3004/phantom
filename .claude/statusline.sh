#!/usr/bin/env python3
import sys, json, subprocess

data = json.loads(sys.stdin.read())

cwd = data.get("cwd") or data.get("workspace", {}).get("current_dir") or None

try:
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        stderr=subprocess.DEVNULL,
        cwd=cwd,
        env={**__import__("os").environ, "GIT_OPTIONAL_LOCKS": "0"}
    ).decode().strip()
except Exception:
    branch = "?"

ctx_pct = data.get("context_window", {}).get("used_percentage")
rate = data.get("rate_limits", {})
five_h = rate.get("five_hour", {}).get("used_percentage")
seven_d = rate.get("seven_day", {}).get("used_percentage")

def color(pct):
    if pct >= 80: return "\033[91m"
    if pct >= 50: return "\033[93m"
    return "\033[90m"

model = data.get("model", {}).get("display_name", "")

parts = [f"\033[36m{model}\033[0m", f"\033[33m{branch}\033[0m"]
if ctx_pct is not None:
    parts.append(f"ctx:{color(ctx_pct)}{ctx_pct:.0f}%\033[0m")
if five_h is not None:
    parts.append(f"5h:{color(five_h)}{five_h:.0f}%\033[0m")
if seven_d is not None:
    parts.append(f"7d:{color(seven_d)}{seven_d:.0f}%\033[0m")

print(" | ".join(parts), end="")
