import Head from 'next/head'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { useState, useEffect } from 'react'

function getMSTTime() {
  const now = new Date()
  const mstOffset = -7 * 60 // MST is UTC-7
  const utc = now.getTime() + now.getTimezoneOffset() * 60 * 1000
  return new Date(utc + mstOffset * 60 * 1000)
}

function formatTime(date) {
  return date.toLocaleTimeString('en-US', { 
    hour: 'numeric', 
    minute: '2-digit', 
    hour12: true 
  })
}

export default function Layout({ children, title = 'Braxton Helios' }) {
  const router = useRouter()
  const [currentTime, setCurrentTime] = useState('')
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  useEffect(() => {
    const updateTime = () => {
      setCurrentTime(formatTime(getMSTTime()))
    }
    updateTime()
    const interval = setInterval(updateTime, 1000)
    return () => clearInterval(interval)
  }, [])

  const navItems = [
    { name: 'Dashboard', path: '/', emoji: '◈' },
    { name: 'Hierarchy', path: '/hierarchy', emoji: '◎' },
    { name: 'Posts', path: '/posts', emoji: '◉' },
    { name: 'Tom Feed', path: '/tom-feed', emoji: '◐' },
    { name: 'AI Posts', path: '/generated-posts', emoji: '✦' },
    { name: 'Tasks', path: '/tasks', emoji: '○' },
    { name: 'Trading Journal', path: '/trading-journal', emoji: '📊' },
    { name: 'Tools', path: '/tools', emoji: '◇' },
    { name: 'Settings', path: '/settings', emoji: '◇' },
  ]

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200">
      <Head>
        <title>{title} | Braxton Helios</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Sidebar */}
      <aside className={`fixed left-0 top-0 h-full bg-slate-800/50 backdrop-blur-sm border-r border-slate-700 transition-all duration-300 ${isSidebarOpen ? 'w-64' : 'w-16'}`}>
        <div className="p-4 border-b border-slate-700">
          <div className="flex items-center justify-between">
            {isSidebarOpen && (
              <h1 className="text-xl font-bold text-orange-500">Helios</h1>
            )}
            <button 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
            >
              <span className="text-slate-400">{isSidebarOpen ? '◀' : '▶'}</span>
            </button>
          </div>
          {isSidebarOpen && (
            <p className="text-xs text-slate-500 mt-2">Braxton Helios Dashboard</p>
          )}
        </div>

        {/* MST Clock */}
        <div className="p-4 border-b border-slate-700">
          <div className="flex items-center gap-2">
            <span className="text-green-500">●</span>
            {isSidebarOpen && (
              <span className="text-sm text-slate-400">MST: {currentTime}</span>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-2">
          {navItems.map((item) => (
            <Link
              key={item.path}
              href={item.path}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors mb-1 ${
                router.pathname === item.path 
                  ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' 
                  : 'hover:bg-slate-700/50 text-slate-400'
              }`}
            >
              <span>{item.emoji}</span>
              {isSidebarOpen && <span>{item.name}</span>}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className={`transition-all duration-300 ${isSidebarOpen ? 'ml-64' : 'ml-16'}`}>
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  )
}
