# Step 04 - Peer discovery (multicast scouting)

## Goal
Let Pi-1 and Pi-2 find each other without any configured endpoints, and observe
which network path the automatic connection uses.

## How scouting works
In peer mode each node announces itself on the local network via UDP multicast
("I am here, reachable at these addresses"). Peers that hear the announcement
connect to one of the advertised addresses automatically.

## Experiment A - fully default configuration
Pi-2: python scripts/sub.py
Pi-1: python scripts/pub.py --name pi1 --key lab/pi1/counter

Result: all messages delivered with no endpoints configured.
`ss -tnp` on Pi-1 showed the TCP link was established over the Tailscale IPv6
addresses (fd7a:...), not over the LAN, on a random port chosen by Pi-2.

Why: with no `listen` endpoint, a peer listens on all interfaces and advertises
all of them (LAN, VPN, ...). The connecting peer used the first address that worked.

## Experiment B - advertise the LAN address only
Pi-2: python scripts/sub.py --listen tcp/<PI2_LAN_IP>:7447
Pi-1: python scripts/pub.py --name pi1 --key lab/pi1/counter --listen tcp/<PI1_LAN_IP>:7447

Result: still discovered automatically (no `--connect`), and the link now used
the LAN addresses on port 7447.

## Takeaways: peer mode
- All peers are equal; once linked, data flows both ways regardless of who connected.
- Discovery is either explicit (`connect`) or automatic (multicast, same LAN only).
- Peers connect directly to each other: lowest latency, no single point of failure.
- The number of links grows quickly (full mesh), and multicast does not cross networks.
- On multi-homed hosts, set `listen` explicitly to control which path is advertised.

## Why the VPN address was chosen (source code)
With no `listen` endpoint a peer listens on `tcp/[::]:0`. The advertised addresses
are then ordered by `get_ipv6_ipaddrs` in `zenoh-util` (`src/net/mod.rs`):
1. non-link-local IPv6 (here: the VPN's ULA address)
2. public IPv4 (here: the VPN's 100.x address, not considered private)
3. link-local IPv6
4. private IPv4 (here: the LAN address, last)

The connecting peer used the first address that worked, i.e. the VPN.
