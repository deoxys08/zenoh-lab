#!/usr/bin/env python3
"""Answer queries on a key expression with this machine's current CPU temperature."""
import argparse
import time
from pathlib import Path

import zenoh

from zcommon import add_common_args, build_config

THERMAL_ZONE = Path("/sys/class/thermal/thermal_zone0/temp")


def read_cpu_temp_c() -> float | None:
    try:
        return int(THERMAL_ZONE.read_text().strip()) / 1000.0
    except (OSError, ValueError):
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", default="lab/pi1/temperature", help="Key expression to answer for")
    parser.add_argument("--name", default="pi1", help="Label included in the reply")
    add_common_args(parser)
    args = parser.parse_args()

    zenoh.init_log_from_env_or("error")
    conf = build_config(args)

    def on_query(query: zenoh.Query) -> None:
        temp = read_cpu_temp_c()
        value = f"{args.name}: {temp:.1f} C" if temp is not None else f"{args.name}: n/a"
        print(f"[query] {query.selector} -> reply '{value}'", flush=True)
        query.reply(args.key, value)

    with zenoh.open(conf) as session:
        queryable = session.declare_queryable(args.key, on_query)
        print(f"queryable ready: mode={args.mode} key={args.key} (Ctrl+C to stop)", flush=True)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        queryable.undeclare()


if __name__ == "__main__":
    main()
