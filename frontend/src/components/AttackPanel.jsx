function AttackPanel({ config, setConfig, onRun, loading }) {
  return (
    <div style={{
      background: "#1a1a1a",
      border: "1px solid #333",
      borderRadius: "8px",
      padding: "1.5rem",
      display: "flex",
      flexDirection: "column",
      gap: "1rem",
      maxWidth: "500px"
    }}>
      <h2 style={{ color: "#e0e0e0", marginBottom: "0.5rem" }}>Configure Simulation</h2>

      <label style={{ color: "#aaa", fontSize: "0.85rem" }}>
        Attack Type
        <select
          value={config.attack_type}
          onChange={e => setConfig({ ...config, attack_type: e.target.value })}
          style={{ display: "block", marginTop: "0.25rem", width: "100%", padding: "0.5rem", background: "#0f1117", color: "#e0e0e0", border: "1px solid #444", borderRadius: "4px" }}
        >
          <option value="none">None (baseline)</option>
          <option value="jamming">Jamming</option>
          <option value="rach_flood">RACH Flooding</option>
          <option value="carrier_sense">Carrier Sense Exploit</option>
        </select>
      </label>

      <label style={{ color: "#aaa", fontSize: "0.85rem" }}>
        Number of Ticks: {config.num_ticks}
        <input type="range" min="50" max="200" value={config.num_ticks}
          onChange={e => setConfig({ ...config, num_ticks: parseInt(e.target.value) })}
          style={{ display: "block", width: "100%", marginTop: "0.25rem" }}
        />
      </label>

      <label style={{ color: "#aaa", fontSize: "0.85rem" }}>
        Countermeasure Start Tick: {config.countermeasure_start_tick}
        <input type="range" min="10" max={config.num_ticks - 10} value={config.countermeasure_start_tick}
          onChange={e => setConfig({ ...config, countermeasure_start_tick: parseInt(e.target.value) })}
          style={{ display: "block", width: "100%", marginTop: "0.25rem" }}
        />
      </label>

      <button
        onClick={onRun}
        disabled={loading}
        style={{
          marginTop: "0.5rem",
          padding: "0.75rem",
          background: loading ? "#333" : "#4ade80",
          color: "#0f1117",
          border: "none",
          borderRadius: "4px",
          fontFamily: "monospace",
          fontWeight: "bold",
          fontSize: "1rem",
          cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "Running..." : "Run Simulation"}
      </button>
    </div>
  );
}

export default AttackPanel;
