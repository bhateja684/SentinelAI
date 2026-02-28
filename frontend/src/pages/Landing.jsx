import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold text-blue-400 mb-6">
        SentinelAI
      </h1>

      <p className="text-slate-400 mb-8 text-center max-w-md">
        AI-powered digital risk protection for startups.
      </p>

      <Link
        to="/dashboard"
        className="bg-blue-600 px-6 py-3 rounded-lg hover:bg-blue-500 transition"
      >
        Go to Dashboard
      </Link>
    </div>
  );
}