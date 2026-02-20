import Head from 'next/head'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'

export default function Tom() {
  const [feed, setFeed] = useState([])
  const [lastUpdated, setLastUpdated] = useState(null)
  const [loading, setLoading] = useState(false)

  // Load feed from Tom's report file
  useEffect(() => {
    loadTomFeed()
  }, [])

  const loadTomFeed = async () => {
    setLoading(true)
    try {
      const response = await fetch('/tom-feed.json')
      if (response.ok) {
        const data = await response.json()
        setFeed(data.feed || [])
        setLastUpdated(data.timestamp || null)
      }
    } catch (e) {
      console.log('No feed file yet')
    }
    setLoading(false)
  }

  const formatTime = (isoString) => {
    if (!isoString) return ''
    const date = new Date(isoString)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })
  }

  const categories = {
    'Breaking News': { color: 'text-red-400', border: 'border-red-500' },
    'Unusual Options': { color: 'text-yellow-400', border: 'border-yellow-500' },
    'Stock Alerts': { color: 'text-green-400', border: 'border-green-500' },
  }

  return (
    <Layout title="Tom Feed | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">Tom Feed</h1>
        <p className="text-slate-400 mt-2">Raw Twitter data - what Tom is seeing</p>
      </header>

      <div className="flex justify-between items-center mb-6">
        <div className="text-sm text-slate-400">
          {lastUpdated && (
            <span>Last updated: {formatTime(lastUpdated)}</span>
          )}
        </div>
        <button
          onClick={loadTomFeed}
          disabled={loading}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            loading 
              ? 'bg-slate-700 text-slate-500' 
              : 'bg-orange-500/20 text-orange-400 hover:bg-orange-500/30'
          }`}
        >
          {loading ? 'Loading...' : 'Refresh Feed'}
        </button>
      </div>

      {feed.length === 0 ? (
        <div className="card p-8 text-center">
          <p className="text-slate-400">No feed data yet. Tom runs at:</p>
          <div className="mt-4 space-y-2 text-sm">
            <p><span className="text-slate-500">Weekdays:</span> 5:40 AM, 11:12 AM, 4:45 PM, 8:12 PM</p>
            <p><span className="text-slate-500">Weekends:</span> 1:18 PM</p>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {feed.map((item, idx) => (
            <div key={idx} className={`card p-4 border-l-4 ${categories[item.category]?.border || 'border-slate-500'}`}>
              <div className="flex justify-between items-start mb-2">
                <span className={`text-xs uppercase tracking-wide ${categories[item.category]?.color || 'text-slate-400'}`}>
                  {item.category}
                </span>
                <span className="text-xs text-slate-500">{item.author}</span>
              </div>
              <div className="text-slate-300 text-sm mb-2">{item.text}</div>
              <div className="flex gap-4 text-xs text-slate-500">
                <span>{item.time}</span>
                {item.rt > 0 && <span>RT: {item.rt}</span>}
                {item.likes > 0 && <span>Likes: {item.likes}</span>}
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  )
}
