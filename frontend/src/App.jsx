import { useState } from "react";
import { brandScan } from "./api/client";

function App() {
  const [brand, setBrand] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [domain, setDomain] = useState("");

  const handleClick = async () => {
    if (!brand) return;

    try {
      setLoading(true);
      setError("");
      const data = await brandScan(brand, domain);
      setResults(data);
    } catch (err) {
      console.error(err);
      setError("Failed to connect to backend");
    } finally {
      setLoading(false);
    }
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

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {results && results.results && (
        <div style={{ marginTop: "20px" }}>
          <h3>Results:</h3>
          {results.results.map((item, index) => (
            <div key={index}>
              <p><strong>Domain:</strong> {item.domain}</p>
              <p><strong>Risk Score:</strong> {item.risk_score}</p>
              <hr />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;