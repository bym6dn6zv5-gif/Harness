"""第 8 天：给固定工具进程设置超时，区分错误与程序崩溃。"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time


def valid_seconds(value: object, *, allow_zero: bool, maximum: float) -> bool:
    return (type(value) in (int, float) and value <= maximum
            and (value >= 0 if allow_zero else value > 0) and math.isfinite(value))


def run_timed_probe(delay_seconds: float, timeout_seconds: float) -> dict:
    """仅启动本教材的固定 worker；不接受命令、代码或任意脚本路径。"""
    if not valid_seconds(delay_seconds, allow_zero=True, maximum=10) or not valid_seconds(timeout_seconds, allow_zero=False, maximum=30):
        return {"ok": False, "error": {
            "code": "invalid_arguments", "message": "delay 应在 [0, 10]，timeout 应在 (0, 30]，单位为秒。",
        }}
    started = time.monotonic()

    def failure(code: str, message: str) -> dict:
        return {"ok": False, "error": {"code": code, "message": message},
                "elapsed_ms": round((time.monotonic() - started) * 1000, 2)}

    # 不把宿主 API 密钥等环境变量传给实验进程；仍然不构成安全沙箱。
    child_env = {key: value for key, value in os.environ.items()
                 if key.upper() in {"SYSTEMROOT", "WINDIR", "TEMP", "TMP"}}
    worker = Path(__file__).with_name("timeout_worker.py").resolve()
    try:
        completed = subprocess.run(
            [sys.executable, "-I", "-X", "utf8", str(worker), "--delay", str(delay_seconds)],
            shell=False, cwd=worker.parent, env=child_env, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, encoding="utf-8", timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        # run() 已终止并等待这个直接子进程，然后才抛出 TimeoutExpired。
        return failure("tool_timeout", "固定实验进程超时，已终止并等待退出。")
    except OSError:
        return failure("tool_failed", "固定实验进程无法启动。")
    if completed.returncode != 0:
        return failure("tool_failed", f"固定实验进程退出码：{completed.returncode}")
    try:
        result = json.loads(completed.stdout)
    except (ValueError, TypeError):
        return failure("invalid_tool_result", "进程没有返回约定的 JSON。")
    if result != {"ok": True, "data": {"completed": True}}:
        return failure("invalid_tool_result", "进程返回结构与约定不符。")
    result["elapsed_ms"] = round((time.monotonic() - started) * 1000, 2)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=["normal", "timeout", "invalid"], default="normal")
    args = parser.parse_args()
    delay, timeout = {"normal": (0, 5), "timeout": (3, 0.1), "invalid": (-1, 5)}[args.scenario]
    print("[参数]", {"delay_seconds": delay, "timeout_seconds": timeout})
    print("[工具结果]", json.dumps(run_timed_probe(delay, timeout), ensure_ascii=False))


if __name__ == "__main__":
    main()
