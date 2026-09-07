'use client';

import { Database, Upload, RefreshCw } from 'lucide-react';

export default function DataManagementPage() {
  return (
    <div className="space-y-6 animate-slide-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-1">Data Management</h1>
          <p className="text-slate-400 text-sm">Manage databases, backups, and data retention policies.</p>
        </div>
        <button className="px-4 py-2 bg-slate-800 text-slate-200 border border-slate-700 rounded-lg text-sm font-medium hover:bg-slate-700 transition-colors">
          <Upload className="w-4 h-4 inline mr-2" />
          Import Dataset
        </button>
      </div>

      <div className="glass-panel rounded-xl border border-slate-700/50 p-8 text-center flex flex-col items-center justify-center min-h-[400px]">
        <div className="w-16 h-16 bg-purple-500/10 rounded-full flex items-center justify-center mb-4">
          <Database className="w-8 h-8 text-purple-400" />
        </div>
        <h2 className="text-xl font-semibold text-white mb-2">Storage Healthy</h2>
        <p className="text-slate-400 max-w-md">
          Total usage: 45GB / 500GB. PostgreSQL connections and Redis caches are operating normally. No manual retention flush is required at this time.
        </p>
      </div>
    </div>
  );
}
