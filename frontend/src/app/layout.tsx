import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata: Metadata = {
  title: 'AI Cyber Sentinel',
  description: 'AI-assisted threat intelligence & investigation platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} antialiased`} suppressHydrationWarning>
        <div className="flex h-screen overflow-hidden text-slate-100 bg-[#020617]">
          <Sidebar />
          <div className="flex flex-col flex-1 overflow-hidden relative z-10 w-full">
            <Header />
            <main className="flex-1 overflow-auto p-4 md:p-6 lg:p-8">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
