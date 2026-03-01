import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="w-72 bg-white border-r border-slate-200 p-8">
      <h1 className="text-xl font-bold text-slate-900 mb-10">
  SentinelAI
      </h1>

      <nav className="space-y-4">
        <Link to="/dashboard" className="block px-4 py-2 rounded-lg hover:bg-slate-100 transition text-slate-600">
          Brand Protection
        </Link>

        <p className="text-slate-400">Signup Risk</p>
        <p className="text-slate-400">History</p>
        <p className="text-slate-400">Settings</p>
      </nav>
    </aside>
  );
}