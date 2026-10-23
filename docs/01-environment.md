# Step 01 - Environment and network check

## Goal
Inventory the three machines and verify basic reachability before installing Zenoh.
Zenoh peers can discover each other via UDP multicast scouting, so all nodes
should be on the same local network.

## Machines

| Role   | OS                   | Arch    | Python |
|--------|----------------------|---------|--------|
| Laptop | macOS                | arm64   | 3.14   |
| Pi-1   | Debian 12 (bookworm) | aarch64 | 3.11   |
| Pi-2   | Debian 13 (trixie)   | aarch64 | 3.13   |

All three machines are on the same local network. Actual IP addresses are kept
in the git-ignored `hosts.env` (see `configs/hosts.env.example`).

## Reachability
- Laptop -> Pi-1: OK
- Laptop -> Pi-2: OK
- Pi-1 -> Pi-2: OK

## Design decision: laptop connects outbound only
Throughout this lab the laptop always initiates connections to the Pis;
the Pis never connect to the laptop. This mirrors a common edge/automotive
pattern where devices behind restrictive networks only open outbound connections.

## Notes
Nodes may have multiple network interfaces (VPNs, container bridges).
Zenoh advertises locators on all of them by default, which can affect
discovery and connection attempts.
