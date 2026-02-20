import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Dashboard() {
  const [showSettings, setShowSettings] = useState(false)

  return (
    <Layout title="Dashboard | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">Dashboard</h1>
        <p className="text-slate-400 mt-2">Braxton Helios - Agent System Status</p>
      </header>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="card p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-green-500">●</span>
            <h3 className="font-semibold">System Status</h3>
          </div>
          <p className="text-slate-400">All systems operational</p>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-orange-500">●</span>
            <h3 className="font-semibold">Active Agents</h3>
          </div>
          <p className="text-slate-400">Chief of Staff: Online</p>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-blue-500">●</span>
            <h3 className="font-semibold">Last Sync</h3>
          </div>
          <p className="text-slate-400">{new Date().toLocaleTimeString()}</p>
        </div>
      </div>

      {/* Heartbeat Schedule */}
      <div className="card p-6 mb-8">
        <h2 className="text-xl font-bold text-orange-400 mb-4">Heartbeat Schedule</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-semibold text-green-400 mb-2">Weekdays</h3>
            <ul className="space-y-1 text-slate-300 text-sm">
              <li>5:50 AM - Morning settlement letter, posts</li>
              <li>11:22 AM - Midday content, market update</li>
              <li>4:55 PM - End-of-day wrap, after-hours preview</li>
              <li>8:22 PM - Evening news scan, emails</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-green-400 mb-2">Weekends</h3>
            <ul className="space-y-1 text-slate-300 text-sm">
              <li>1:28 PM - Weekend content generation</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <a href="/hierarchy" className="card p-4 hover:bg-slate-700/50 transition-colors">
          <h3 className="font-semibold text-orange-400 mb-2">Hierarchy</h3>
          <p className="text-xs text-slate-500">Agent structure and roles</p>
        </a>
        
        <a href="/tasks" className="card p-4 hover:bg-slate-700/50 transition-colors">
          <h3 className="font-semibold text-orange-400 mb-2">Tasks</h3>
          <p className="text-xs text-slate-500">Track and manage tasks</p>
        </a>
        
        <a href="/tools" className="card p-4 hover:bg-slate-700/50 transition-colors">
          <h3 className="font-semibold text-orange-400 mb-2">Tools</h3>
          <p className="text-xs text-slate-500">Configuration and tools</p>
        </a>
        
        <a href="/settings" className="card p-4 hover:bg-slate-700/50 transition-colors">
          <h3 className="font-semibold text-orange-400 mb-2">Settings</h3>
          <p className="text-xs text-slate-500">System configuration</p>
        </a>
      </div>
    </Layout>
  )
}
