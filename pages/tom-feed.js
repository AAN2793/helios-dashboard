import Head from 'next/head'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'

export default function TomFeed() {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [accounts, setAccounts] = useState({
    'Breaking News': ['@wallstengine', '@StockMKTNewz', '@DeItaone', '@OracleNYSE', '@TheInsiderPaper'],
    'Unusual Options': ['@unusual_whales', '@CheddarFlow'],
    'Stock Alerts': ['@PlayBookTrades']
  })

  useEffect(() => {
    fetchReport()
  }, [])

  const fetchReport = async () => {
    try {
      const res = await fetch('/api/tom-report')
      if (!res.ok) throw new Error('Failed to fetch')
      const data = await res.json()
      setReport(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const refreshFeed = () => {
    setLoading(true)
    fetchReport()
  }

  return (
    <Layout title="Tom Feed | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">Twitter Tom Feed</h1>
        <p className="text-slate-400 mt-2">Real-time Twitter monitoring feed</p>
      </header>

      <div className="mb-6 flex gap-4">
        <button
          onClick={refreshFeed}
          className="px-4 py-2 bg-cyan-700 text-cyan-100 rounded hover:bg-cyan-600"
        >
          Refresh Feed
        </button>
        <a
          href="/settings"
          className="px-4 py-2 bg-slate-700 text-slate-200 rounded hover:bg-slate-600"
        >
          Manage Sources
        </a>
      </div>

      {loading && <div className="text-cyan-400">Loading Tom's feed...</div>}
      {error && <div className="text-red-400">Error: {error}</div>}

      {report && (
        <div className="space-y-6">
          <div className="bg-slate-800 p-4 rounded">
            <span className="text-slate-400">Last Scan:</span>
            <span className="text-cyan-400 ml-2">{report.generated}</span>
          </div>

          {Object.entries(report.categories || {}).map(([category, tweets]) => (
            <div key={category} className="bg-slate-900 rounded-lg overflow-hidden">
              <div className="bg-slate-800 px-4 py-2 border-b border-slate-700">
                <h2 className="text-lg font-semibold text-cyan-400">{category}</h2>
              </div>
              <div className="divide-y divide-slate-800">
                {(tweets || []).map((tweet, idx) => (
                  <div key={idx} className="p-4 hover:bg-slate-800/50">
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-orange-400 font-mono">{tweet.author}</span>
                      <span className="text-slate-500 text-sm">{tweet.created_at}</span>
                    </div>
                    <p className="text-slate-200 mb-2">{tweet.text}</p>
                    <div className="flex gap-4 text-xs text-slate-500">
                      <span>RT: {tweet.retweet_count}</span>
                      <span>Likes: {tweet.like_count}</span>
                    </div>
                  </div>
                ))}
                {(!tweets || tweets.length === 0) && (
                  <div className="p-4 text-slate-500">No new tweets in this category</div>
                )}
              </div>
            </div>
          ))}

          {(!report.categories || Object.keys(report.categories).length === 0) && (
            <div className="text-slate-400">No new tweets from this scan</div>
          )}
        </div>
      )}
    </Layout>
  )
}
