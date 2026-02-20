import Head from 'next/head'
import Layout from '../components/Layout'

export default function Tools() {
  const tools = {
    trading: [
      { name: 'Benzinga', description: 'News, alerts, market data' },
      { name: 'Trade Ideas', description: 'Stock scanning, alerts, patterns' },
      { name: 'Yahoo Finance', description: 'Stock quotes, earnings calendar' },
    ],
    ai: [
      { name: 'OpenRouter', description: 'Model routing (MiniMax, Sonnet, Opus)' },
      { name: 'Perplexity', description: 'Research subagent' },
    ],
    social: [
      { name: 'X/Twitter', description: '@AlertsAndNews (6.4K followers)' },
      { name: 'StockTwits', description: 'AlertsAndNews (26.5K followers)' },
    ],
    news: [
      { name: 'Brave API', description: 'Web search' },
      { name: 'Bloomberg', description: 'Market news' },
      { name: 'Reuters', description: 'Breaking news' },
      { name: 'CNBC', description: 'Market updates' },
    ],
  }

  return (
    <Layout title="Tools | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">Tools</h1>
        <p className="text-slate-400 mt-2">Configured tools and integrations</p>
      </header>

      <div className="grid gap-6">
        {/* Trading Tools */}
        <div className="card p-6">
          <h2 className="text-xl font-bold text-green-400 mb-4">Trading</h2>
          <div className="grid gap-3">
            {tools.trading.map((tool, idx) => (
              <div key={idx} className="p-3 bg-slate-800/50 rounded-lg">
                <h3 className="font-medium text-orange-300">{tool.name}</h3>
                <p className="text-sm text-slate-400">{tool.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* AI Models */}
        <div className="card p-6">
          <h2 className="text-xl font-bold text-cyan-400 mb-4">AI Models</h2>
          <div className="grid gap-3">
            {tools.ai.map((tool, idx) => (
              <div key={idx} className="p-3 bg-slate-800/50 rounded-lg">
                <h3 className="font-medium text-orange-300">{tool.name}</h3>
                <p className="text-sm text-slate-400">{tool.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Social Media */}
        <div className="card p-6">
          <h2 className="text-xl font-bold text-yellow-400 mb-4">Social Media</h2>
          <div className="grid gap-3">
            {tools.social.map((tool, idx) => (
              <div key={idx} className="p-3 bg-slate-800/50 rounded-lg">
                <h3 className="font-medium text-orange-300">{tool.name}</h3>
                <p className="text-sm text-slate-400">{tool.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* News Sources */}
        <div className="card p-6">
          <h2 className="text-xl font-bold text-red-400 mb-4">News Sources</h2>
          <div className="grid gap-3">
            {tools.news.map((tool, idx) => (
              <div key={idx} className="p-3 bg-slate-800/50 rounded-lg">
                <h3 className="font-medium text-orange-300">{tool.name}</h3>
                <p className="text-sm text-slate-400">{tool.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  )
}
