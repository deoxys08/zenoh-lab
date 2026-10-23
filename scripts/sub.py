#!/usr/bin/env python3
"""Subscribe to a key expression and print every sample received."""
import argparse
import time

import zenoh

from zcommon import add_common_args, build_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", default="lab/**", help="Key expression to subscribe to")
    add_common_args(parser)
    args = parser.parse_args()

    zenoh.init_log_from_env_or("error")
    conf = build_config(args)

    def on_sample(sample: zenoh.Sample) -> None:
        print(f"[recv] {sample.key_expr} -> {sample.payload.to_string()}", flush=True)

    with zenoh.open(conf) as session:
        sub = session.declare_subscriber(args.key, on_sample)
        print(f"subscriber ready: mode={args.mode} key={args.key} (Ctrl+C to stop)", flush=True)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        sub.undeclare()


if __name__ == "__main__":
    main()
