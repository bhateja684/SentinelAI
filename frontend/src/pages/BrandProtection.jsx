import { useState } from "react";
import { brandScan } from "../api/client";

function BrandProtection() {
  const [brand, setBrand] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [domain, setDomain] = useState("");

  const handleClick = async () => {
    if (!brand || !domain) return;

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

  // ✅ SAFE PERCENTAGE HANDLING
//   const percentage = results?.risk_score
//     ? parseInt(results.risk_score.toString().replace("%", ""))
//     : 0;
const percentage =
  results && results.risk_score !== undefined
    ? Math.round(Number(results.risk_score) * 100)
    : 0;

  return (
    <div className="max-w-4xl mx-auto space-y-12">

      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900">
          Brand Impersonation Detection
        </h1>
        <p className="text-slate-500 mt-2">
          Analyze suspicious domains against your brand using AI-powered risk scoring.
        </p>
      </div>

      {/* Form Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm space-y-6">

        <input
          placeholder="Brand name"
          value={brand}
          onChange={(e) => setBrand(e.target.value)}
          className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
        />

        <input
          placeholder="Suspicious domain"
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
          className="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
        />

        <button
          onClick={handleClick}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-500 text-white rounded-lg py-3 font-semibold transition shadow-sm disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Analyze Risk"}
        </button>

        {error && (
          <p className="text-red-500 text-sm">{error}</p>
        )}
      </div>

      {/* Results */}
      {results && (
        <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm space-y-8 animate-fadeIn">

          {/* Header */}
          <div className="flex justify-between items-center">
            <h3 className="text-xl font-semibold text-slate-900">
              Risk Assessment Result
            </h3>

            <span
              className={`px-4 py-1 rounded-full text-sm font-semibold
                ${
                  results.risk_level === "HIGH"
                    ? "bg-red-100 text-red-600"
                    : results.risk_level === "MEDIUM"
                    ? "bg-yellow-100 text-yellow-600"
                    : "bg-green-100 text-green-600"
                }`}
            >
              {results.risk_level} RISK
            </span>
          </div>

          <div className="h-px bg-slate-200" />

          {/* Percentage + Bar */}
          <div>
            <p className="text-5xl font-bold text-slate-900">
              {percentage}%
            </p>

            <div className="w-full h-4 bg-slate-200 rounded-full mt-6 overflow-hidden">
              <div
                className={`h-full transition-all duration-1000 rounded-full ${
                  results.risk_level === "HIGH"
                    ? "bg-red-500"
                    : results.risk_level === "MEDIUM"
                    ? "bg-yellow-500"
                    : "bg-green-500"
                }`}
                style={{
                  width: `${percentage}%`,
                }}
              />
            </div>
          </div>

          {/* Explanation */}
          {results.explanation && (
            <div className="space-y-3 text-sm text-slate-700">
              <h4 className="font-semibold text-slate-900">
                Analysis Factors
              </h4>

              <div className="flex justify-between">
                <span>High Similarity</span>
                <span className={results.explanation.high_similarity ? "text-red-600" : "text-green-600"}>
                  {results.explanation.high_similarity ? "Detected" : "Not Detected"}
                </span>
              </div>

              <div className="flex justify-between">
                <span>High Entropy Pattern</span>
                <span className={results.explanation.high_entropy ? "text-red-600" : "text-green-600"}>
                  {results.explanation.high_entropy ? "Detected" : "Not Detected"}
                </span>
              </div>

              <div className="flex justify-between">
                <span>Suspicious Keyword</span>
                <span className={results.explanation.suspicious_keyword ? "text-red-600" : "text-green-600"}>
                  {results.explanation.suspicious_keyword ? "Detected" : "Not Detected"}
                </span>
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
}

export default BrandProtection;