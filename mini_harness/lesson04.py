"""第 4 天：把已经完成的运行导出为 JSONL 消息快照。"""

import argparse
import json
from pathlib import Path
from uuid import uuid4

from mini_harness.lesson03 import ReadThenCountModel, RepeatingModel, run_agent


def save_trace(result: dict, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{uuid4().hex}.jsonl"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        for sequence, message in enumerate(result["messages"], start=1):
            record = {"type": "message", "sequence": sequence, "message": message}
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        summary = {key: result[key] for key in ("status", "model_calls", "tool_calls")}
        stream.write(json.dumps({"type": "summary", **summary}, ensure_ascii=False) + "\n")
    return path


def load_trace(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=["normal", "repeat"], default="normal")
    parser.add_argument("--show-trace", action="store_true")
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    model = ReadThenCountModel() if args.scenario == "normal" else RepeatingModel()
    result = run_agent(model, project / "lessons/six_day_pack/workspace", max_steps=3)
    path = save_trace(result, project / ".harness/day04")
    print("[记录文件]", path)
    print("[停止状态]", result["status"])
    records = load_trace(path)
    print("[记录条数]", len(records))
    if args.show_trace:
        for record in records:
            print(json.dumps(record, ensure_ascii=False))


if __name__ == "__main__":
    main()
