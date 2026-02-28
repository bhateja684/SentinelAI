import BrandProtection from "./BrandProtection";
import Sidebar from "../components/Sidebar";

export default function Dashboard() {
  return (
    <div className="min-h-screen flex bg-slate-100 text-slate-900">
      <Sidebar />
      <main className="flex-1 p-12">
        <BrandProtection />
      </main>
    </div>
  );
}