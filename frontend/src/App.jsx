import { useState } from "react";

function App() {
  const [brand, setBrand] = useState("");
  const [domain, setDomain] = useState("");
  const [message, setMessage] = useState("");

  const handleClick = () => {
    setMessage(`Analyzing risk for ${brand} → ${domain}`);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>SentinelAI</h1>
      <p>Brand Impersonation Detection</p>

      <input
        placeholder="Brand name"
        value={brand}
        onChange={(e) => setBrand(e.target.value)}
        style={{ display: "block", marginBottom: "10px" }}
      />

      <input
        placeholder="Suspicious domain"
        value={domain}
        onChange={(e) => setDomain(e.target.value)}
        style={{ display: "block", marginBottom: "10px" }}
      />

      <button onClick={handleClick}>
        Analyze Risk
      </button>

      {message && (
        <p style={{ marginTop: "20px" }}>
          {message}
        </p>
      )}
    </div>
  );
}

export default App;