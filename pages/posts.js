import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Posts() {
  const [copied, setCopied] = useState(null)

  const posts = [
    {
      time: '4:45 PM - Feb 12, 2026',
      category: 'TECH',
      tickers: 'AAPL',
      content: 'Apple $AAPL suffered its worst single-day decline since April 2025, leading tech sector retreat. The slump reflects growing concerns about consumer spending in premium electronics. Tech names broadly under pressure as investors rotate away from mega-cap growth.'
    },
    {
      time: '4:45 PM - Feb 12, 2026',
      category: 'INSTITUTIONAL',
      tickers: 'FISHER',
      content: 'Fisher Investments ($298.7B AUM) filed Q4 portfolio updates, maintaining diversified equity exposure with notable shifts in technology and healthcare sectors. Big money continues repositioning for 2026 market conditions.'
    },
    {
      time: '4:45 PM - Feb 12, 2026',
      category: 'INSTITUTIONAL',
      tickers: 'SOUND SHORE',
      content: 'Sound Shore Management ($3.1B AUM) realigned positions, increasing cash positions while selectively adding to quality growth names. Institutional caution evident as money managers hedge near-term uncertainty.'
    },
    {
      time: '4:45 PM - Feb 12, 2026',
      category: 'INSTITUTIONAL',
      tickers: 'EGERTON',
      content: 'Egerton Capital ($9.2B AUM) under John Armitage made targeted adjustments to its long-short equity book. Active managers positioning defensively while maintaining quality exposure.'
    },
    {
      time: '4:45 PM - Feb 12, 2026',
      category: 'POLITICS',
      tickers: 'GABBARD KUSHNER',
      content: 'Whistleblower complaint emerged involving Tulsi Gabbard and Jared Kushner. Classified complaint filed with intelligence inspectors general contains allegations related to foreign conversation intercepted last spring. Congressional committees reviewing.'
    },
    {
      time: '4:45 PM - Feb 12, 2026',
      category: 'OPTIONS',
      tickers: 'SEMIS SOFTWARE',
      content: 'Elevated put volumes in semiconductor and software names suggest increased hedging behavior. Options market indicating institutional concern about near-term downside in tech sectors.'
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
