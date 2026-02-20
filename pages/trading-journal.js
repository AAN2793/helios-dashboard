import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function TradingJournal() {
  const [trades, setTrades] = useState([
    { id: 1, symbol: 'NVDA', type: 'BUY', price: 145.50, shares: 100, timestamp: '2026-02-12T09:30:00' },
    { id: 2, symbol: 'NVDA', type: 'SELL', price: 148.25, shares: 100, timestamp: '2026-02-12T10:45:00' },
    { id: 3, symbol: 'TSLA', type: 'BUY', price: 215.00, shares: 50, timestamp: '2026-02-12T11:15:00' },
    { id: 4, symbol: 'AAPL', type: 'BUY', price: 185.00, shares: 75, timestamp: '2026-02-12T14:30:00' },
  ])

  const [showAddForm, setShowAddForm] = useState(false)
  const [newTrade, setNewTrade] = useState({ symbol: '', type: 'BUY', price: '', shares: '' })

  const addTrade = () => {
    if (!newTrade.symbol || !newTrade.price || !newTrade.shares) return
    
    const trade = {
      id: Date.now(),
      symbol: newTrade.symbol.toUpperCase(),
      type: newTrade.type,
      price: parseFloat(newTrade.price),
      shares: parseInt(newTrade.shares),
      timestamp: new Date().toISOString()
    }
    
    setTrades([...trades, trade])
    setNewTrade({ symbol: '', type: 'BUY', price: '', shares: '' })
    setShowAddForm(false)
  }

  const deleteTrade = (id) => {
    setTrades(trades.filter(t => t.id !== id))
  }

  // Calculate P&L from trades
  const calculatePnL = () => {
    const symbolTrades = {}
    
    trades.forEach(trade => {
      if (!symbolTrades[trade.symbol]) {
        symbolTrades[trade.symbol] = { buys: [], sells: [] }
      }
      
      if (trade.type === 'BUY') {
        symbolTrades[trade.symbol].buys.push(trade)
      } else {
        symbolTrades[trade.symbol].sells.push(trade)
      }
    })

    const roundTrades = []
    
    Object.keys(symbolTrades).forEach(symbol => {
      const { buys, sells } = symbolTrades[symbol]
      
      // Match buys with sells
      let remainingBuys = [...buys]
      let remainingSells = [...sells]
      
      while (remainingBuys.length > 0 && remainingSells.length > 0) {
        const buy = remainingBuys[0]
        const sell = remainingSells[0]
        
        const pnl = (sell.price - buy.price) * Math.min(buy.shares, sell.shares)
        
        roundTrades.push({
          id: `${buy.id}-${sell.id}`,
          symbol,
          type: 'ROUND TRADE',
          entryPrice: buy.price,
          exitPrice: sell.price,
          shares: Math.min(buy.shares, sell.shares),
          pnl,
          timestamp: sell.timestamp
        })
        
        if (buy.shares > sell.shares) {
          remainingBuys[0] = { ...buy, shares: buy.shares - sell.shares }
          remainingSells.shift()
        } else if (sell.shares > buy.shares) {
          remainingSells[0] = { ...sell, shares: sell.shares - buy.shares }
          remainingBuys.shift()
        } else {
          remainingBuys.shift()
          remainingSells.shift()
        }
      }
    })

    return roundTrades.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
  }

  const roundTrades = calculatePnL()
  
  const totalPnL = roundTrades.reduce((sum, t) => sum + t.pnl, 0)
  const winCount = roundTrades.filter(t => t.pnl > 0).length
  const lossCount = roundTrades.filter(t => t.pnl < 0).length
  const totalTrades = roundTrades.length
  const winRate = totalTrades > 0 ? ((winCount / totalTrades) * 100).toFixed(1) : 0

  return (
    <Layout title="Trading Journal | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">Trading Journal</h1>
        <p className="text-slate-400 mt-2">Track your trades, calculate P&L, review performance</p>
      </header>

      {/* Summary Stats */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="card p-4">
          <div className="text-slate-400 text-sm">Total P&L</div>
          <div className={`text-2xl font-bold ${totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            ${totalPnL.toFixed(2)}
          </div>
        </div>
        <div className="card p-4">
          <div className="text-slate-400 text-sm">Win Rate</div>
          <div className="text-2xl font-bold text-cyan-400">{winRate}%</div>
        </div>
        <div className="card p-4">
          <div className="text-slate-400 text-sm">Wins</div>
          <div className="text-2xl font-bold text-green-400">{winCount}</div>
        </div>
        <div className="card p-4">
          <div className="text-slate-400 text-sm">Losses</div>
          <div className="text-2xl font-bold text-red-400">{lossCount}</div>
        </div>
      </div>

      {/* Add Trade Button */}
      <button
        onClick={() => setShowAddForm(!showAddForm)}
        className="mb-4 px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg"
      >
        {showAddForm ? 'Cancel' : '+ Add Trade'}
      </button>

      {/* Add Trade Form */}
      {showAddForm && (
        <div className="card p-4 mb-6">
          <div className="grid grid-cols-5 gap-4">
            <div>
              <label className="block text-slate-400 text-sm mb-1">Symbol</label>
              <input
                type="text"
                value={newTrade.symbol}
                onChange={(e) => setNewTrade({...newTrade, symbol: e.target.value})}
                placeholder="AAPL"
                className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white"
              />
            </div>
            <div>
              <label className="block text-slate-400 text-sm mb-1">Type</label>
              <select
                value={newTrade.type}
                onChange={(e) => setNewTrade({...newTrade, type: e.target.value})}
                className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white"
              >
                <option value="BUY">BUY</option>
                <option value="SELL">SELL</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-400 text-sm mb-1">Price</label>
              <input
                type="number"
                value={newTrade.price}
                onChange={(e) => setNewTrade({...newTrade, price: e.target.value})}
                placeholder="150.00"
                step="0.01"
                className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white"
              />
            </div>
            <div>
              <label className="block text-slate-400 text-sm mb-1">Shares</label>
              <input
                type="number"
                value={newTrade.shares}
                onChange={(e) => setNewTrade({...newTrade, shares: e.target.value})}
                placeholder="100"
                className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white"
              />
            </div>
            <div className="flex items-end">
              <button
                onClick={addTrade}
                className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Open Positions */}
      <div className="mb-8">
        <h2 className="text-xl font-bold text-cyan-400 mb-4">Open Positions</h2>
        <div className="card overflow-hidden">
          <table className="w-full">
            <thead className="bg-slate-800">
              <tr>
                <th className="text-left p-3 text-slate-400">Symbol</th>
                <th className="text-left p-3 text-slate-400">Type</th>
                <th className="text-right p-3 text-slate-400">Price</th>
                <th className="text-right p-3 text-slate-400">Shares</th>
                <th className="text-right p-3 text-slate-400">Value</th>
                <th className="text-right p-3 text-slate-400">Time</th>
                <th className="text-right p-3 text-slate-400"></th>
              </tr>
            </thead>
            <tbody>
              {trades.map(trade => (
                <tr key={trade.id} className="border-t border-slate-800">
                  <td className="p-3 font-bold text-orange-400">{trade.symbol}</td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded text-xs ${trade.type === 'BUY' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`}>
                      {trade.type}
                    </span>
                  </td>
                  <td className="p-3 text-right">${trade.price.toFixed(2)}</td>
                  <td className="p-3 text-right">{trade.shares}</td>
                  <td className="p-3 text-right">${(trade.price * trade.shares).toFixed(2)}</td>
                  <td className="p-3 text-right text-slate-500 text-sm">
                    {new Date(trade.timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
                  </td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => deleteTrade(trade.id)}
                      className="text-red-400 hover:text-red-300 text-sm"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Round Trades (Completed) */}
      <div>
        <h2 className="text-xl font-bold text-cyan-400 mb-4">Round Trades (P&L)</h2>
        <div className="card overflow-hidden">
          <table className="w-full">
            <thead className="bg-slate-800">
              <tr>
                <th className="text-left p-3 text-slate-400">Symbol</th>
                <th className="text-right p-3 text-slate-400">Entry</th>
                <th className="text-right p-3 text-slate-400">Exit</th>
                <th className="text-right p-3 text-slate-400">Shares</th>
                <th className="text-right p-3 text-slate-400">P&L</th>
                <th className="text-right p-3 text-slate-400">Time</th>
              </tr>
            </thead>
            <tbody>
              {roundTrades.map(trade => (
                <tr key={trade.id} className="border-t border-slate-800">
                  <td className="p-3 font-bold text-orange-400">{trade.symbol}</td>
                  <td className="p-3 text-right">${trade.entryPrice.toFixed(2)}</td>
                  <td className="p-3 text-right">${trade.exitPrice.toFixed(2)}</td>
                  <td className="p-3 text-right">{trade.shares}</td>
                  <td className="p-3 text-right font-bold">
                    <span className={trade.pnl >= 0 ? 'text-green-400' : 'text-red-400'}>
                      ${trade.pnl.toFixed(2)}
                    </span>
                  </td>
                  <td className="p-3 text-right text-slate-500 text-sm">
                    {new Date(trade.timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
                  </td>
                </tr>
              ))}
              {roundTrades.length === 0 && (
                <tr>
                  <td colSpan="6" className="p-4 text-center text-slate-500">
                    No completed round trades yet. Match BUYs with SELLs to see P&L.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  )
}
