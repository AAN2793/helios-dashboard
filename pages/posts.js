import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Posts() {
  const [copied, setCopied] = useState(null)

  const posts = [
    {
      time: '11:30 AM - Feb 12, 2026',
      category: 'HEDGE FUNDS',
      tickers: 'SOFTWARE',
      content: 'Hedge funds made $24 billion shorting software stocks in 2026 so far, and they are increasing the bet, per CNBC. Software wipeout continues.'
    },
    {
      time: '11:30 AM - Feb 12, 2026',
      category: 'SECTOR',
      tickers: 'XLE',
      content: 'Energy entering rotational bull market, BofA says. XLE ETF outperformed S&P 500 by 13% in January. Mid-cap energy names (DVN, CTRA, OVV, CRC) more attractive than large-cap.'
    },
    {
      time: '11:30 AM - Feb 12, 2026',
      category: 'AI',
      tickers: 'MSFT AI',
      content: 'Microsoft AI CEO Mustafa Suleyman: Most accountant, lawyer and professional tasks fully automated by AI within 12-18 months. Major disruption ahead.'
    },
    {
      time: '11:30 AM - Feb 12, 2026',
      category: 'CRYPTO',
      tickers: 'BTC ETH',
      content: 'Bitcoin down 50% from October highs. Wolfe Research warns average 75% drawdowns in past cycles could push BTC to $30K. Standard Chartered cuts target to $100K.'
    },
    {
      time: '11:30 AM - Feb 12, 2026',
      category: 'MACRO',
      tickers: 'HOUSING',
      content: 'US Existing Home Sales -8.4% to 3.91M rate (est 4.15M). Median home price +0.9% YoY to $396,800. Housing market continues to slow.'
    },
    {
      time: '11:30 AM - Feb 12, 2026',
      category: 'AUTONOMOUS',
      tickers: 'GOOGL WAYMO',
      content: 'Waymo targets 1 million weekly rides by 2026, up from 400K now. Planning 20+ city expansions this year. International launch in London, Tokyo next.'
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
