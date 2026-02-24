import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import businessIdeas from '../data/business-ideas'

export const dynamic = 'force-dynamic'

export default function Ideas() {
  const [expanded, setExpanded] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [favorites, setFavorites] = useState([])
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false)
  const [sortBy, setSortBy] = useState('id') // id, market, revenue

  // Load favorites from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('helios-ideas-favorites')
    if (saved) {
      try {
        setFavorites(JSON.parse(saved))
      } catch {
        localStorage.removeItem('helios-ideas-favorites')
      }
    }
  }, [])

  // Save favorites to localStorage when changed
  useEffect(() => {
    localStorage.setItem('helios-ideas-favorites', JSON.stringify(favorites))
  }, [favorites])

  const toggleFavorite = (id) => {
    setFavorites(prev => 
      prev.includes(id) ? prev.filter(f => f !== id) : [...prev, id]
    )
  }

  const exportFavorites = () => {
    const favIdeas = businessIdeas.filter(i => favorites.includes(i.id))
    const csv = [
      ['ID', 'Title', 'Market', 'Growth', 'Risk', 'Year 1 Revenue', 'Year 3 Revenue', 'Execution Paths'].join(','),
      ...favIdeas.map(i => [
        i.id,
        `"${i.title}"`,
        `"${i.market}"`,
        `"${i.marketGrowth}"`,
        `"${i.risk}"`,
        `"${i.revenueProjection.year1}"`,
        `"${i.revenueProjection.year3}"`,
        `"${i.execution.join(' | ')}"`
      ].join(','))
    ].join('\n')
    
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `helios-ideas-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  const filteredIdeas = businessIdeas
    .filter(i => {
      const matchesSearch = i.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        i.tagline.toLowerCase().includes(searchTerm.toLowerCase())
      if (showFavoritesOnly) return matchesSearch && favorites.includes(i.id)
      return matchesSearch
    })
    .sort((a, b) => {
      if (sortBy === 'market') {
        // Simple numeric extraction for comparison
        const aNum = parseFloat(a.market.replace(/[^0-9.]/g, '')) || 0
        const bNum = parseFloat(b.market.replace(/[^0-9.]/g, '')) || 0
        return bNum - aNum
      }
      if (sortBy === 'revenue') {
        const aNum = parseFloat(a.revenueProjection.year3.replace(/[^0-9]/g, '')) || 0
        const bNum = parseFloat(b.revenueProjection.year3.replace(/[^0-9]/g, '')) || 0
        return bNum - aNum
      }
      return a.id - b.id
    })

  return (
    <Layout title="Business Ideas | Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-cyan-500">💡 22 Business Ideas</h1>
        <p className="text-slate-400 mt-2">22 ways to make $1M - detailed analysis with execution paths</p>
      </header>

      {/* Tools */}
      <div className="mb-6 flex flex-wrap gap-3 items-center">
        <input
          type="text"
          placeholder="Search ideas..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-cyan-500 w-64"
        />
        
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-cyan-500"
        >
          <option value="id">Sort by ID</option>
          <option value="market">Sort by Market Size</option>
          <option value="revenue">Sort by Year 3 Revenue</option>
        </select>

        <button
          onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            showFavoritesOnly 
              ? 'bg-yellow-600 text-white' 
              : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
          }`}
        >
          {showFavoritesOnly ? '★ All Favorites' : '☆ Favorites'} ({favorites.length})
        </button>

        {favorites.length > 0 && (
          <button
            onClick={exportFavorites}
            className="px-4 py-2 bg-green-800 text-green-100 rounded-lg text-sm hover:bg-green-700"
          >
            ↓ Export CSV
          </button>
        )}
      </div>

      {/* Stats */}
      <div className="mb-6 flex gap-4 text-sm">
        <span className="text-slate-400">Showing: <span className="text-white">{filteredIdeas.length}</span> / 22</span>
        {showFavoritesOnly && (
          <button 
            onClick={() => setShowFavoritesOnly(false)}
            className="text-cyan-400 hover:text-cyan-300 underline"
          >
            Clear filter
          </button>
        )}
      </div>

      {/* Grid */}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {filteredIdeas.map(idea => (
          <div 
            key={idea.id}
            onClick={() => setExpanded(expanded === idea.id ? null : idea.id)}
            className={`bg-slate-800 rounded-lg p-5 cursor-pointer border transition-all ${
              expanded === idea.id 
                ? 'border-cyan-500 ring-1 ring-cyan-500' 
                : favorites.includes(idea.id)
                ? 'border-yellow-600 hover:border-yellow-500'
                : 'border-slate-700 hover:border-slate-600'
            }`}
          >
            <div className="flex justify-between items-start mb-2">
              <span className="text-cyan-400 font-mono text-sm">#{idea.id}</span>
              <button
                onClick={(e) => { e.stopPropagation(); toggleFavorite(idea.id) }}
                className={`text-xl ${favorites.includes(idea.id) ? 'text-yellow-500' : 'text-slate-600 hover:text-yellow-600'}`}
              >
                {favorites.includes(idea.id) ? '★' : '☆'}
              </button>
            </div>
            
            <h3 className="text-lg font-bold text-white mb-1">{idea.title}</h3>
            <p className="text-slate-400 text-sm mb-3">{idea.tagline}</p>
            
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs text-green-400 bg-green-900/30 px-2 py-1 rounded">{idea.market}</span>
              <span className="text-xs text-blue-400 bg-blue-900/30 px-2 py-1 rounded">{idea.marketGrowth}</span>
              <span className="text-xs text-orange-400 bg-orange-900/30 px-2 py-1 rounded">{idea.risk}</span>
            </div>

            {!expanded && (
              <div className="mt-3 text-xs text-slate-500">
                Revenue: {idea.revenueProjection.year1} → {idea.revenueProjection.year3}
              </div>
            )}

            {expanded === idea.id && (
              <div className="mt-4 pt-4 border-t border-slate-700 space-y-4">
                {/* Startup Costs */}
                <div>
                  <h4 className="text-orange-400 text-sm font-bold mb-1">Startup Cost</h4>
                  <p className="text-slate-300 text-sm mb-1">
                    ${idea.startupCost.min.toLocaleString()} - ${idea.startupCost.max.toLocaleString()}
                  </p>
                  <ul className="text-xs text-slate-400 space-y-1 ml-2">
                    {idea.startupCost.breakdown.map((item, i) => (
                      <li key={i}>• {item}</li>
                    ))}
                  </ul>
                </div>

                {/* Pricing Models */}
                <div>
                  <h4 className="text-purple-400 text-sm font-bold mb-1">Pricing</h4>
                  <ul className="text-xs text-slate-300 space-y-1">
                    {idea.pricing.models.map((model, i) => (
                      <li key={i} className="flex gap-2">
                        <span className="text-purple-500">→</span> {model}
                      </li>
                    ))}
                  </ul>
                  <p className="text-xs text-slate-400 mt-1">Avg: {idea.pricing.avgClientValue}</p>
                </div>

                {/* Execution Paths */}
                <div>
                  <h4 className="text-cyan-400 text-sm font-bold mb-1">Execution Paths</h4>
                  <ul className="text-xs text-slate-300 space-y-1">
                    {idea.execution.map((path, i) => (
                      <li key={i} className="flex gap-2">
                        <span className="text-cyan-500">→</span> {path}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Go-to-Market */}
                <div>
                  <h4 className="text-green-400 text-sm font-bold mb-1">Go-to-Market</h4>
                  <ul className="text-xs text-slate-300 space-y-1">
                    {idea.gotoMarket.map((strategy, i) => (
                      <li key={i} className="flex gap-2">
                        <span className="text-green-500">→</span> {strategy}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Revenue Projections */}
                <div>
                  <h4 className="text-amber-400 text-sm font-bold mb-1">Revenue Projection</h4>
                  <div className="grid grid-cols-3 gap-2 text-center">
                    <div className="bg-slate-900/50 p-2 rounded">
                      <div className="text-xs text-slate-500">Year 1</div>
                      <div className="text-sm text-white font-bold">{idea.revenueProjection.year1}</div>
                    </div>
                    <div className="bg-slate-900/50 p-2 rounded">
                      <div className="text-xs text-slate-500">Year 2</div>
                      <div className="text-sm text-white font-bold">{idea.revenueProjection.year2}</div>
                    </div>
                    <div className="bg-slate-900/50 p-2 rounded">
                      <div className="text-xs text-slate-500">Year 3</div>
                      <div className="text-sm text-white font-bold">{idea.revenueProjection.year3}</div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </Layout>
  )
}
