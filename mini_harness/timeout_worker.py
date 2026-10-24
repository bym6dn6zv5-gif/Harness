"""第 8 天的固定实验进程：只等待一小段时间，再输出固定结构。"""

import argparse
import json
import math
import time


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delay", type=float, required=True)
    args = parser.parse_args()
    if not math.isfinite(args.delay) or not 0 <= args.delay <= 10:
        parser.error("delay 必须在 0 到 10 秒之间")
    time.sleep(args.delay)
    print(json.dumps({"ok": True, "data": {"completed": True}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
