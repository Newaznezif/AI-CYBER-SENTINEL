'use client';

import { Globe, AlertTriangle, Shield, Search, Zap, Crosshair, RefreshCw, XCircle } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function ThreatIntelligencePage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [indicators, setIndicators] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchIndicators = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/indicators');
      if (!res.ok) throw new Error('Failed to fetch indicators');
      const data = await res.json();
      setIndicators(data);
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIndicators();
  }, []);

  const filtered = indicators.filter((ind: any) => 
    (ind.value?.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (ind.indicator_type?.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-6 animate-slide-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-1">Threat Intelligence</h1>
          <p className="text-slate-400 text-sm">Aggregated multi-source indicators (OTX, VirusTotal, AbuseIPDB).</p>
        </div>
        <div className="flex gap-2">
          <button onClick={fetchIndicators} className="px-4 py-2 bg-slate-800 text-slate-200 border border-slate-700 rounded-lg text-sm font-medium hover:bg-slate-700 transition-colors flex items-center">
             <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} /> Sync
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
              <h3 className="text-2xl font-bold text-white mt-1">{indicators.length}</h3>
            </div>
            <div className="p-2 bg-blue-500/10 text-blue-400 rounded-lg">
              <Crosshair className="w-5 h-5" />
            </div>
          </div>
        </div>
        
        <div className="glass-panel p-4 rounded-xl border border-slate-700/50">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-slate-400">Tracked Campaigns</p>
              <h3 className="text-2xl font-bold text-red-500 mt-1">{loading ? '-' : Math.floor(indicators.length * 0.1)}</h3>
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
              <span className="w-8 h-8 rounded bg-gray-500/10 border border-gray-500/20 flex flex-col items-center justify-center text-[9px] font-bold text-gray-400" title="AlienVault OTX (Offline)">OTX</span>
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
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)} 
            className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-[#38bdf8]"
          />
        </div>
      </div>

      <div className="glass-panel rounded-xl border border-slate-700/50 overflow-hidden min-h-[300px]">
        {loading ? (
          <div className="flex flex-col items-center justify-center p-12 text-slate-400">
            <RefreshCw className="w-8 h-8 animate-spin text-[#38bdf8] mb-4" />
            <p>Loading indicators...</p>
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center p-12 text-slate-400 text-center">
            <XCircle className="w-12 h-12 text-red-500 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Failed to load</h3>
            <p className="mb-4">{error}</p>
            <button onClick={fetchIndicators} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm rounded-lg flex items-center transition-colors">
              <RefreshCw className="w-4 h-4 mr-2" /> Retry
            </button>
          </div>
        ) : indicators.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12 text-slate-400 text-center">
            <Shield className="w-12 h-12 text-emerald-500 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">No Indicators</h3>
            <p className="mb-4">There are no threat indicators populated yet.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/50 text-xs uppercase font-semibold text-slate-500 border-b border-slate-800">
                <tr>
                  <th className="px-6 py-4">Indicator</th>
                  <th className="px-6 py-4">Type</th>
                  <th className="px-6 py-4">Confidence</th>
                  <th className="px-6 py-4">Sources</th>
                  <th className="px-6 py-4">First Seen</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {filtered.map((ind: any) => (
                  <tr key={ind.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4 font-mono font-medium text-slate-200">{ind.value}</td>
                    <td className="px-6 py-4">
                      <span className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs font-semibold">
                        {ind.indicator_type || 'Unknown'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                          <div 
                            className={`h-full ${(ind.confidence || 0) * 100 > 80 ? 'bg-red-500' : (ind.confidence || 0) * 100 > 50 ? 'bg-orange-500' : 'bg-green-500'}`} 
                            style={{ width: `${(ind.confidence || 0) * 100}%` }}
                          ></div>
                        </div>
                        <span className={`text-xs font-bold ${(ind.confidence || 0) * 100 > 80 ? 'text-red-400' : (ind.confidence || 0) * 100 > 50 ? 'text-orange-400' : 'text-green-400'}`}>
                          {((ind.confidence || 0) * 100).toFixed(0)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs text-slate-400 flex items-center gap-1">
                        <Globe className="w-3 h-3" /> System
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {new Date(ind.created_at).toLocaleDateString()}
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
        )}
      </div>
    </div>
  );
}
