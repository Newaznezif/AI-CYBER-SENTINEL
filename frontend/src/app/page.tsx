'use client';

import { Activity, AlertTriangle, ShieldAlert, Cpu, Network, Lock, Crosshair } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const mockChartData = [
  { time: '00:00', alerts: 12, blocks: 45 },
  { time: '04:00', alerts: 18, blocks: 32 },
  { time: '08:00', alerts: 45, blocks: 112 },
  { time: '12:00', alerts: 67, blocks: 154 },
  { time: '16:00', alerts: 34, blocks: 89 },
  { time: '20:00', alerts: 22, blocks: 65 },
  { time: '24:00', alerts: 15, blocks: 41 },
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
      <span className={trend > 0 ? 'text-green-400' : 'text-red-400'}>
        {trend > 0 ? '+' : ''}{trend}%
      </span>
      <span className="text-slate-500 ml-2">from last 24h</span>
    </div>
  </div>
);

export default function Dashboard() {
  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 pb-2 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-1">Global Dashboard</h1>
          <p className="text-slate-400 text-sm">System status & active threat intelligence overview.</p>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-sm font-medium transition-colors">
            Export Report
          </button>
          <button className="px-4 py-2 bg-[#38bdf8]/10 hover:bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/50 rounded-lg text-sm font-medium transition-all shadow-[0_0_10px_rgba(56,189,248,0.1)]">
            New Investigation
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Active Investigations" value="14" icon={Activity} color="blue" trend={+12} />
        <StatCard title="Critical Alerts" value="3" icon={AlertTriangle} color="red" trend={-5} />
        <StatCard title="Indicators Tracked" value="12,403" icon={Crosshair} color="purple" trend={+8} />
        <StatCard title="Auto-Blocked IPs" value="842" icon={ShieldAlert} color="emerald" trend={+24} />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Main Chart */}
        <div className="xl:col-span-2 glass-panel p-5 rounded-xl border border-slate-700/50 flex flex-col">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">Network Anomaly Trend</h2>
            <p className="text-xs text-slate-400">Total detected threats and mitigations over time</p>
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
              { name: 'Ollama AI Engine', status: 'Online', icon: Cpu, latency: '45ms' },
              { name: 'PCAP Analyzer', status: 'Processing', icon: Network, latency: '124ms' },
              { name: 'Suricata IDS', status: 'Online', icon: ShieldAlert, latency: '12ms' },
              { name: 'CTI Aggregator', status: 'Synced', icon: Lock, latency: '2s ago' },
            ].map((sys, idx) => (
              <div key={idx} className="flex justify-between items-center p-3 rounded-lg bg-slate-800/50 border border-slate-700 mt-2">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-md ${sys.status === 'Online' || sys.status === 'Synced' ? 'bg-green-500/10 text-green-400' : 'bg-blue-500/10 text-[#38bdf8]'}`}>
                    <sys.icon className="w-4 h-4" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-200">{sys.name}</p>
                    <p className="text-xs text-slate-500">{sys.latency}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${sys.status === 'Online' || sys.status === 'Synced' ? 'bg-green-500' : 'bg-[#38bdf8] animate-pulse'}`}></div>
                  <span className="text-xs font-medium text-slate-300">{sys.status}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-center">
            <h4 className="text-sm font-medium text-indigo-300 mb-1">MITRE ATT&CK Matrix Update</h4>
            <p className="text-xs text-slate-400 mb-3">Version 14.1 successfully synchronized.</p>
            <button className="text-xs font-semibold text-white bg-indigo-500 hover:bg-indigo-600 px-3 py-1.5 rounded transition-colors w-full">
              View Framework
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
