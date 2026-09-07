'use client';

import { Shield, ArrowLeft, Clock, Server, Terminal, ShieldAlert } from 'lucide-react';
import Link from 'next/link';

export default function InvestigationDetailsPage({ params }: { params: { id: string } }) {
  return (
    <div className="space-y-6 animate-slide-in">
      <div className="flex items-center gap-4 pb-4 border-b border-slate-800">
        <Link href="/investigations" className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors">
          <ArrowLeft className="w-5 h-5" />
        </Link>
        <div>
          <div className="flex items-center gap-3 mb-1">
            <h1 className="text-3xl font-bold text-white tracking-tight">INV-{params.id.toUpperCase()}</h1>
            <span className="bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider">Active</span>
          </div>
          <p className="text-slate-400 text-sm">Suspicious Lateral Movement via SMB</p>
        </div>
        <div className="ml-auto">
          <button className="px-4 py-2 bg-[#38bdf8] text-slate-900 font-bold rounded-lg text-sm hover:bg-[#38bdf8]/90 transition-colors shadow-[0_0_15px_rgba(56,189,248,0.4)]">
            Remediate Threat
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <div className="glass-panel p-6 rounded-xl border border-slate-700/50">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Terminal className="w-5 h-5 text-slate-400" />
              Event Timeline
            </h2>
            <div className="space-y-6 pl-4 border-l border-slate-700">
              <div className="relative">
                <div className="absolute -left-5 top-1 w-2.5 h-2.5 bg-red-500 rounded-full ring-4 ring-slate-900 group-hover:bg-red-400 transition-colors"></div>
                <h4 className="text-sm font-bold text-slate-200">Execution Blocked</h4>
                <p className="text-xs text-slate-500 mb-2">12:45 PM by Sentinel Agent</p>
                <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg text-xs font-mono text-pink-400">
                  <span className="text-slate-500">C:\Users\Admin> </span>
                  powershell.exe -enc JABzAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAEkATwAuAE0AZQBtAG8AcgB5AFMAdAByAGUAYQBtACg...
                </div>
              </div>
              <div className="relative">
                <div className="absolute -left-5 top-1 w-2.5 h-2.5 bg-orange-500 rounded-full ring-4 ring-slate-900 group-hover:bg-orange-400 transition-colors"></div>
                <h4 className="text-sm font-bold text-slate-200">Lateral Movement Detected</h4>
                <p className="text-xs text-slate-500 mb-2">12:42 PM via Suricata IDS</p>
                <p className="text-sm text-slate-400">Suspicious SMB activity directed at sensitive internal subnet originating from a compromised DMZ host.</p>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="glass-panel p-5 rounded-xl border border-slate-700/50">
            <h2 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 border-b border-slate-800 pb-2">Analysis Results</h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center bg-slate-900 p-2 rounded-lg border border-slate-800">
                <span className="text-xs text-slate-400 flex items-center gap-2"><ShieldAlert className="w-4 h-4 text-orange-500"/> Risk Score</span>
                <span className="font-bold text-orange-400 text-sm">89/100</span>
              </div>
              <div className="flex justify-between items-center bg-slate-900 p-2 rounded-lg border border-slate-800">
                <span className="text-xs text-slate-400 flex items-center gap-2"><Server className="w-4 h-4 text-blue-500"/> Source Asset</span>
                <span className="font-medium text-slate-200 text-sm">DMZ-SRV-01</span>
              </div>
              <div className="flex justify-between items-center bg-slate-900 p-2 rounded-lg border border-slate-800">
                <span className="text-xs text-slate-400 flex items-center gap-2"><Clock className="w-4 h-4 text-emerald-500"/> Extracted IOCs</span>
                <span className="font-medium text-emerald-400 text-sm">12 Entities</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
