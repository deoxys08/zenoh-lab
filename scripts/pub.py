#!/usr/bin/env python3
"""Publish a counter message on a key expression at a fixed interval."""
import argparse
import time

import zenoh

from zcommon import add_common_args, build_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", default="lab/laptop/counter", help="Key expression to publish on")
    parser.add_argument("--name", default="laptop", help="Sender label included in the payload")
    parser.add_argument("--interval", type=float, default=1.0, help="Seconds between messages")
    add_common_args(parser)
    args = parser.parse_args()

    zenoh.init_log_from_env_or("error")
    conf = build_config(args)

    with zenoh.open(conf) as session:
        pub = session.declare_publisher(args.key)
        print(f"publisher ready: mode={args.mode} key={args.key} (Ctrl+C to stop)", flush=True)
        i = 0
        try:
            while True:
                i += 1
                msg = f"{args.name} #{i}"
                pub.put(msg)
                print(f"[sent] {args.key} -> {msg}", flush=True)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            pass
        pub.undeclare()


if __name__ == "__main__":
    main()
