import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Posts() {
  const [copied, setCopied] = useState(null)

  const posts = [
    {
      time: '8:12 PM - Feb 12, 2026',
      category: 'TRADE',
      tickers: 'US TAIWAN',
      content: 'US and Taiwan signed new trade deal cutting US tariff on most Taiwanese exports to 15%. Taiwan removing 99% of tariff barriers on US goods and committing to $84B+ of US purchases including energy and aviation. Major geopolitical development.'
    },
    {
      time: '8:12 PM - Feb 12, 2026',
      category: 'DIVIDENDS',
      tickers: 'META',
      content: 'Meta $META declared quarterly dividend of $0.525 per share. Mark Zuckerberg owns 342.6M shares, meaning $180M dividend check. Regular payouts signal mature company transition and shareholder return focus.'
    },
    {
      time: '8:12 PM - Feb 12, 2026',
      category: 'FOREX',
      tickers: 'USD JPY',
      content: 'Japanese yen on track for biggest weekly gain since November 2024. The move reflects shifting currency flows and Bank of Japan policy expectations. Dollar weakness supporting yen strength.'
    },
    {
      time: '8:12 PM - Feb 12, 2026',
      category: 'MOVERS',
      tickers: 'RIME',
      content: 'RIME $RIME closed at $1.48 off $1.05 reclaim and holds. $1.60++ target for 4H expansion. Chinese names running across markets may distribute volume. Take profits and raise stops.'
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
