// This is the main entry point for the React frontend.
// It defines the App component, which checks the health of the backend API
// and displays the status on the page.

import { useEffect, useState } from "react";
import axios from "axios"; // axios is a library that makes it easy to send HTTP requests from the browser

function App() {
  const [status, setStatus] = useState(null);

  // When the component mounts, we send a GET request to the backend's health endpoint
  useEffect(() => {
    axios.get("http://localhost:8000/health")
      .then(res => setStatus(res.data.status))
      .catch(() => setStatus("error — is the backend running?"));
  }, []);

  // This is what the component renders.
  return (
    <div style={{ fontFamily: "monospace", padding: "2rem" }}>
      <h1>Wireless Attack Simulator</h1>
      <p>Backend status: <strong>{status ?? "checking..."}</strong></p>
    </div>
  );
}

export default App;