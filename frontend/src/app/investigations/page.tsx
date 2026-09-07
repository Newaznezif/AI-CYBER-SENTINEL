'use client';

import { Search, Filter, AlertTriangle, Play, CheckCircle2, XCircle, RefreshCw } from 'lucide-react';
import Link from 'next/link';
import { useState, useEffect } from 'react';

export default function InvestigationsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [investigations, setInvestigations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchInvestigations = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/investigations');
      if (!res.ok) throw new Error('Failed to fetch investigations');
      const data = await res.json();
      setInvestigations(data);
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInvestigations();
  }, []);

  const filtered = investigations.filter((inv: any) => 
    (inv.investigation_number?.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (inv.title?.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-6 animate-slide-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-1">Investigations</h1>
          <p className="text-slate-400 text-sm">Manage, analyze, and resolve active security incidents.</p>
        </div>
        <button className="px-4 py-2 bg-[#38bdf8] text-slate-900 font-bold rounded-lg text-sm hover:bg-[#38bdf8]/90 transition-colors shadow-[0_0_15px_rgba(56,189,248,0.4)]">
          Create Case
        </button>
      </div>

      <div className="glass-panel p-4 rounded-xl border border-slate-700/50 flex flex-col sm:flex-row gap-4 items-center">
        <div className="flex-1 w-full relative">
          <Search className="absolute left-3 top-2.5 h-5 w-5 text-slate-500" />
          <input 
            type="text" 
            placeholder="Search by ID, title, or attribute..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-10 pr-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-[#38bdf8] transition-colors"
          />
        </div>
        <button className="flex items-center px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-700 transition-colors">
          <Filter className="w-4 h-4 mr-2" />
          Filters
        </button>
      </div>

      <div className="glass-panel rounded-xl border border-slate-700/50 overflow-hidden min-h-[300px]">
        {loading ? (
          <div className="flex flex-col items-center justify-center p-12 text-slate-400">
            <RefreshCw className="w-8 h-8 animate-spin text-[#38bdf8] mb-4" />
            <p>Loading investigations...</p>
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center p-12 text-slate-400 text-center">
            <XCircle className="w-12 h-12 text-red-500 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Failed to load</h3>
            <p className="mb-4">{error}</p>
            <button onClick={fetchInvestigations} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm rounded-lg flex items-center transition-colors">
              <RefreshCw className="w-4 h-4 mr-2" /> Retry
            </button>
          </div>
        ) : investigations.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12 text-slate-400 text-center">
            <CheckCircle2 className="w-12 h-12 text-emerald-500 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">No active investigations</h3>
            <p className="mb-4">Everything looks quiet. There are no investigations currently recorded.</p>
            <button onClick={fetchInvestigations} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm rounded-lg flex items-center transition-colors">
              <RefreshCw className="w-4 h-4 mr-2" /> Refresh
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/50 text-xs uppercase font-semibold text-slate-500 border-b border-slate-800">
                <tr>
                  <th className="px-6 py-4">Case ID / Title</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4">Severity</th>
                  <th className="px-6 py-4">Confidence</th>
                  <th className="px-6 py-4">Created Time</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {filtered.map((inv: any) => (
                  <tr key={inv.id} className="hover:bg-slate-800/30 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="font-medium text-slate-200 mb-1">{inv.investigation_number || `INV-${inv.id}`}</div>
                      <div className="text-slate-400 text-xs">{inv.title}</div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${
                        inv.status === 'ACTIVE' || inv.status === 'Active' ? 'bg-blue-500/10 text-[#38bdf8] border-[#38bdf8]/20' :
                        inv.status === 'CLOSED' || inv.status === 'Closed' ? 'bg-green-500/10 text-emerald-400 border-emerald-500/20' :
                        'bg-slate-500/10 text-slate-300 border-slate-500/20'
                      }`}>
                        {inv.status || 'Active'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        {inv.severity === 'CRITICAL' && <AlertTriangle className="w-4 h-4 text-red-500" />}
                        {inv.severity === 'HIGH' && <AlertTriangle className="w-4 h-4 text-orange-500" />}
                        <span className={`
                          ${inv.severity === 'CRITICAL' ? 'text-red-400' : ''}
                          ${inv.severity === 'HIGH' ? 'text-orange-400' : ''}
                          ${inv.severity === 'MEDIUM' ? 'text-yellow-400' : ''}
                          ${inv.severity === 'LOW' ? 'text-blue-400' : ''}
                        `}>{inv.severity}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">{(inv.confidence * 100).toFixed(0)}%</td>
                    <td className="px-6 py-4">{new Date(inv.created_at).toLocaleString()}</td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button className="text-slate-400 hover:text-white" title="Analyze with AI">
                          <Play className="w-4 h-4" />
                        </button>
                        <button className="text-slate-400 hover:text-emerald-400" title="Mark Resolved">
                          <CheckCircle2 className="w-4 h-4" />
                        </button>
                        <Link 
                          href={`/investigations/${inv.id}`} 
                          className="ml-2 px-3 py-1 bg-slate-800 hover:bg-slate-700 text-xs rounded border border-slate-700 text-slate-200"
                        >
                          View
                        </Link>
                      </div>
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
