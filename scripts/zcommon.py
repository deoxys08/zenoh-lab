"""Shared helpers: build a Zenoh config from command-line arguments."""
import argparse
import json

import zenoh


def add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--mode", choices=["peer", "client"], default="peer",
                        help="Zenoh session mode (default: peer)")
    parser.add_argument("--connect", action="append", default=[], metavar="ENDPOINT",
                        help="Endpoint to connect to, e.g. tcp/192.168.1.10:7447 (repeatable)")
    parser.add_argument("--listen", action="append", default=[], metavar="ENDPOINT",
                        help="Endpoint to listen on, e.g. tcp/0.0.0.0:7447 (repeatable)")
    parser.add_argument("--no-listen", action="store_true",
                        help="Open no listening socket (outbound connections only)")
    return parser


def build_config(args: argparse.Namespace) -> zenoh.Config:
    conf = zenoh.Config()
    conf.insert_json5("mode", json.dumps(args.mode))
    if args.connect:
        conf.insert_json5("connect/endpoints", json.dumps(args.connect))
    if args.no_listen:
        conf.insert_json5("listen/endpoints", json.dumps([]))
    elif args.listen:
        conf.insert_json5("listen/endpoints", json.dumps(args.listen))
    return conf
