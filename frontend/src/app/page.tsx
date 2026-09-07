'use client';

import { Activity, AlertTriangle, ShieldAlert, Cpu, Network, Lock, Crosshair, RefreshCw, XCircle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useState, useEffect } from 'react';

const mockChartData = [
  { time: '00:00', alerts: 1, blocks: 4 },
  { time: '04:00', alerts: 2, blocks: 3 },
  { time: '08:00', alerts: 5, blocks: 11 },
  { time: '12:00', alerts: 7, blocks: 15 },
  { time: '16:00', alerts: 3, blocks: 8 },
  { time: '20:00', alerts: 2, blocks: 6 },
  { time: '24:00', alerts: 1, blocks: 4 },
];

const StatCard = ({ title, value, icon: Icon, color, trend }: any) => (
  <div className="glass-panel p-5 rounded-xl border border-slate-700/50 hover:border-[#38bdf8]/30 transition-all duration-300 relative group overflow-hidden">
    <div className={`absolute top-0 right-0 w-32 h-32 bg-${color}-500/10 rounded-full blur-3xl -mr-10 -mt-10 group-hover:bg-${color}-500/20 transition-all`}></div>
    <div className="flex justify-between items-start mb-4 relative z-10">
      <div>
        <p className="text-slate-400 text-sm font-medium mb-1">{title}</p>
        <h3 className="text-3xl font-bold text-white tracking-tight">{value}</h3>
      </div>
      <div className={`p-3 rounded-lg bg-${color}-500/10 text-${color}-400 border border-${color}-500/20 shadow-[0_0_15px_rgba(var(--color-${color}-rgb),0.2)]`}>
        <Icon className="w-6 h-6" />
      </div>
    </div>
    <div className="flex items-center text-xs relative z-10">
      <span className={trend > 0 ? 'text-green-400' : trend < 0 ? 'text-red-400' : 'text-slate-400'}>
        {trend > 0 ? '+' : ''}{trend}%
      </span>
      <span className="text-slate-500 ml-2">from last 24h</span>
    </div>
  </div>
);

export default function Dashboard() {
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [metrics, setMetrics] = useState({ investigations: 0, indicators: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchDashboardData = async () => {
    setLoading(true);
    setError('');
    try {
      const [health, invs, inds] = await Promise.all([
        fetch('http://127.0.0.1:8000/api/v1/system-health').then(r => r.ok ? r.json() : null),
        fetch('http://127.0.0.1:8000/api/v1/investigations').then(r => r.ok ? r.json() : []),
        fetch('http://127.0.0.1:8000/api/v1/indicators').then(r => r.ok ? r.json() : [])
      ]);
      setHealthStatus(health);
      setMetrics({ investigations: invs.length || 0, indicators: inds.length || 0 });
    } catch (err: any) {
      setError(err.message || 'Error syncing backend data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 pb-2 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-1">Global Dashboard</h1>
          <p className="text-slate-400 text-sm">System status & active threat intelligence overview.</p>
        </div>
        <div className="flex gap-3">
          <button onClick={fetchDashboardData} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-sm font-medium transition-colors flex items-center">
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} /> Sync
          </button>
          <button className="px-4 py-2 bg-[#38bdf8]/10 hover:bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/50 rounded-lg text-sm font-medium transition-all shadow-[0_0_10px_rgba(56,189,248,0.1)]">
            New Investigation
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-lg flex items-center">
          <XCircle className="w-5 h-5 mr-3" />
          <span>{error}</span>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Active Investigations" value={loading ? '-' : metrics.investigations} icon={Activity} color="blue" trend={0} />
        <StatCard title="Critical Alerts" value="0" icon={AlertTriangle} color="red" trend={0} />
        <StatCard title="Indicators Tracked" value={loading ? '-' : metrics.indicators} icon={Crosshair} color="purple" trend={0} />
        <StatCard title="Auto-Blocked IPs" value="0" icon={ShieldAlert} color="emerald" trend={0} />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Main Chart */}
        <div className="xl:col-span-2 glass-panel p-5 rounded-xl border border-slate-700/50 flex flex-col">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">Network Anomaly Trend</h2>
            <p className="text-xs text-slate-400">Total detected threats over time</p>
          </div>
          <div className="flex-1 min-h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorAlerts" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorBlocks" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#38bdf8" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="time" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px' }}
                  itemStyle={{ color: '#e2e8f0' }}
                />
                <Area type="monotone" dataKey="alerts" stroke="#ef4444" fillOpacity={1} fill="url(#colorAlerts)" strokeWidth={2} />
                <Area type="monotone" dataKey="blocks" stroke="#38bdf8" fillOpacity={1} fill="url(#colorBlocks)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* System Health */}
        <div className="glass-panel p-5 rounded-xl border border-slate-700/50">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">System Status</h2>
            <p className="text-xs text-slate-400">Core intelligence components health</p>
          </div>
          
          <div className="space-y-4">
            {[
              { name: 'PostgreSQL DB', status: (healthStatus?.PostgreSQL) ? 'Online' : 'Offline', icon: Lock },
              { name: 'Ollama AI Engine', status: (healthStatus?.Ollama) ? 'Online' : 'Offline', icon: Cpu },
              { name: 'API Server', status: (healthStatus?.API) ? 'Online' : 'Loading', icon: Network },
              { name: 'Suricata IDS', status: (healthStatus?.Suricata) ? 'Online' : 'Offline', icon: ShieldAlert },
              { name: 'CTI Aggregator', status: (healthStatus?.VirusTotal || healthStatus?.OTX) ? 'Online' : 'Offline', icon: Activity },
            ].map((sys, idx) => (
              <div key={idx} className="flex justify-between items-center p-3 rounded-lg bg-slate-800/50 border border-slate-700 mt-2">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-md ${sys.status === 'Online' || sys.status === 'Synced' ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-500'}`}>
                    <sys.icon className="w-4 h-4" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-200">{sys.name}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${sys.status === 'Online' || sys.status === 'Synced' ? 'bg-green-500' : 'bg-red-500 animate-pulse'}`}></div>
                  <span className="text-xs font-medium text-slate-300">{sys.status}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-center">
            <h4 className="text-sm font-medium text-indigo-300 mb-1">Backend Connectivity</h4>
            <p className="text-xs text-slate-400 mb-3">{loading ? 'Checking status...' : (healthStatus ? 'API Connected successfully.' : 'API Unreachable.')}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
