'use client';

import { Activity, DownloadCloud } from 'lucide-react';

export default function TelemetryPage() {
  return (
    <div className="space-y-6 animate-slide-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-1">Network Telemetry</h1>
          <p className="text-slate-400 text-sm">Live packet captures and Zeek log monitoring.</p>
        </div>
        <button className="px-4 py-2 bg-[#38bdf8]/10 text-[#38bdf8] border border-[#38bdf8]/30 rounded-lg text-sm font-medium hover:bg-[#38bdf8]/20 transition-colors">
          <DownloadCloud className="w-4 h-4 inline mr-2" />
          Export PCAP
        </button>
      </div>

      <div className="glass-panel rounded-xl border border-slate-700/50 p-8 text-center flex flex-col items-center justify-center min-h-[400px]">
        <div className="w-16 h-16 bg-[#38bdf8]/10 rounded-full flex items-center justify-center mb-4">
          <Activity className="w-8 h-8 text-[#38bdf8]" />
        </div>
        <h2 className="text-xl font-semibold text-white mb-2">Telemetry Offline</h2>
        <p className="text-slate-400 max-w-md">
          The network sensor is currently initializing. Raw PCAP data and connection logs will appear here once the engine starts.
        </p>
      </div>
    </div>
  );
}
