import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import MarkovStateDisplay from "./MarkovStateDisplay";

const ATTACK_ORDER = ["jamming", "rach_flood", "carrier_sense"];

const ATTACK_LABELS = {
  jamming: "Jamming",
  rach_flood: "RACH Flooding",
  carrier_sense: "Carrier Sense Exploit",
};

const ATTACK_COLORS = {
  jamming: "#4ade80",
  rach_flood: "#fbbf24",
  carrier_sense: "#60a5fa",
};

const CHART_MARGIN = { top: 5, right: 20, bottom: 5, left: 0 };
const YAXIS_WIDTH = 60;
const PLOT_PADDING = { left: YAXIS_WIDTH, right: CHART_MARGIN.right };

function buildOverlayData(results, formatter = (_, value) => value) {
  const firstMetrics = results?.jamming?.metrics || results?.rach_flood?.metrics || results?.carrier_sense?.metrics;
  if (!firstMetrics?.ticks) return [];

  return firstMetrics.ticks.map((tick, index) => {
    const row = { tick };

    ATTACK_ORDER.forEach((attackType) => {
      const metrics = results[attackType]?.metrics;
      if (!metrics) return;

      Object.keys(metrics).forEach((metricKey) => {
        if (metricKey === "ticks" || metricKey === "state_sequence") return;
        row[`${attackType}_${metricKey}`] = formatter(metricKey, metrics[metricKey][index]);
      });
    });

    return row;
  });
}

function OverlayMetricChart({
  title,
  data,
  metricKey,
  domain,
  countermeasureStart,
}) {
  return (
    <section
      style={{
        background: "#1a1a1a",
        border: "1px solid #333",
        borderRadius: "8px",
        padding: "1.25rem",
      }}
    >
      <h2 style={{ color: "#e0e0e0", marginTop: 0, marginBottom: "0.75rem" }}>{title}</h2>
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={data} margin={CHART_MARGIN}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="tick" stroke="#555" />
          <YAxis stroke="#555" width={YAXIS_WIDTH} domain={domain} />
          <Tooltip contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }} />
          <Legend />
          <ReferenceLine x={countermeasureStart} stroke="#facc15" strokeDasharray="4 4" label={{ value: "countermeasure", fill: "#facc15", fontSize: 11 }} />
          {ATTACK_ORDER.map((attackType) => (
            <Line
              key={attackType}
              type="monotone"
              dataKey={`${attackType}_${metricKey}`}
              name={ATTACK_LABELS[attackType]}
              stroke={ATTACK_COLORS[attackType]}
              dot={false}
              strokeWidth={2}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </section>
  );
}

function SingleAttackMetricChart({
  title,
  data,
  attackType,
  metricKey,
  domain,
  countermeasureStart,
}) {
  return (
    <section
      style={{
        background: "#1a1a1a",
        border: "1px solid #333",
        borderRadius: "8px",
        padding: "1.25rem",
      }}
    >
      <h2 style={{ color: "#e0e0e0", marginTop: 0, marginBottom: "0.75rem" }}>{title}</h2>
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={data} margin={CHART_MARGIN}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="tick" stroke="#555" />
          <YAxis stroke="#555" width={YAXIS_WIDTH} domain={domain} />
          <Tooltip contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }} />
          <Legend />
          <ReferenceLine x={countermeasureStart} stroke="#facc15" strokeDasharray="4 4" label={{ value: "countermeasure", fill: "#facc15", fontSize: 11 }} />
          <Line
            type="monotone"
            dataKey={`${attackType}_${metricKey}`}
            name={ATTACK_LABELS[attackType]}
            stroke={ATTACK_COLORS[attackType]}
            dot={false}
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </section>
  );
}

function ComparisonView({ results, countermeasureStart }) {
  if (!results) return null;

  const rawData = buildOverlayData(results);
  const percentData = buildOverlayData(results, (metricKey, value) => {
    if (
      metricKey === "packet_success_rate" ||
      metricKey === "channel_utilization" ||
      metricKey === "connection_success_rate"
    ) {
      return parseFloat((value * 100).toFixed(1));
    }

    return value;
  });

  return (
    <div style={{ marginTop: "2rem", display: "grid", gap: "1.5rem" }}>
      <section
        style={{
          background: "#1a1a1a",
          border: "1px solid #333",
          borderRadius: "8px",
          padding: "1.25rem",
        }}
      >
        <h2 style={{ color: "#e0e0e0", marginTop: 0, marginBottom: "1rem" }}>Markov State Comparison</h2>
        {ATTACK_ORDER.map((attackType) => (
          <div key={attackType} style={{ marginBottom: attackType === ATTACK_ORDER[ATTACK_ORDER.length - 1] ? 0 : "1rem" }}>
            <h3 style={{ color: ATTACK_COLORS[attackType], marginTop: 0, marginBottom: "0.5rem" }}>{ATTACK_LABELS[attackType]}</h3>
            <MarkovStateDisplay
              states={results[attackType]?.metrics?.state_sequence}
              plotPadding={PLOT_PADDING}
            />
          </div>
        ))}
      </section>

      <OverlayMetricChart
        title="Throughput Comparison"
        data={rawData}
        metricKey="throughput"
        countermeasureStart={countermeasureStart}
      />

      <OverlayMetricChart
        title="Packet Success Rate Comparison (%)"
        data={percentData}
        metricKey="packet_success_rate"
        domain={[0, 100]}
        countermeasureStart={countermeasureStart}
      />

      <OverlayMetricChart
        title="Channel Utilization Comparison (%)"
        data={percentData}
        metricKey="channel_utilization"
        domain={[0, 100]}
        countermeasureStart={countermeasureStart}
      />

      <SingleAttackMetricChart
        title="RACH Flooding Connection Success Rate (%)"
        data={percentData}
        attackType="rach_flood"
        metricKey="connection_success_rate"
        domain={[0, 100]}
        countermeasureStart={countermeasureStart}
      />

      <OverlayMetricChart
        title="Dropped Packets Comparison"
        data={rawData}
        metricKey="dropped_packets"
        countermeasureStart={countermeasureStart}
      />
    </div>
  );
}

export default ComparisonView;
