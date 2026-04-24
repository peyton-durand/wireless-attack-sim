// This is the main entry point for the React frontend.
// It defines the App component, which checks the health of the backend API
// and displays the status on the page.

import { useState } from "react";
import axios from "axios"; // axios is a library that makes it easy to send HTTP requests from the browser
import AttackInfoCard from "./components/AttackInfoCard";
import AttackPanel from "./components/AttackPanel";
import ComparisonView from "./components/ComparisonView";
import SimulationChart from "./components/SimulationChart";

const DEFAULT_CONFIG = {
  attack_type: "none",
  num_nodes: 10,
  base_throughput: 300,
  packet_success_rate: 0.98,
  channel_utilization: 0.15,
  connection_success_rate: 0.99,
  offered_load: 0.65,
  noise_std: 0.02,
  num_ticks: 100,
  countermeasure_start_tick: 50,
};

const ATTACK_INFO = {
  jamming: {
    title: "Jamming",
    description: "An attacker transmits interference on the same channel, causing legitimate packets to fail and reducing throughput.",
    protocol: "Wireless PHY / 802.11 shared channel behavior",
    countermeasure: "Frequency hopping or channel switching to move traffic away from interference.",
    accentColor: "#4ade80",
  },
  rach_flood: {
    title: "RACH Flooding",
    description: "Spoofed devices flood the random access channel with fake requests, making it harder for real users to connect.",
    protocol: "Cellular Random Access Channel (RACH)",
    countermeasure: "Rate limiting, authentication, and backoff to reduce fake access attempts.",
    accentColor: "#fbbf24",
  },
  carrier_sense: {
    title: "Carrier Sense Exploit",
    description: "Fake RTS/NAV reservations keep nearby devices waiting, so the channel looks busy while real throughput collapses.",
    protocol: "802.11 CSMA/CA and NAV virtual carrier sensing",
    countermeasure: "NAV anomaly detection and timeout thresholds to ignore unrealistic reservations.",
    accentColor: "#60a5fa",
  },
};

function App() {
  const [config, setConfig] = useState(DEFAULT_CONFIG);
  const [metrics, setMetrics] = useState(null);
  const [comparisonResults, setComparisonResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleRun() {
    setLoading(true);
    setError(null);
    try {
      if (config.attack_type === "compare_all") {
        const { attack_type, ...compareConfig } = config;
        const res = await axios.post("http://localhost:8000/simulate/compare-all", compareConfig);
        setComparisonResults(res.data.results);
        setMetrics(null);
      } else {
        const res = await axios.post("http://localhost:8000/simulate", config);
        setMetrics(res.data.metrics);
        setComparisonResults(null);
      }
    } catch (e) {
      setError("Simulation failed - is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  // This is what the component renders.
  return (
    <div style={{ padding: "2rem", display: "flex", gap: "2rem", alignItems: "flex-start", minHeight: "100vh", boxSizing: "border-box" }}>
      <div style={{ flex: "0 0 320px" }}>
        <h1 style={{ marginBottom: "0.25rem" }}>Wireless Attack Simulator</h1>
        <p style={{ color: "#555", marginBottom: "2rem" }}>
          Simulating jamming, RACH flooding, and carrier sense exploits
        </p>

        <AttackPanel
          config={config}
          setConfig={setConfig}
          onRun={handleRun}
          loading={loading}
        />

        {error && <p style={{ color: "#f87171", marginTop: "1rem" }}>{error}</p>}
      </div>

      <div style={{ flex: 1, minWidth: 0 }}>
        {config.attack_type !== "compare_all" && (
          ATTACK_INFO[config.attack_type] && (
            <div style={{ marginTop: "2rem" }}>
              <AttackInfoCard {...ATTACK_INFO[config.attack_type]} />
            </div>
          )
        )}

        {config.attack_type === "compare_all" ? (
          <ComparisonView
            results={comparisonResults}
            countermeasureStart={config.countermeasure_start_tick}
          />
        ) : (
          <SimulationChart
            metrics={metrics}
            countermeasureStart={config.countermeasure_start_tick}
            attackType={config.attack_type}
          />
        )}
      </div>
    </div>
  );
}

export default App;
