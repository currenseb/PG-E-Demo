# 12 kV Substation Monitoring Demo

Docker-based demo of a four-feeder, 12 kV distribution substation. A Python simulator writes artificial three-phase measurement data to ClickHouse; Grafana displays historical trends; ngrok provides an external HTTPS link.

## Stack

```text
Simulator → ClickHouse → Grafana → ngrok public URL
```

| Component        | Role                                                       |
| ---------------- | ---------------------------------------------------------- |
| Python simulator | Creates a record for each of four feeders every 5 seconds. |
| ClickHouse       | Stores timestamped measurement data.                       |
| Grafana          | Displays live and historical trends.                       |
| Docker Compose   | Runs the complete Linux-hosted stack.                      |
| ngrok            | Tunnels the Grafana UI for external review.                |

## Simulated system

| Feeder | Load        | Baseline current | Approximate MW |
| ------ | ----------- | ---------------: | -------------: |
| 1      | Residential |            100 A |         2.0 MW |
| 2      | Commercial  |            150 A |         3.0 MW |
| 3      | Industrial  |            200 A |         4.0 MW |
| 4      | Mixed-use   |            125 A |         2.5 MW |

Each record contains UTC timestamp, feeder ID, phase A/B/C voltage, phase A/B/C current, MW, and MVAR. Values include small random variation to produce realistic trends and minor phase imbalance.

```text
MW   = √3 × kV × A × power factor / 1000
MVAR = √3 × kV × A × √(1 - power factor²) / 1000
```

The model uses nominal 12 kV line-to-line voltage and 0.95 inductive power factor.

## Dashboard

Grafana dashboard: **12 kV Distribution Substation Monitoring**

- Real power (MW) by feeder
- Reactive power (MVAR) by feeder
- Three-phase feeder currents (A/B/C)
- Total substation real power

Voltage A/B/C is also stored in ClickHouse and available for a future panel/query.

## Public dashboard

Open the dashboard at:

```text
https://tux-flask-candied.ngrok-free.dev
```

Login details are provided separately.

## Security/networking

- ClickHouse is private; it has no published host port.
- Grafana is bound to `127.0.0.1:3000`.
- Services communicate on Docker's private `monitoring` bridge network.
