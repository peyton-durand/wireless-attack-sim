const STATE_COLORS = {
  NORMAL: "#4ade80",
  DEGRADED: "#facc15",
  FAILED: "#f87171",
  RECOVERING: "#60a5fa",
};

function MarkovStateDisplay({ states, plotPadding = { left: 0, right: 0 }, compact = false }) {
  if (!states || states.length === 0) return null;

  const n = states.length;
  const interval = Math.ceil(n / 10);
  const ticks = Array.from({ length: n }, (_, i) => i).filter((i) => i % interval === 0);
  if (ticks[ticks.length - 1] !== n - 1) ticks.push(n - 1);

  const innerStyle = {
    marginLeft: `${plotPadding.left}px`,
    marginRight: `${plotPadding.right}px`,
  };

  const containerMarginBottom = compact ? "0.75rem" : "1.5rem";
  const titleMarginBottom = compact ? "0.35rem" : "0.5rem";
  const barHeight = compact ? "24px" : "36px";
  const axisHeight = compact ? "14px" : "16px";
  const axisMarginTop = compact ? "1px" : "2px";
  const tickFontSize = compact ? "0.6rem" : "0.65rem";
  const legendGap = compact ? "1rem" : "1.5rem";
  const legendMarginTop = compact ? "0.25rem" : "0.4rem";
  const legendSwatchSize = compact ? "10px" : "12px";
  const legendFontSize = compact ? "0.72rem" : "0.8rem";

  return (
    <div style={{ marginBottom: containerMarginBottom }}>
      <h3 style={{ marginBottom: titleMarginBottom, color: "#aaa", marginLeft: `${plotPadding.left}px` }}>
        Network State (Markov Chain)
      </h3>

      <div style={{ ...innerStyle, display: "flex", height: barHeight, borderRadius: "4px", overflow: "hidden" }}>
        {states.map((state, i) => (
          <div
            key={i}
            title={`Tick ${i}: ${state}`}
            style={{ flex: 1, background: STATE_COLORS[state] }}
          />
        ))}
      </div>

      <div style={{ ...innerStyle, position: "relative", height: axisHeight, marginTop: axisMarginTop }}>
        {ticks.map((tick) => {
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
                fontSize: tickFontSize,
                color: "#555",
                userSelect: "none",
              }}
            >
              {tick}
            </span>
          );
        })}
      </div>

      <div
        style={{
          display: "flex",
          gap: legendGap,
          marginTop: legendMarginTop,
          flexWrap: "wrap",
          marginLeft: `${plotPadding.left}px`,
        }}
      >
        {Object.entries(STATE_COLORS).map(([state, color]) => (
          <div key={state} style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
            <div style={{ width: legendSwatchSize, height: legendSwatchSize, borderRadius: "2px", background: color }} />
            <span style={{ color: "#aaa", fontSize: legendFontSize }}>{state}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MarkovStateDisplay;
