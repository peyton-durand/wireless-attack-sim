import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8000/health")
      .then(res => setStatus(res.data.status))
      .catch(() => setStatus("error — is the backend running?"));
  }, []);

  return (
    <div style={{ fontFamily: "monospace", padding: "2rem" }}>
      <h1>Wireless Attack Simulator</h1>
      <p>Backend status: <strong>{status ?? "checking..."}</strong></p>
    </div>
  );
}

export default App;