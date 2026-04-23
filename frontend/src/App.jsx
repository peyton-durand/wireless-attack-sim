// This is the main entry point for the React frontend.
// It defines the App component, which checks the health of the backend API
// and displays the status on the page.

import { useEffect, useState } from "react";
import axios from "axios"; // axios is a library that makes it easy to send HTTP requests from the browser
import AttackPanel from "./components/AttackPanel";
import SimulationChart from "./components/SimulationChart";

const DEFAULT_CONFIG = {
  attack_type: "none",
  num_nodes: 10,
  base_throughput: 100,
  packet_success_rate: 1,
  channel_utilization: 0,
  connection_success_rate: 1,
  num_ticks: 100,
  countermeasure_start_tick: 50,
};

function App() {
  const [config, setConfig] = useState(DEFAULT_CONFIG);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleRun() {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post("http://localhost:8000/simulate", config);
      setMetrics(res.data.metrics);
    } catch (e) {
      setError("Simulation failed — is the backend running?");
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
        <SimulationChart
          metrics={metrics}
          countermeasureStart={config.countermeasure_start_tick}
          attackType={config.attack_type}
        />
      </div>
    </div>
  );
}

export default App;
