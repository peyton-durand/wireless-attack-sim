const STATE_COLORS = {
  NORMAL:     "#4ade80",  // green
  DEGRADED:   "#facc15",  // yellow
  FAILED:     "#f87171",  // red
  RECOVERING: "#60a5fa",  // blue
};

function MarkovStateDisplay({ states }) {
  if (!states || states.length === 0) return null;

  return (
    <div style={{ marginTop: "2rem" }}>
      <h3 style={{ marginBottom: "0.5rem", color: "#aaa" }}>Network State (Markov Chain)</h3>

      <div style={{ display: "flex", width: "100%", height: "36px", borderRadius: "4px", overflow: "hidden" }}>
        {states.map((state, i) => (
          <div
            key={i}
            title={`Tick ${i}: ${state}`}
            style={{ flex: 1, background: STATE_COLORS[state] }}
          />
        ))}
      </div>

      {/* Tick axis */}
      {(() => {
        const n = states.length;
        const interval = Math.ceil(n / 10);
        const ticks = Array.from({ length: n }, (_, i) => i).filter(i => i % interval === 0);
        if (ticks[ticks.length - 1] !== n - 1) ticks.push(n - 1);
        return (
          <div style={{ position: "relative", width: "100%", height: "16px", marginTop: "2px" }}>
            {ticks.map(tick => {
              const isFirst = tick === 0;
              const isLast = tick === n - 1;
              return (
                <span
                  key={tick}
                  style={{
                    position: "absolute",
                    left: isLast ? "auto" : `${(tick / (n - 1)) * 100}%`,
                    right: isLast ? "0" : "auto",
                    transform: isFirst || isLast ? "none" : "translateX(-50%)",
                    fontSize: "0.65rem",
                    color: "#555",
                    userSelect: "none",
                  }}
                >
                  {tick}
                </span>
              );
            })}
          </div>
        );
      })()}

      <div style={{ display: "flex", gap: "1.5rem", marginTop: "0.4rem", flexWrap: "wrap" }}>
        {Object.entries(STATE_COLORS).map(([state, color]) => (
          <div key={state} style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
            <div style={{ width: "12px", height: "12px", borderRadius: "2px", background: color }} />
            <span style={{ color: "#aaa", fontSize: "0.8rem" }}>{state}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MarkovStateDisplay;
