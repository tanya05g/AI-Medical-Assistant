import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Link, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { Activity, BarChart3, Download, FileText, LogOut, Shield, Stethoscope, UploadCloud, Users } from "lucide-react";
import { ArcElement, BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, LineElement, PointElement, Tooltip } from "chart.js";
import { Bar, Doughnut, Line } from "react-chartjs-2";
import { api, API_URL } from "./api";
import "./index.css";

ChartJS.register(ArcElement, BarElement, CategoryScale, Legend, LinearScale, LineElement, PointElement, Tooltip);

const AuthContext = createContext(null);
const useAuth = () => useContext(AuthContext);

function AuthProvider({ children }) {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem("user") || "null"));
  const login = ({ access_token, user }) => {
    localStorage.setItem("token", access_token);
    localStorage.setItem("user", JSON.stringify(user));
    setUser(user);
  };
  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
  };
  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>;
}

function Protected({ children, admin = false }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  if (admin && user.role !== "admin") return <Navigate to="/dashboard" />;
  return children;
}

function Nav() {
  const { user, logout } = useAuth();
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2 font-bold text-ink"><Stethoscope className="h-5 w-5 text-clinical" />AI Medical Assistant</Link>
        <nav className="flex items-center gap-2 text-sm">
          {user ? (
            <>
              <Link className="btn-secondary" to="/dashboard">Dashboard</Link>
              {user.role === "admin" && <Link className="btn-secondary" to="/admin"><Shield className="h-4 w-4" />Admin</Link>}
              <button className="btn-secondary" onClick={logout}><LogOut className="h-4 w-4" />Logout</button>
            </>
          ) : (
            <>
              <Link className="btn-secondary" to="/login">Login</Link>
              <Link className="btn-primary" to="/register">Register</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

function Landing() {
  const features = ["CNN pneumonia classification", "Grad-CAM visual explanations", "PDF and CSV reports", "Protected clinical dashboard"];
  return (
    <main>
      <section className="bg-white">
        <div className="mx-auto grid min-h-[78vh] max-w-7xl items-center gap-10 px-4 py-14 lg:grid-cols-[1.1fr_0.9fr]">
          <div>
            <p className="mb-3 text-sm font-semibold uppercase tracking-wide text-clinical">Chest X-ray AI Decision Support</p>
            <h1 className="max-w-3xl text-4xl font-bold leading-tight text-ink md:text-6xl">AI Medical Assistant</h1>
            <p className="mt-5 max-w-2xl text-lg text-slate-600">Upload chest radiographs, receive pneumonia risk predictions, inspect heatmap explanations, and export clinical-style reports from a secure full-stack workflow.</p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Link className="btn-primary" to="/register"><Activity className="h-4 w-4" />Start Analysis</Link>
              <Link className="btn-secondary" to="/login">Open Dashboard</Link>
            </div>
          </div>
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <div className="aspect-[4/3] rounded-md bg-[radial-gradient(circle_at_30%_30%,#99f6e4,transparent_28%),linear-gradient(135deg,#0f766e,#14213d)] p-5 text-white">
              <div className="grid h-full grid-cols-2 gap-4">
                <div className="rounded-md bg-white/15 p-4 backdrop-blur"><FileText /> <p className="mt-3 font-semibold">Prediction</p><p className="text-3xl font-bold">92.4%</p></div>
                <div className="rounded-md bg-white/15 p-4 backdrop-blur"><BarChart3 /> <p className="mt-3 font-semibold">Risk</p><p className="text-3xl font-bold">High</p></div>
                <div className="col-span-2 rounded-md bg-white/15 p-4 backdrop-blur"><p className="font-semibold">Explainable AI heatmap overlay</p><div className="mt-3 h-20 rounded bg-gradient-to-r from-cyan-200 via-yellow-300 to-red-500" /></div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section className="mx-auto max-w-7xl px-4 py-12">
        <div className="grid gap-4 md:grid-cols-4">{features.map((item) => <div className="panel" key={item}><p className="font-semibold">{item}</p><p className="mt-2 text-sm text-slate-600">Built into the same authenticated workflow for reproducible analysis.</p></div>)}</div>
      </section>
      <section className="bg-slate-100 py-12">
        <div className="mx-auto max-w-7xl px-4">
          <h2 className="text-2xl font-bold">About the AI Model</h2>
          <p className="mt-3 max-w-3xl text-slate-600">The backend uses a TensorFlow/Keras convolutional neural network with OpenCV preprocessing. Training scripts calculate accuracy, classification metrics, and confusion matrices, while inference produces Grad-CAM overlays from the final convolutional block.</p>
        </div>
      </section>
    </main>
  );
}

function AuthForm({ mode }) {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const submit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const endpoint = mode === "register" ? "/api/auth/register" : "/api/auth/login";
      const payload = mode === "register" ? form : { email: form.email, password: form.password };
      const { data } = await api.post(endpoint, payload);
      login(data);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed");
    }
  };
  return (
    <main className="mx-auto flex min-h-[70vh] max-w-md items-center px-4">
      <form onSubmit={submit} className="panel w-full">
        <h1 className="text-2xl font-bold">{mode === "register" ? "Create account" : "Welcome back"}</h1>
        {mode === "register" && <input className="input mt-5" placeholder="Full name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required />}
        <input className="input mt-3" type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        <input className="input mt-3" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required minLength={6} />
        {error && <p className="mt-3 text-sm text-alert">{error}</p>}
        <button className="btn-primary mt-5 w-full">{mode === "register" ? "Register" : "Login"}</button>
      </form>
    </main>
  );
}

function Dashboard() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [history, setHistory] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);
  const latest = history[0];

  const refresh = async () => {
    const [historyRes, analyticsRes] = await Promise.all([api.get("/api/scans/history"), api.get("/api/scans/analytics")]);
    setHistory(historyRes.data);
    setAnalytics(analyticsRes.data);
  };
  useEffect(() => { refresh(); }, []);

  const chooseFile = (selected) => {
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  };
  const analyze = async () => {
    if (!file) return;
    setLoading(true);
    const form = new FormData();
    form.append("file", file);
    await api.post("/api/scans/analyze", form);
    setFile(null);
    setPreview("");
    await refresh();
    setLoading(false);
  };
  const doughnutData = useMemo(() => ({
    labels: ["Normal", "Pneumonia"],
    datasets: [{ data: [analytics?.normal || 0, analytics?.pneumonia || 0], backgroundColor: ["#0f766e", "#b91c1c"] }]
  }), [analytics]);
  const lineData = useMemo(() => ({
    labels: analytics?.weekly?.map((d) => d.date.slice(5)) || [],
    datasets: [{ label: "Scans", data: analytics?.weekly?.map((d) => d.count) || [], borderColor: "#0f766e", backgroundColor: "#99f6e4" }]
  }), [analytics]);

  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <div className="grid gap-4 md:grid-cols-4">
        <Stat label="Total scans" value={analytics?.total || 0} icon={<Activity />} />
        <Stat label="Normal" value={analytics?.normal || 0} icon={<Shield />} />
        <Stat label="Pneumonia" value={analytics?.pneumonia || 0} icon={<Stethoscope />} />
        <Stat label="Avg confidence" value={`${analytics?.average_confidence || 0}%`} icon={<BarChart3 />} />
      </div>
      <div className="mt-6 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <section className="panel">
          <h2 className="text-xl font-bold">Upload X-ray</h2>
          <label onDragOver={(e) => e.preventDefault()} onDrop={(e) => { e.preventDefault(); chooseFile(e.dataTransfer.files[0]); }} className="mt-4 flex min-h-56 cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-slate-300 bg-slate-50 p-6 text-center">
            <UploadCloud className="h-10 w-10 text-clinical" />
            <span className="mt-3 font-semibold">Drag and drop or browse</span>
            <span className="text-sm text-slate-500">JPG, JPEG, PNG</span>
            <input type="file" className="hidden" accept=".jpg,.jpeg,.png" onChange={(e) => chooseFile(e.target.files[0])} />
          </label>
          {preview && <img src={preview} className="mt-4 max-h-72 w-full rounded-md object-contain" alt="X-ray preview" />}
          <button className="btn-primary mt-4 w-full" disabled={!file || loading} onClick={analyze}>{loading ? "Analyzing..." : "Run AI Analysis"}</button>
        </section>
        <section className="panel">
          <h2 className="text-xl font-bold">Latest Result</h2>
          {latest ? (
            <div className="mt-4">
              <div className="grid gap-4 md:grid-cols-2">
                <img src={`${API_URL}/api/scans/${latest.id}/image`} className="rounded-md border object-contain" alt="Original X-ray" />
                <img src={`${API_URL}/api/scans/${latest.id}/heatmap`} className="rounded-md border object-contain" alt="Grad-CAM heatmap" />
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-4">
                <Metric label="Prediction" value={latest.prediction} />
                <Metric label="Confidence" value={`${latest.confidence}%`} />
                <Metric label="Risk" value={latest.risk_level} />
                <Metric label="Timestamp" value={new Date(latest.created_at).toLocaleString()} />
              </div>
              <a className="btn-secondary mt-4" href={`${API_URL}/api/scans/${latest.id}/report`}><Download className="h-4 w-4" />Download PDF</a>
            </div>
          ) : <p className="mt-4 text-slate-600">No scans analyzed yet.</p>}
        </section>
      </div>
      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <section className="panel"><h2 className="mb-4 text-xl font-bold">Normal vs Pneumonia</h2><Doughnut data={doughnutData} /></section>
        <section className="panel"><h2 className="mb-4 text-xl font-bold">Weekly Trends</h2><Line data={lineData} /></section>
      </div>
      <section className="panel mt-6">
        <div className="flex items-center justify-between"><h2 className="text-xl font-bold">Prediction History</h2><a className="btn-secondary" href={`${API_URL}/api/scans/exports/history.csv`}><Download className="h-4 w-4" />CSV</a></div>
        <HistoryTable rows={history} />
      </section>
    </main>
  );
}

function Stat({ label, value, icon }) {
  return <div className="panel"><div className="flex items-center justify-between text-slate-500">{label}<span className="text-clinical">{icon}</span></div><p className="mt-2 text-2xl font-bold text-ink">{value}</p></div>;
}

function Metric({ label, value }) {
  return <div className="rounded-md bg-slate-50 p-3"><p className="text-xs font-semibold uppercase text-slate-500">{label}</p><p className="mt-1 font-bold text-ink">{value}</p></div>;
}

function HistoryTable({ rows }) {
  return (
    <div className="mt-4 overflow-x-auto">
      <table className="w-full min-w-[760px] text-left text-sm">
        <thead className="bg-slate-100 text-slate-600"><tr><th className="p-3">ID</th><th>Prediction</th><th>Confidence</th><th>Risk</th><th>Date</th><th>Report</th></tr></thead>
        <tbody>{rows.map((row) => <tr className="border-t" key={row.id}><td className="p-3">{row.id}</td><td>{row.prediction}</td><td>{row.confidence}%</td><td>{row.risk_level}</td><td>{new Date(row.created_at).toLocaleString()}</td><td><a className="text-clinical underline" href={`${API_URL}/api/scans/${row.id}/report`}>PDF</a></td></tr>)}</tbody>
      </table>
    </div>
  );
}

function Admin() {
  const [users, setUsers] = useState([]);
  const [scans, setScans] = useState([]);
  const [search, setSearch] = useState("");
  const load = async () => {
    const [userRes, scanRes] = await Promise.all([api.get("/api/admin/users"), api.get(`/api/admin/scans?search=${encodeURIComponent(search)}`)]);
    setUsers(userRes.data);
    setScans(scanRes.data);
  };
  useEffect(() => { load(); }, []);
  const remove = async (id) => {
    await api.delete(`/api/admin/scans/${id}`);
    await load();
  };
  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <div className="grid gap-4 md:grid-cols-2"><Stat label="Users" value={users.length} icon={<Users />} /><Stat label="All scans" value={scans.length} icon={<Activity />} /></div>
      <section className="panel mt-6">
        <div className="flex gap-3"><input className="input" placeholder="Search records" value={search} onChange={(e) => setSearch(e.target.value)} /><button className="btn-primary" onClick={load}>Search</button></div>
        <div className="mt-5 overflow-x-auto"><table className="w-full min-w-[760px] text-sm"><thead className="bg-slate-100"><tr><th className="p-3 text-left">ID</th><th className="text-left">User</th><th className="text-left">Prediction</th><th className="text-left">Confidence</th><th className="text-left">Risk</th><th></th></tr></thead><tbody>{scans.map((scan) => <tr className="border-t" key={scan.id}><td className="p-3">{scan.id}</td><td>{scan.user_id}</td><td>{scan.prediction}</td><td>{scan.confidence}%</td><td>{scan.risk_level}</td><td><button className="text-alert underline" onClick={() => remove(scan.id)}>Delete</button></td></tr>)}</tbody></table></div>
      </section>
    </main>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Nav />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<AuthForm mode="login" />} />
          <Route path="/register" element={<AuthForm mode="register" />} />
          <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
          <Route path="/admin" element={<Protected admin><Admin /></Protected>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
