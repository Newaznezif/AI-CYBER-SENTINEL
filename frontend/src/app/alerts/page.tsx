'use client';

import { AlertOctagon, Filter, CheckCircle2 } from 'lucide-react';

export default function AlertsPage() {
  return (
    <div className="space-y-6 animate-slide-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-1">Security Alerts</h1>
          <p className="text-slate-400 text-sm">Real-time alerts from Suricata IDS and Zeek analyzers.</p>
        </div>
        <button className="px-4 py-2 bg-slate-800 text-slate-200 border border-slate-700 rounded-lg text-sm font-medium hover:bg-slate-700 transition-colors">
          <Filter className="w-4 h-4 inline mr-2" />
          Filter Alerts
        </button>
      </div>

      <div className="glass-panel rounded-xl border border-slate-700/50 p-8 text-center flex flex-col items-center justify-center min-h-[400px]">
        <div className="w-16 h-16 bg-emerald-500/10 rounded-full flex items-center justify-center mb-4">
          <CheckCircle2 className="w-8 h-8 text-emerald-400" />
        </div>
        <h2 className="text-xl font-semibold text-white mb-2">No Active Alerts</h2>
        <p className="text-slate-400 max-w-md">
          Your network telemetry does not show any outstanding high-severity alerts at this moment. The system is continuously monitoring.
        </p>
      </div>
    </div>
  );
}
