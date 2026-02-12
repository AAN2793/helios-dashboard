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
      content: 'Silver crashed 10% in less than 30 minutes, marking one of the fastest declines in precious metals this year. The flash crash overwhelmed buyers during thin liquidity hours and caught algo traders flatfooted. Silver miners including $SLV and $PAAS may face continued pressure if gold follows.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'TECH',
      tickers: 'AAPL',
      content: 'Apple $AAPL dropped 5% today as tech weakness continues spreading across the sector. The move comes amid broader rotation away from mega-cap tech names as investors digest Fed signals and AI disruption concerns. Key support levels being tested.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'AI',
      tickers: 'GOOGL',
      content: 'Google $GOOGL updated Gemini 3 Deep Think to accelerate modern science, research and engineering capabilities. The move signals continued AI arms race among tech giants. Investors watching closely for commercial applications and competitive positioning.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'AI',
      tickers: 'MSFT AI',
      content: 'Microsoft AI CEO Mustafa Suleyman warned most white collar tasks will be fully automated by AI within 12-18 months. The bold prediction highlights massive disruption ahead for professional services sectors. Labor markets may face significant restructuring.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'GEOPOLITICS',
      tickers: 'RUBLE USD',
      content: 'Russia considering return to dollar-based financial system per Kremlin memo, signaling potential economic partnership with Trump administration. The move would reverse years of de-dollarization efforts and could reshape global finance. Western officials remain skeptical but monitoring closely.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'MARKET',
      tickers: 'DIA',
      content: 'Dow fell below 50,000 for the first time this week as market sentiment turns cautious. The psychological level breach signals growing investor uncertainty amid rate cut timing and geopolitical headlines. Key support being tested.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'REAL ESTATE',
      tickers: 'WALDORF',
      content: 'Chinese owners of NYC iconic Waldorf Astoria preparing to sell the property just months after its multibillion-dollar overhaul reopened. The sale could test the strength of luxury hotel markets and Chinese capital flows into US real estate. Source: WSJ.'
    },
    {
      time: '11:13 AM - Feb 12, 2026',
      category: 'CONSUMER',
      tickers: 'GEN Z',
      content: 'Gen Z and millennials swimming in student debt may never own homes, yet splurging on gut-healthy juices and rotisserie chickens. The spending pattern highlights generational wealth divide and consumer sector opportunities. Food stocks benefiting from premium positioning.'
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
