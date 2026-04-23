const STATE_COLORS = {
  NORMAL:     "#4ade80",  // green
  DEGRADED:   "#facc15",  // yellow
  FAILED:     "#f87171",  // red
  RECOVERING: "#60a5fa",  // blue
};

function MarkovStateDisplay({ states, plotPadding = { left: 0, right: 0 } }) {
  if (!states || states.length === 0) return null;

  const n = states.length;
  const interval = Math.ceil(n / 10);
  const ticks = Array.from({ length: n }, (_, i) => i).filter(i => i % interval === 0);
  if (ticks[ticks.length - 1] !== n - 1) ticks.push(n - 1);

  const innerStyle = {
    marginLeft: `${plotPadding.left}px`,
    marginRight: `${plotPadding.right}px`,
  };

  return (
    <div style={{ marginBottom: "1.5rem" }}>
      <h3 style={{ marginBottom: "0.5rem", color: "#aaa", marginLeft: `${plotPadding.left}px` }}>Network State (Markov Chain)</h3>

      {/* Color bar — inset to match chart plot area */}
      <div style={{ ...innerStyle, display: "flex", height: "36px", borderRadius: "4px", overflow: "hidden" }}>
        {states.map((state, i) => (
          <div
            key={i}
            title={`Tick ${i}: ${state}`}
            style={{ flex: 1, background: STATE_COLORS[state] }}
          />
        ))}
      </div>

      {/* Tick axis — same inset, positions computed relative to inner width */}
      <div style={{ ...innerStyle, position: "relative", height: "16px", marginTop: "2px" }}>
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

      <div style={{ display: "flex", gap: "1.5rem", marginTop: "0.4rem", flexWrap: "wrap", marginLeft: `${plotPadding.left}px` }}>
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
