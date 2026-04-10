# Nokia-AI-ML-Automation-Demo

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-Vanilla%20%26%20React-blue)
![ML](https://img.shields.io/badge/ML-scikit--learn%20RandomForest-orange)
![Status](https://img.shields.io/badge/Status-Demo%20%2F%20Prototype-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

> **Demonstration of agentic automation capabilities for enterprise 5G network infrastructure.** Built as a proof-of-concept for Nokia's domain: closed-loop, ML-driven network operations where software agents sense network state, predict load, and act autonomously — no human in the loop.

---

## What Agentic Automation Means for Network Infrastructure

Traditional network operations require an engineer to observe telemetry dashboards, interpret anomalies, and manually push configuration changes through a NETCONF/YANG interface. At scale — hundreds of gNB (5G base stations) across a metro area — this is not operationally feasible.

**Agentic automation** replaces the observe-interpret-act cycle with software agents that run continuously:

```
┌─────────────────────────────────────────────────────────┐
│              CLOSED-LOOP AUTOMATION CYCLE               │
│                                                         │
│   Telemetry              Prediction           Action    │
│   ─────────              ──────────           ──────    │
│  [Tower KPIs]  ──────▶  [AI Brain]  ──────▶  [Bot]     │
│  - Users                 RandomForest          NETCONF  │
│  - RSRP (dBm)            Load Forecast         Push     │
│  - Hour of day                                          │
│        ▲                                         │      │
│        └─────────────── Audit Log ──────────────┘      │
│                         Dashboard                       │
└─────────────────────────────────────────────────────────┘
```

This matters to Nokia specifically because the **Nokia Network Automation Platform** and **CloudBand** infrastructure both depend on this exact pattern: policy-driven closed loops that react to network events faster than any NOC analyst can. This demo implements that pattern from scratch at the agent level.

---

## System Overview

**NetOps-AI** is a self-healing 5G network prototype with three components that together form a complete agentic pipeline:

| Component | Role | Technology |
|---|---|---|
| `network_brain.py` | Trains load-prediction model on telemetry | scikit-learn RandomForest |
| `automation_bot.py` | Sense → Decide → Act loop | Python, NETCONF-style JSON |
| `dashboard.ts` / `dashboard.tsx` | Operator audit trail | Vanilla TypeScript + React |

---

## Capabilities Demonstrated

### 1. ML-Driven Load Prediction

`network_brain.py` trains a `CongestionPredictor` on synthetic 5G telemetry:

- **Features:** Connected user count, RSRP signal strength (dBm), hour of day
- **Target:** Continuous load factor (0.0–1.0), incorporating circadian traffic patterns via a sinusoidal hour term
- **Model:** `RandomForestRegressor` (100 estimators) — robust against telemetry noise, interpretable feature importance for network engineers
- **Output:** Serialized `5g_brain.pkl` model artifact for runtime inference

```python
# Load factor incorporates users, signal quality, and time-of-day traffic pattern
load = (users / 1200) + (np.sin(hour / 24 * 2 * np.pi) * 0.1) - (rsrp * 0.001)
```

The time-of-day sinusoidal term mirrors real 5G network behavior: peak hours (morning commute, evening rush) drive congestion independently of raw user counts.

### 2. Closed-Loop Automation Agent

`automation_bot.py` is the core agentic loop. It:

1. **Observes** tower metrics (user count, signal quality)
2. **Predicts** load using the trained ML model
3. **Decides** whether to intervene (threshold: load > 0.80)
4. **Acts** autonomously — generates NETCONF-compatible JSON config payloads and writes them to the tower's configuration log

```
Tower T-505 | 980 users | RSRP: -110 dBm | Hour: 18
  → Predicted Load: 0.93 (CRITICAL)
  → [ACTION] Antenna tilt: -6°, TX Power: +2dB
  → Config written to config_change_T-505.json
```

The decision logic mirrors real radio frequency (RF) optimization:
- **High congestion (> 90%):** Aggressive antenna tilt (-6°) to narrow beam and reduce interference
- **Moderate congestion (80–90%):** Conservative tilt (-3°) to redistribute coverage
- **TX power boost** applied universally to improve RSRP for edge-of-cell users

### 3. Operator Audit Dashboard

The dashboard provides a real-time audit trail of all automated configuration changes — essential for regulatory compliance in network operations where every configuration push must be logged and attributable.

Implemented in two flavors:
- **`dashboard.ts`** — Vanilla TypeScript, zero framework dependency, lightweight for embedded NOC tooling
- **`dashboard.tsx`** — React component version for integration into larger operator portals

```
┌──────────────────────────────────────────────────────────┐
│  NetOps-AI: Automation Log                               │
├─────────┬──────────────────────┬──────────┬─────────────┤
│ Tower   │ Action               │ Time     │ Status      │
├─────────┼──────────────────────┼──────────┼─────────────┤
│ T-505   │ ANTENNA_TILT -6deg   │ 18:00:01 │ ✅ SUCCESS  │
│ T-505   │ TX_POWER +2dB        │ 18:00:02 │ ✅ SUCCESS  │
│ T-101   │ LOAD_BALANCE_INIT    │ 18:05:10 │ ✅ SUCCESS  │
└─────────┴──────────────────────┴──────────┴─────────────┘
```

---

## Technical Architecture

### Agent Design Pattern

This demo uses the **Sense–Reason–Act (SRA)** pattern, the foundational loop in agentic AI systems:

```
┌──────────────────────────────────────────────────┐
│              NetworkAutomator Agent              │
│                                                  │
│  SENSE          REASON           ACT             │
│  ──────         ──────           ───             │
│  Read KPIs  →  RF Model     →  NETCONF Push      │
│  (users,       Predict          JSON config      │
│   rsrp,        load%            payload to       │
│   hour)        ↓                gNB endpoint     │
│                Threshold                         │
│                decision                          │
│                (>0.80 = act)                     │
└──────────────────────────────────────────────────┘
```

### Tech Stack

```
┌─────────────────────────────────────┐
│  ML Layer         network_brain.py  │
│  ─────────────────────────────────  │
│  numpy / pandas — data synthesis    │
│  scikit-learn   — RF regressor      │
│  joblib         — model persistence │
│                                     │
│  Automation Layer  automation_bot.py│
│  ─────────────────────────────────  │
│  pandas     — telemetry parsing     │
│  colorama   — operator console UX   │
│  json       — NETCONF-style payload │
│                                     │
│  Dashboard Layer  dashboard.ts/.tsx │
│  ─────────────────────────────────  │
│  Vanilla TS — zero-dependency UI    │
│  React (TSX) — composable component │
│  HTML5       — lightweight host     │
└─────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
# numpy>=1.21.0, pandas>=1.3.0, scikit-learn>=1.0.0, joblib>=1.1.0, colorama>=0.4.4
```

### Run the Demo

```bash
# 1. Clone
git clone https://github.com/A-Kuo/Nokia-AI-ML-Automation-Demo.git
cd Nokia-AI-ML-Automation-Demo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the AI model on synthetic 5G telemetry
python network_brain.py
# >> [AI] Training Model on 5G Telemetry...
# >> [AI] Model Trained. Accuracy (R2 Score): 0.97

# 4. Run the automation agent
python automation_bot.py
# [SYSTEM] AI Model Loaded.
# [ANALYSIS] Tower ID: T-101 | Status: Optimal. No action needed.
# [ANALYSIS] Tower ID: T-505 | [ALERT] Congestion Detected! → Config saved.

# 5. View the audit dashboard
tsc dashboard.ts && open index.html
# (or use the React component in dashboard.tsx in a React application)
```

---

## Nokia Domain Context

Nokia's core business is supplying the hardware and software that runs 5G networks — gNBs (Next Generation NodeBs), the Nokia Network Automation Platform (NAP), and their CloudBand NFV infrastructure. The automation loop this demo implements corresponds directly to:

| Nokia Product Layer | This Demo's Equivalent |
|---|---|
| Nokia NAP intent policies | `automation_bot.py` decision logic |
| 5G RAN telemetry ingestion | `network_brain.py` training data |
| SON (Self-Organizing Network) | The full closed-loop pipeline |
| NETCONF/YANG config push | `config_payload` JSON generation |
| NOC operations dashboard | `dashboard.ts` audit trail |

The self-organizing network (SON) automation goal — networks that reconfigure themselves in response to changing conditions — is exactly what this prototype demonstrates at a component level.

---

## Status

| Component | Status |
|---|---|
| ML load prediction (RandomForest) | ✅ Implemented |
| Closed-loop automation bot | ✅ Implemented |
| NETCONF config payload generation | ✅ Simulated (JSON stub) |
| Vanilla TypeScript dashboard | ✅ Implemented |
| React dashboard component | ✅ Implemented |
| Live NETCONF push to real gNB | ⏸️ Out of scope (demo) |
| Multi-tower batch automation | 🔄 Extension opportunity |

---

## Related Work

This demo is part of a broader portfolio exploring agentic frameworks and enterprise ML automation:

- **[crosscloud-ml-orchestration](https://github.com/A-Kuo/crosscloud-ml-orchestration)** — Multi-cloud ML orchestration with entropy-based routing; the cross-cloud infrastructure layer that would host a production version of this pipeline
- **[CIPHER](https://github.com/A-Kuo/CIPHER)** — On-device tactical AI using the same sense-reason-act agent pattern in a first-responder context (YOLO, local RAG, Qualcomm NPU)
- **[Agentic-Visualization-Framework](https://github.com/A-Kuo/Agentic-Visualization-Framework)** — Multi-agent pipeline for automated visualization generation; the observability layer for agentic systems like this one

---

## License

MIT — see [LICENSE](LICENSE)
