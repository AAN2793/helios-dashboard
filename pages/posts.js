import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Posts() {
  const [copied, setCopied] = useState(null)

  const posts = [
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'FLASH CRASH',
      tickers: 'SILVER',
      content: 'Silver crashes 10% in less than 30 minutes. Major volatility event hitting precious metals. Quick move caught many off guard.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'TECH',
      tickers: 'AAPL',
      content: 'Apple $AAPL down 5% today. Tech weakness continues spreading across the sector. Market rotation away from mega-cap tech.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'AI',
      tickers: 'GOOGL',
      content: 'Google $GOOGL updates Gemini 3 Deep Think to accelerate modern science, research and engineering. AI arms race intensifies.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'AI',
      tickers: 'MSFT AI',
      content: 'Microsoft AI CEO Mustafa Suleyman: "Most white collar tasks fully automated by AI within 12-18 months." Major disruption ahead.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'GEOPOLITICS',
      tickers: 'RUBLE USD',
      content: 'Russia considering return to dollar-based financial system per Kremlin memo. Economic partnership pitch to Trump administration.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'MARKET',
      tickers: 'DIA',
      content: 'Dow below 50,000. Market sentiment turning cautious as major averages face resistance levels.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'REAL ESTATE',
      tickers: 'WALDORF',
      content: 'Chinese owners of NYC iconic Waldorf Astoria preparing to sell. Just months after multibillion-dollar overhaul. Source: WSJ.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'DEMOGRAPHICS',
      tickers: 'GEN Z',
      content: 'Gen Z and millennials swimming in student debt, may never own homes, but splurging on gut-healthy juices and rotisserie chickens. Source: WSJ.'
    },
  ]

  const copyToClipboard = (index, text) => {
    navigator.clipboard.writeText(text)
    setCopied(index)
    setTimeout(() => setCopied(null), 2000)
  }

  const getFullText = (post) => {
    return `${post.tickers}\n${post.content}`
  }

  return (
    <Layout title="Posts | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">Posts</h1>
        <p className="text-slate-400 mt-2">Market news posts - Copy/paste ready</p>
      </header>

      <div className="mb-4 text-sm text-slate-400">
        User does market moves. Helios does market news.
      </div>

      <div className="grid gap-4">
        {posts.map((post, idx) => (
          <div key={idx} className="card p-4">
            <div className="flex justify-between items-start mb-2">
              <div>
                <span className="text-xs text-cyan-400 uppercase tracking-wide">{post.category}</span>
                <span className="text-xs text-slate-500 ml-2">{post.time}</span>
              </div>
              <button
                onClick={() => copyToClipboard(idx, getFullText(post))}
                className={`px-3 py-1 text-xs rounded transition-colors ${
                  copied === idx 
                    ? 'bg-green-900 text-green-300' 
                    : 'bg-cyan-900 text-cyan-300 hover:bg-cyan-800'
                }`}
              >
                {copied === idx ? 'Copied!' : 'Copy'}
              </button>
            </div>
            <div className="font-bold text-orange-400 mb-2">{post.tickers}</div>
            <div className="text-slate-300 text-sm whitespace-pre-wrap">{post.content}</div>
          </div>
        ))}
      </div>
    </Layout>
  )
}
