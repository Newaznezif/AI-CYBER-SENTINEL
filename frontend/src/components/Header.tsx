'use client';

import { Bell, Search, User } from 'lucide-react';

export default function Header() {
  return (
    <header className="h-16 glass-panel border-b border-l-0 border-r-0 border-t-0 flex items-center justify-between px-6 z-10 shrink-0">
      <div className="flex-1 max-w-xl hidden md:flex items-center bg-slate-900 border border-slate-700/50 rounded-lg px-3 py-1.5 focus-within:border-[#38bdf8] focus-within:shadow-[0_0_10px_rgba(56,189,248,0.2)] transition-all">
        <Search className="w-4 h-4 text-slate-500 mr-2" />
        <input 
          type="text" 
          placeholder="Search indicators, alerts, or queries..." 
          className="bg-transparent border-none outline-none text-sm text-slate-200 placeholder:text-slate-500 w-full"
        />
        <div className="ml-2 flex gap-1">
          <kbd className="hidden lg:inline-flex items-center justify-center px-2 py-0.5 text-xs font-semibold text-slate-400 bg-slate-800 border border-slate-700 rounded-md">Ctrl</kbd>
          <kbd className="hidden lg:inline-flex items-center justify-center px-2 py-0.5 text-xs font-semibold text-slate-400 bg-slate-800 border border-slate-700 rounded-md">K</kbd>
        </div>
      </div>
      
      <div className="flex items-center gap-4 ml-auto">
        <button className="relative p-2 text-slate-400 hover:text-slate-200 transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-2 w-2 h-2 bg-red-500 rounded-full border border-[#020617]"></span>
        </button>
        
        <div className="w-px h-6 bg-slate-800 mx-2"></div>
        
        <div className="flex items-center gap-3 cursor-pointer hover:bg-slate-800/50 p-1.5 rounded-lg transition-colors">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#38bdf8] to-[#8b5cf6] flex items-center justify-center text-white font-bold text-sm shadow-[0_0_10px_rgba(139,92,246,0.3)]">
            OP
          </div>
          <div className="hidden sm:block">
            <div className="text-sm font-medium text-slate-200">Operator One</div>
            <div className="text-xs text-slate-500">Tier 2 Analyst</div>
          </div>
        </div>
      </div>
    </header>
  );
}
