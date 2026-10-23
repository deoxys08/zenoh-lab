#!/usr/bin/env python3
"""Send a query and print every reply received, with its latency."""
import argparse
import time

import zenoh

from zcommon import add_common_args, build_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selector", default="lab/*/temperature", help="Key expression to query")
    parser.add_argument("--timeout", type=float, default=3.0, help="Query timeout in seconds")
    add_common_args(parser)
    args = parser.parse_args()

    zenoh.init_log_from_env_or("error")
    conf = build_config(args)

    with zenoh.open(conf) as session:
        print(f"query: {args.selector} (timeout {args.timeout}s)", flush=True)
        start = time.monotonic()
        replies = session.get(args.selector, target=zenoh.QueryTarget.ALL, timeout=args.timeout)
        count = 0
        for reply in replies:
            elapsed_ms = (time.monotonic() - start) * 1000
            if reply.ok is not None:
                count += 1
                print(f"[reply] {reply.ok.key_expr} -> {reply.ok.payload.to_string()} ({elapsed_ms:.1f} ms)", flush=True)
            else:
                print(f"[error] {reply.err.payload.to_string()} ({elapsed_ms:.1f} ms)", flush=True)
        total_ms = (time.monotonic() - start) * 1000
        print(f"done: {count} replies in {total_ms:.1f} ms", flush=True)


if __name__ == "__main__":
    main()
