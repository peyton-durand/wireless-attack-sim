# Wireless Attack Simulator

## Setup and Build Info

### Backend
* cd backend
* python -m venv venv
* venv\Scripts\activate (Windows)
* pip install -r requirements.txt
* uvicorn api.main:app --reload

### Frontend
* cd frontend
* npm install
* npm run dev

## Project Overview
A Python simulation that models three wireless availability attacks. Jamming, RACH flooding, and carrier sense exploits. The frontend displays 4-5 graphs per attack including a baseline, that shows the network degradation by tick. It then introduces a specific countermeasure for each attack and shows the network recovery through the same graphs. Other features include a markov state bar, editable node count, and multiple attack comparison.

## Course Themes Covered
* Availability issues in wireless systems (jamming, RACH flooding, carrier sense exploits)
* Wireless protocols (802.11 / cellular — attacks are protocol-specific)
* Fault tolerance (countermeasure and recovery side)
* Markov chains — modeling attack state transitions (bonus 5th theme, easy extension)

## Design Decisions, Trade-offs, and Limitations
### Tech Stack
|Tool|Purpose|
|---|---|
|React + Vite|Frontend UI|
|Recharts|Chart component in React|
|Axios|API calls from the frontend|
|Python + FastAPI|Simulation engine and REST API|

### Backend
* Python is used as the main language for modeling the network, attacks, and simulation engine. Fast API is a Python web framework for building APIs. It is ran locally with Uvicorn, an AGSI server.
* Pydantic is used in Fast API for request validation.

#### Design
* __Simulation__: Simulation class manages a tick loop that runs in a 3-step sequence:
  1. Call the set attack (or baseline)
  2. Call the countermeasure for set attack (none for baseline)
  3. Call record_metrics() to capture the state

* __Network__: Meant to perform similarly to a 802.11ac home network at baseline:
  - base_throughput = ~190 mbps (out of 380mbps)
  - packet_success_rate = ~0.98
  - connection_success_rate = ~0.99
  - channel_utilization = ~17-55% based on number of connected nodes

* __Markov Chain__: Runs after the simulation finishes.
Reads the recorded metrics and assigns a health state to each tick:
  - NORMAL -> DEGRADED -> FAILED -> RECOVERING
  - Computed as: ((packet success rate) * (1.0 - (channel utilization))) / (baseline_health)
  - Baseline health is the very first ticks values. This is used to anchor new computes to their own starting conditions.


### Frontend
* React with Vite as the build tool for fast reload
* Recharts for data visualization on the frontend
* Axios for easy HTTP requests to the backend

#### Design
* __Component split__: App.jsx is the main control with every other rendered part being passed in as a component. Allows for easy design changes.
* __Markov state visualization__: MarkovStateDisplay.jsx renders a color bar with 4 different color states (green=NORMAL, yellow=DEGRADED, red=FAILED, blue=RECOVERING).
* __Informative UI__: Stored information about each attack is stored and rendered as a display box for each individual attack.
* __Comparative view__: A ComparsionView.jsx component renders all three attacks over the same graphs for comparing degradation and recovery.

#### Flow
1) "Run Simulation" button sends POST to backend local host
2) Response stored and passed to SimulationChart.jsx
3) Recharts renders line charts
