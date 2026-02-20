import { useState, useEffect } from 'react'
import Layout from '../components/Layout'

export default function CarbonData() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    solicitation_id: '',
    project_name: '',
    county: '',
    wells_count: '',
    status: 'Open',
    bid_due_date: '',
    winning_company: '',
    winning_bid_amount: '',
    your_bid_amount: '',
    notes: ''
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const res = await fetch('/api/carbon-data')
      const json = await res.json()
      setData(json.solicitations || [])
    } catch (err) {
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch('/api/carbon-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      const json = await res.json()
      setData(json.solicitations || [])
      setShowForm(false)
      setFormData({
        solicitation_id: '',
        project_name: '',
        county: '',
        wells_count: '',
        status: 'Open',
        bid_due_date: '',
        winning_company: '',
        winning_bid_amount: '',
        your_bid_amount: '',
        notes: ''
      })
    } catch (err) {
      alert('Error adding entry: ' + err.message)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this entry?')) return
    try {
      const res = await fetch('/api/carbon-data', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
      })
      const json = await res.json()
      setData(json.solicitations || [])
    } catch (err) {
      alert('Error deleting: ' + err.message)
    }
  }

  const downloadCSV = () => {
    const headers = ['Solicitation_ID', 'Project_Name', 'County', 'Wells_Count', 'Status', 'Bid_Due_Date', 'Winning_Company', 'Winning_Bid_Amount', 'Your_Bid_Amount', 'Notes']
    const rows = data.map(d => [
      d.solicitation_id || '',
      d.project_name || '',
      d.county || '',
      d.wells_count || '',
      d.status || '',
      d.bid_due_date || '',
      d.winning_company || '',
      d.winning_bid_amount || '',
      d.your_bid_amount || '',
      d.notes || ''
    ])
    
    const csv = [headers, ...rows].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `carbon-cut-ohio-wells-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
  }

  return (
    <Layout title="Carbon Cut - Ohio Wells Data">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-green-500">Carbon Cut - Ohio Wells Data</h1>
        <p className="text-slate-400 mt-2">Track orphan well contracts, bids, and opportunities</p>
      </header>

      <div className="mb-6 flex gap-4">
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-green-700 text-green-100 rounded hover:bg-green-600"
        >
          {showForm ? 'Cancel' : '+ Add Entry'}
        </button>
        <button
          onClick={downloadCSV}
          className="px-4 py-2 bg-blue-700 text-blue-100 rounded hover:bg-blue-600"
        >
          Download CSV
        </button>
        <button
          onClick={fetchData}
          className="px-4 py-2 bg-slate-700 text-slate-200 rounded hover:bg-slate-600"
        >
          Refresh
        </button>
      </div>

      {showForm && (
        <div className="bg-slate-800 p-6 rounded-lg mb-6">
          <h2 className="text-xl font-bold text-green-400 mb-4">Add New Entry</h2>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Solicitation ID"
              value={formData.solicitation_id}
              onChange={e => setFormData({...formData, solicitation_id: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700"
            />
            <input
              type="text"
              placeholder="Project Name"
              value={formData.project_name}
              onChange={e => setFormData({...formData, project_name: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700"
            />
            <input
              type="text"
              placeholder="County"
              value={formData.county}
              onChange={e => setFormData({...formData, county: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700"
            />
            <input
              type="number"
              placeholder="Wells Count"
              value={formData.wells_count}
              onChange={e => setFormData({...formData, wells_count: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700"
            />
            <select
              value={formData.status}
              onChange={e => setFormData({...formData, status: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700"
            >
              <option value="Open">Open</option>
              <option value="Closed">Closed</option>
              <option value="Awarded">Awarded</option>
            </select>
            <input
              type="date"
              placeholder="Bid Due Date"
              value={formData.bid_due_date}
              onChange={e => setFormData({...formData, bid_due_date: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700"
            />
            <input
              type="text"
              placeholder="Winning Company"
              value={formData.winning_company}
              onChange={e => setFormData({...formData, winning_company: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700"
            />
            <input
              type="number"
              placeholder="Winning Bid $"
              value={formData.winning_bid_amount}
              onChange={e => setFormData({...formData, winning_bid_amount: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700"
            />
            <input
              type="number"
              placeholder="Your Bid $"
              value={formData.your_bid_amount}
              onChange={e => setFormData({...formData, your_bid_amount: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700"
            />
            <input
              type="text"
              placeholder="Notes"
              value={formData.notes}
              onChange={e => setFormData({...formData, notes: e.target.value})}
              className="px-3 py-2 bg-slate-900 text-white rounded border border-slate-700 md:col-span-2"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-500 md:col-span-2"
            >
              Save Entry
            </button>
          </form>
        </div>
      )}

      {loading ? (
        <div className="text-cyan-400">Loading...</div>
      ) : data.length === 0 ? (
        <div className="text-slate-400">No entries yet. Click "+ Add Entry" to start.</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-slate-400 border-b border-slate-700">
                <th className="p-2">Solicitation</th>
                <th className="p-2">Project</th>
                <th className="p-2">County</th>
                <th className="p-2">Wells</th>
                <th className="p-2">Status</th>
                <th className="p-2">Bid Due</th>
                <th className="p-2">Winner</th>
                <th className="p-2">Winning Bid</th>
                <th className="p-2">Your Bid</th>
                <th className="p-2"></th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => (
                <tr key={idx} className="border-b border-slate-800 hover:bg-slate-800">
                  <td className="p-2 text-green-400">{row.solicitation_id || '-'}</td>
                  <td className="p-2">{row.project_name || '-'}</td>
                  <td className="p-2">{row.county || '-'}</td>
                  <td className="p-2">{row.wells_count || '-'}</td>
                  <td className="p-2">
                    <span className={`px-2 py-1 rounded text-xs ${
                      row.status === 'Open' ? 'bg-green-900 text-green-300' :
                      row.status === 'Awarded' ? 'bg-blue-900 text-blue-300' :
                      'bg-slate-700 text-slate-300'
                    }`}>
                      {row.status || '-'}
                    </span>
                  </td>
                  <td className="p-2">{row.bid_due_date || '-'}</td>
                  <td className="p-2">{row.winning_company || '-'}</td>
                  <td className="p-2">${row.winning_bid_amount || '-'}</td>
                  <td className="p-2 text-green-400">${row.your_bid_amount || '-'}</td>
                  <td className="p-2">
                    <button
                      onClick={() => handleDelete(row.id)}
                      className="text-red-400 hover:text-red-300 text-xs"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  )
}
