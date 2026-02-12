import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Tasks() {
  const [tasks, setTasks] = useState([
    { id: 1, text: 'Morning research and settlement letter', time: '5:50 AM', done: false },
    { id: 2, text: 'Midday content generation', time: '11:22 AM', done: false },
    { id: 3, text: 'End-of-day wrap and after-hours preview', time: '4:55 PM', done: false },
    { id: 4, text: 'Evening news scan and emails', time: '8:22 PM', done: false },
    { id: 5, text: 'Twitter Tom scan - Breaking News accounts', time: '5:40 AM', done: true },
    { id: 6, text: 'Twitter Tom scan - Unusual Options', time: '11:12 AM', done: true },
    { id: 7, text: 'Twitter Tom scan - Stock Alerts', time: '4:45 PM', done: true },
  ])

  const toggleTask = (id) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, done: !t.done } : t))
  }

  return (
    <Layout title="Tasks | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">Tasks</h1>
        <p className="text-slate-400 mt-2">Daily schedule and to-dos</p>
      </header>

      <div className="grid gap-6">
        {/* Today's Schedule */}
        <div className="card p-6">
          <h2 className="text-xl font-bold text-green-400 mb-4">Today - Feb 11, 2026</h2>
          <div className="space-y-3">
            {tasks.filter(t => t.id <= 4).map(task => (
              <div key={task.id} className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg">
                <button
                  onClick={() => toggleTask(task.id)}
                  className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                    task.done 
                      ? 'bg-green-500 border-green-500' 
                      : 'border-slate-500 hover:border-green-400'
                  }`}
                >
                  {task.done && <span className="text-slate-900 text-xs">✓</span>}
                </button>
                <div className="flex-1">
                  <span className="text-xs text-slate-500">{task.time}</span>
                  <p className={`text-slate-200 ${task.done ? 'line-through opacity-50' : ''}`}>
                    {task.text}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Tom Scans */}
        <div className="card p-6">
          <h2 className="text-xl font-bold text-cyan-400 mb-4">Twitter Tom Scans</h2>
          <div className="space-y-3">
            {tasks.filter(t => t.id > 4).map(task => (
              <div key={task.id} className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg">
                <button
                  onClick={() => toggleTask(task.id)}
                  className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                    task.done 
                      ? 'bg-green-500 border-green-500' 
                      : 'border-slate-500 hover:border-green-400'
                  }`}
                >
                  {task.done && <span className="text-slate-900 text-xs">✓</span>}
                </button>
                <div className="flex-1">
                  <span className="text-xs text-slate-500">{task.time}</span>
                  <p className={`text-slate-200 ${task.done ? 'line-through opacity-50' : ''}`}>
                    {task.text}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  )
}
