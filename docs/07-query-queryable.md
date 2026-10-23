# Step 07 - Query / Queryable

## Goal
Request data on demand instead of streaming it: Pi-1 (and later Pi-2) answer
queries with their current CPU temperature; the laptop asks.
All nodes run as clients through the router on Pi-2.

## Concepts
- A **queryable** registers a key expression it can answer for
  (`lab/pi1/temperature`) and computes a reply each time a query arrives.
- A **get** sends a query for a selector (`lab/*/temperature`) and receives
  zero or more replies, followed by an explicit end of the query.

## Commands
Pi-2:   zenohd -l tcp/<PI2_LAN_IP>:7447
Pi-1:   python scripts/queryable.py --mode client --connect tcp/<PI2_LAN_IP>:7447 --name pi1 --key lab/pi1/temperature
Pi-2:   python scripts/queryable.py --mode client --connect tcp/<PI2_LAN_IP>:7447 --name pi2 --key lab/pi2/temperature
Laptop: python scripts/get.py --mode client --connect tcp/<PI2_LAN_IP>:7447

## Results

| Experiment | Queryables     | Replies | Total time |
|------------|----------------|---------|------------|
| A          | Pi-1           | 1       | 13-16 ms   |
| B          | Pi-1 and Pi-2  | 2       | ~15 ms     |
| C          | none           | 0       | ~7 ms      |

## Observations
- Values are computed at query time (temperature changed between queries);
  nothing is stored in between.
- One query with a wildcard reached every matching queryable and collected all replies.
- The query finished as soon as all matching queryables had replied; it did not
  wait for the 3 s timeout.
- With no queryable, the query returned immediately: the router knows from the
  declarations which queryables exist, so there was nothing to wait for.
- The round trip (laptop -> router -> Pi-1 -> router -> laptop) crosses Wi-Fi
  four times, which explains most of the ~15 ms.

## Pub/sub vs query
- Pub/sub: continuous stream; late joiners miss earlier data; no end marker.
- Query: on-demand; fresh value at the moment of asking; explicit completion.
- A Zenoh storage is essentially a subscriber that records data plus a queryable
  that answers from what it recorded.
