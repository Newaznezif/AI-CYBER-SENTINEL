'use client';

import { Globe, AlertTriangle, Shield, Search, Zap, Crosshair } from 'lucide-react';
import { useState } from 'react';

const mockIndicators = [
  { id: 1, type: 'IPv4', value: '185.153.199.122', score: 87, source: 'AbuseIPDB', firstSeen: '2 hours ago', status: 'Blocked' },
  { id: 2, type: 'Domain', value: 'auth-update-alert.com', score: 92, source: 'VirusTotal', firstSeen: '3 days ago', status: 'Blocked' },
  { id: 3, type: 'Hash', value: '4b490f...1a9e3', score: 65, source: 'OTX', firstSeen: '12 hours ago', status: 'Monitored' },
  { id: 4, type: 'URL', value: 'http://malicious.net/payload.sh', score: 99, source: 'VirusTotal', firstSeen: '1 hour ago', status: 'Blocked' },
  { id: 5, type: 'IPv4', value: '45.79.130.12', score: 40, source: 'AbuseIPDB', firstSeen: '1 week ago', status: 'Monitored' },
];

export default function ThreatIntelligencePage() {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="space-y-6 animate-slide-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-1">Threat Intelligence</h1>
          <p className="text-slate-400 text-sm">Aggregated multi-source indicators (OTX, VirusTotal, AbuseIPDB).</p>
        </div>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-slate-800 text-slate-200 border border-slate-700 rounded-lg text-sm font-medium hover:bg-slate-700 transition-colors">
            Force Sync
          </button>
          <button className="px-4 py-2 bg-purple-500/10 text-purple-400 border border-purple-500/50 rounded-lg text-sm font-medium hover:bg-purple-500/20 transition-colors shadow-[0_0_10px_rgba(168,85,247,0.2)]">
            Manual Query
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-panel p-4 rounded-xl border border-slate-700/50">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-slate-400">Total Indicators</p>
              <h3 className="text-2xl font-bold text-white mt-1">45,102</h3>
            </div>
            <div className="p-2 bg-blue-500/10 text-blue-400 rounded-lg">
              <Crosshair className="w-5 h-5" />
            </div>
          </div>
        </div>
        
        <div className="glass-panel p-4 rounded-xl border border-slate-700/50">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-slate-400">High Confidence Threats</p>
              <h3 className="text-2xl font-bold text-red-500 mt-1">1,204</h3>
            </div>
            <div className="p-2 bg-red-500/10 text-red-400 rounded-lg">
              <AlertTriangle className="w-5 h-5" />
            </div>
          </div>
        </div>
        
        <div className="glass-panel p-4 rounded-xl border border-slate-700/50 flex">
          <div className="flex-1">
            <p className="text-sm font-medium text-slate-400 mb-2">API Health</p>
            <div className="flex gap-2">
              <span className="w-8 h-8 rounded bg-green-500/10 border border-green-500/20 flex flex-col items-center justify-center text-[9px] font-bold text-green-400" title="VirusTotal">VT</span>
              <span className="w-8 h-8 rounded bg-green-500/10 border border-green-500/20 flex flex-col items-center justify-center text-[9px] font-bold text-green-400" title="AbuseIPDB">AD</span>
              <span className="w-8 h-8 rounded bg-yellow-500/10 border border-yellow-500/20 flex flex-col items-center justify-center text-[9px] font-bold text-yellow-400" title="AlienVault OTX (Rate Limited)">OTX</span>
            </div>
          </div>
          <div className="p-2 bg-slate-800 text-slate-400 rounded-lg self-start">
            <Zap className="w-5 h-5" />
          </div>
        </div>
      </div>

      <div className="glass-panel p-4 rounded-xl border border-slate-700/50 flex flex-col sm:flex-row gap-4 items-center">
        <div className="flex-1 w-full relative">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
          <input 
            type="text" 
            placeholder="Search indicator value or source..." 
            className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-[#38bdf8]"
          />
        </div>
      </div>

      <div className="glass-panel rounded-xl border border-slate-700/50 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900/50 text-xs uppercase font-semibold text-slate-500 border-b border-slate-800">
              <tr>
                <th className="px-6 py-4">Indicator</th>
                <th className="px-6 py-4">Type</th>
                <th className="px-6 py-4">Risk Score</th>
                <th className="px-6 py-4">Sources</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {mockIndicators.map((ind) => (
                <tr key={ind.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-6 py-4 font-mono font-medium text-slate-200">{ind.value}</td>
                  <td className="px-6 py-4">
                    <span className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs font-semibold">
                      {ind.type}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div 
                          className={`h-full ${ind.score > 80 ? 'bg-red-500' : ind.score > 50 ? 'bg-orange-500' : 'bg-green-500'}`} 
                          style={{ width: `${ind.score}%` }}
                        ></div>
                      </div>
                      <span className={`text-xs font-bold ${ind.score > 80 ? 'text-red-400' : ind.score > 50 ? 'text-orange-400' : 'text-green-400'}`}>
                        {ind.score}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-xs text-slate-400 flex items-center gap-1">
                      <Globe className="w-3 h-3" /> {ind.source}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${
                      ind.status === 'Blocked' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                    }`}>
                      {ind.status === 'Blocked' && <Shield className="w-3 h-3 mr-1" />}
                      {ind.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-xs font-medium text-[#38bdf8] hover:text-[#38bdf8]/80 hover:underline">
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
