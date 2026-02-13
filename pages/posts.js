import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Posts() {
  const [copied, setCopied] = useState(null)

  const posts = [
    {
      time: '5:50 AM - Feb 13, 2026',
      category: 'TARIFFS',
      tickers: 'TRUMP STEEL',
      content: 'Trump planning to scale back some tariffs on steel and aluminium goods, FT reports. Trump hit imports with tariffs up to 50% last year. Latest softening comes amid voter anxiety about affordability. Markets reacting positively to potential relief.'
    },
    {
      time: '5:50 AM - Feb 13, 2026',
      category: 'TARIFFS',
      tickers: 'USMCA',
      content: 'Trump weighing quitting USMCA as tariffs face House rebuke. House voting on resolution to stop tariffs on Canada including 35% on steel, aluminum, copper and 25% on non-US cars. Six Republicans joined Democrats in backing rescission measure.'
    },
    {
      time: '5:50 AM - Feb 13, 2026',
      category: 'TRADE',
      tickers: 'TARIFFS M&A',
      content: 'Wells Fargo says Trump steel tariffs will fuel US metals M&A activity this year. Tariffs driving consolidation as foreign producers face pricing pressure. Domestic steel names potentially beneficiaries of policy shift.'
    },
    {
      time: '5:50 AM - Feb 13, 2026',
      category: 'ECONOMY',
      tickers: 'NY FED TARIFFS',
      content: 'New York Fed confirms US companies and consumers bearing tariff costs despite Trump claims otherwise. Research validates that domestic price increases passed to buyers. Inflation pressures persisting from trade policies.'
    },
    {
      time: '5:50 AM - Feb 13, 2026',
      category: 'RECIPROCAL',
      tickers: 'TRADE',
      content: 'Trump announcing plans to impose "reciprocal tariffs" on all countries with trade barriers against US in April. Wave of diplomatic outreach follows. Analysts expressing confusion over administration tariff strategies and openness to negotiation.'
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
