'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Shield, LayoutDashboard, Activity, Search, AlertOctagon, Settings, Database, Crosshair } from 'lucide-react';

const navItems = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Investigations', href: '/investigations', icon: Search },
  { name: 'Alerts', href: '/alerts', icon: AlertOctagon },
  { name: 'Network Telemetry', href: '/telemetry', icon: Activity },
  { name: 'Threat Intel', href: '/intelligence', icon: Crosshair },
  { name: 'Data Management', href: '/data', icon: Database },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 glass-panel border-r border-t-0 border-b-0 border-l-0 flex flex-col h-full flex-shrink-0 z-20">
      <div className="h-16 flex items-center px-6 border-b border-[#38bdf8]/20">
        <Shield className="w-8 h-8 text-[#38bdf8] mr-3 animate-glow" />
        <span className="font-bold text-lg tracking-wide bg-clip-text text-transparent bg-gradient-to-r from-[#38bdf8] to-[#8b5cf6]">
          CYBER SENTINEL
        </span>
      </div>
      
      <div className="flex-1 py-6 px-3 overflow-y-auto">
        <div className="text-xs uppercase text-slate-500 font-semibold mb-4 px-3 tracking-wider">
          Main Navigation
        </div>
        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname?.startsWith(`${item.href}/`) && item.href !== '/';
            
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center px-3 py-2.5 rounded-lg transition-all duration-200 group relative ${
                  isActive 
                    ? 'bg-[#38bdf8]/10 text-[#38bdf8]' 
                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`}
              >
                {isActive && (
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#38bdf8] rounded-r-md mask-radial-gradient"></div>
                )}
                <Icon className={`w-5 h-5 mr-3 ${isActive ? 'text-[#38bdf8]' : 'text-slate-500 group-hover:text-slate-300 transition-colors'}`} />
                <span className="font-medium text-sm">{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="p-4 border-t border-[#38bdf8]/10">
        <div className="bg-slate-900 rounded-lg p-3 flex items-center border border-slate-800">
          <div className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></div>
          <div className="text-xs text-slate-400">
            Engine: <span className="text-slate-200 shadow-glow">Online</span>
          </div>
        </div>
      </div>
    </div>
  );
}
