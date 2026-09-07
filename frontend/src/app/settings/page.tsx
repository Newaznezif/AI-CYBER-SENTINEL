'use client';

import { Settings, Shield, User, Bell } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div className="space-y-6 animate-slide-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-1">Settings</h1>
          <p className="text-slate-400 text-sm">System configuration, API keys, and user preferences.</p>
        </div>
      </div>

      <div className="glass-panel rounded-xl border border-slate-700/50 p-8 text-center flex flex-col items-center justify-center min-h-[400px]">
        <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mb-4">
          <Settings className="w-8 h-8 text-slate-400" />
        </div>
        <h2 className="text-xl font-semibold text-white mb-2">Configuration</h2>
        <p className="text-slate-400 max-w-md">
          Platform settings and API key configurations are restricted by system administrators. Contact your SOC lead to apply changes to threat intelligence sync intervals.
        </p>
      </div>
    </div>
  );
}
