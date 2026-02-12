import Head from 'next/head'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'

export default function Tasks() {
  const [tasks, setTasks] = useState([])
  const [newTask, setNewTask] = useState('')
  const [filter, setFilter] = useState('all') // all, active, done

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('helios-tasks')
    if (saved) {
      setTasks(JSON.parse(saved))
    } else {
      // Default tasks if nothing saved
      const defaults = [
        { id: 1, text: 'Morning research and settlement letter', time: '5:50 AM', done: false },
        { id: 2, text: 'Midday content generation', time: '11:22 AM', done: false },
        { id: 3, text: 'End-of-day wrap and after-hours preview', time: '4:55 PM', done: false },
        { id: 4, text: 'Evening news scan and emails', time: '8:22 PM', done: false },
        { id: 5, text: 'Twitter Tom scan - Breaking News', time: '5:40 AM', done: true },
        { id: 6, text: 'Twitter Tom scan - Unusual Options', time: '11:12 AM', done: true },
        { id: 7, text: 'Twitter Tom scan - Stock Alerts', time: '4:45 PM', done: true },
      ]
      setTasks(defaults)
    }
  }, [])

  // Save to localStorage on change
  useEffect(() => {
    if (tasks.length > 0) {
      localStorage.setItem('helios-tasks', JSON.stringify(tasks))
    }
  }, [tasks])

  const addTask = () => {
    if (!newTask.trim()) return
    const task = {
      id: Date.now(),
      text: newTask.trim(),
      time: '',
      done: false
    }
    setTasks([task, ...tasks])
    setNewTask('')
  }

  const toggleTask = (id) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, done: !t.done } : t))
  }

  const deleteTask = (id) => {
    setTasks(tasks.filter(t => t.id !== id))
  }

  const filteredTasks = tasks.filter(t => {
    if (filter === 'active') return !t.done
    if (filter === 'done') return t.done
    return true
  })

  const completedCount = tasks.filter(t => t.done).length
  const totalCount = tasks.length

  return (
    <Layout title="Tasks | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">Tasks</h1>
        <p className="text-slate-400 mt-2">
          {completedCount}/{totalCount} completed
        </p>
      </header>

      {/* Add Task */}
      <div className="card p-4 mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addTask()}
            placeholder="Add a new task..."
            className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-orange-500"
          />
          <button
            onClick={addTask}
            className="bg-orange-500/20 text-orange-400 px-4 py-2 rounded-lg hover:bg-orange-500/30 transition-colors"
          >
            Add
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-2 mb-4">
        {['all', 'active', 'done'].map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1 rounded-lg text-sm capitalize transition-colors ${
              filter === f 
                ? 'bg-orange-500/20 text-orange-400' 
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Task List */}
      <div className="space-y-2">
        {filteredTasks.length === 0 ? (
          <div className="card p-8 text-center text-slate-400">
            No {filter} tasks
          </div>
        ) : (
          filteredTasks.map(task => (
            <div 
              key={task.id} 
              className={`card p-4 flex items-center gap-3 ${
                task.done ? 'opacity-50' : ''
              }`}
            >
              <button
                onClick={() => toggleTask(task.id)}
                className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors flex-shrink-0 ${
                  task.done 
                    ? 'bg-green-500 border-green-500' 
                    : 'border-slate-500 hover:border-green-400'
                }`}
              >
                {task.done && <span className="text-slate-900 text-xs">✓</span>}
              </button>
              
              <div className="flex-1">
                <span className="text-xs text-slate-500">{task.time}</span>
                <p className={`text-slate-200 ${task.done ? 'line-through' : ''}`}>
                  {task.text}
                </p>
              </div>
              
              <button
                onClick={() => deleteTask(task.id)}
                className="text-slate-500 hover:text-red-400 px-2 py-1 rounded transition-colors"
                title="Delete task"
              >
                ×
              </button>
            </div>
          ))
        )}
      </div>

      {/* Clear All Done */}
      {tasks.some(t => t.done) && (
        <button
          onClick={() => setTasks(tasks.filter(t => !t.done))}
          className="mt-6 text-sm text-slate-500 hover:text-slate-400"
        >
          Clear completed
        </button>
      )}
    </Layout>
  )
}
