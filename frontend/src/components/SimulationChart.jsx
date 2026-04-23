import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from "recharts";
import MarkovStateDisplay from "./MarkovStateDisplay";

// Shared layout constants — MarkovStateDisplay uses these to align with the plot area.
const CHART_MARGIN = { top: 5, right: 10, bottom: 5, left: 0 };
const YAXIS_WIDTH = 60;
const PLOT_PADDING = { left: CHART_MARGIN.left + YAXIS_WIDTH, right: CHART_MARGIN.right };

function SimulationChart({ metrics, countermeasureStart, attackType }) {
  if (!metrics) return null;

  // Recharts wants an array of objects, one per tick
  const data = metrics.ticks.map((tick, i) => ({
    tick,
    throughput: metrics.throughput[i],
    packet_success_rate: parseFloat((metrics.packet_success_rate[i] * 100).toFixed(1)),
    channel_utilization: parseFloat((metrics.channel_utilization[i] * 100).toFixed(1)),
    connection_success_rate: parseFloat((metrics.connection_success_rate[i] * 100).toFixed(1)),
    dropped_packets: metrics.dropped_packets[i],
  }));

  return (
    <div style={{ marginTop: "2rem" }}>
      <MarkovStateDisplay states={metrics.state_sequence} plotPadding={PLOT_PADDING} />

      {/* Throughput */}
      <h3 style={{ marginBottom: "0.5rem", color: "#aaa" }}>Throughput</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data} margin={CHART_MARGIN}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="tick" stroke="#555" />
          <YAxis stroke="#555" width={YAXIS_WIDTH} />
          <Tooltip contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }} />
          <ReferenceLine x={countermeasureStart} stroke="#facc15" strokeDasharray="4 4" label={{ value: "countermeasure", fill: "#facc15", fontSize: 11 }} />
          <Line type="monotone" dataKey="throughput" stroke="#4ade80" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>

      {/* Packet Success Rate */}
      <h3 style={{ marginBottom: "0.5rem", marginTop: "1.5rem", color: "#aaa" }}>Packet Success Rate (%)</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data} margin={CHART_MARGIN}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="tick" stroke="#555" />
          <YAxis stroke="#555" width={YAXIS_WIDTH} domain={[0, 100]} />
          <Tooltip contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }} />
          <ReferenceLine x={countermeasureStart} stroke="#facc15" strokeDasharray="4 4" />
          <Line type="monotone" dataKey="packet_success_rate" stroke="#f87171" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>

      {/* Channel Utilization */}
      <h3 style={{ marginBottom: "0.5rem", marginTop: "1.5rem", color: "#aaa" }}>Channel Utilization (%)</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data} margin={CHART_MARGIN}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="tick" stroke="#555" />
          <YAxis stroke="#555" width={YAXIS_WIDTH} domain={[0, 100]} />
          <Tooltip contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }} />
          <ReferenceLine x={countermeasureStart} stroke="#facc15" strokeDasharray="4 4" />
          <Line type="monotone" dataKey="channel_utilization" stroke="#60a5fa" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>

      {attackType === "rach_flood" && (
        <>
          {/* Connection Success Rate */}
          <h3 style={{ marginBottom: "0.5rem", marginTop: "1.5rem", color: "#aaa" }}>Connection Success Rate (%)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={data} margin={CHART_MARGIN}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="tick" stroke="#555" />
              <YAxis stroke="#555" width={YAXIS_WIDTH} domain={[0, 100]} />
              <Tooltip contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }} />
              <ReferenceLine x={countermeasureStart} stroke="#facc15" strokeDasharray="4 4" />
              <Line type="monotone" dataKey="connection_success_rate" stroke="#fbbf24" dot={false} strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </>
      )}

      {/* Dropped Packets */}
      <h3 style={{ marginBottom: "0.5rem", marginTop: "1.5rem", color: "#aaa" }}>Dropped Packets</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data} margin={CHART_MARGIN}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="tick" stroke="#555" />
          <YAxis stroke="#555" width={YAXIS_WIDTH} />
          <Tooltip contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }} />
          <ReferenceLine x={countermeasureStart} stroke="#facc15" strokeDasharray="4 4" />
          <Line type="monotone" dataKey="dropped_packets" stroke="#e879f9" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>

    </div>
  );
}

export default SimulationChart;
