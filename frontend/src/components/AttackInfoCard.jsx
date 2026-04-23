function AttackInfoCard({ title, description, protocol, countermeasure, accentColor }) {
  return (
    <article
      style={{
        background: "#1a1a1a",
        border: `1px solid ${accentColor}`,
        borderRadius: "8px",
        padding: "1rem",
      }}
    >
      <h3 style={{ color: "#e0e0e0", marginTop: 0, marginBottom: "0.75rem" }}>{title}</h3>
      <p style={{ color: "#b0b0b0", marginTop: 0, marginBottom: "0.75rem", lineHeight: 1.5 }}>
        {description}
      </p>
      <p style={{ color: "#aaa", margin: "0 0 0.5rem 0", lineHeight: 1.4 }}>
        <strong style={{ color: "#e0e0e0" }}>Protocol:</strong> {protocol}
      </p>
      <p style={{ color: "#aaa", margin: 0, lineHeight: 1.4 }}>
        <strong style={{ color: "#e0e0e0" }}>Countermeasure:</strong> {countermeasure}
      </p>
    </article>
  );
}

export default AttackInfoCard;
