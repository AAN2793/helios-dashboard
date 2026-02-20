import fs from 'fs'
import path from 'path'

const DATA_FILE = '/Users/helios/.openclaw/workspace/carbon_cut/carbon_cut_data.json'

export default function handler(req, res) {
  if (req.method === 'GET') {
    try {
      if (fs.existsSync(DATA_FILE)) {
        const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'))
        return res.status(200).json(data)
      }
      return res.status(200).json({ solicitations: [], lastUpdated: null })
    } catch (err) {
      return res.status(500).json({ error: err.message })
    }
  }

  if (req.method === 'POST') {
    try {
      let data = { solicitations: [], lastUpdated: null }
      if (fs.existsSync(DATA_FILE)) {
        data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'))
      }
      
      const newEntry = req.body
      newEntry.id = Date.now().toString()
      newEntry.createdAt = new Date().toISOString()
      
      data.solicitations.push(newEntry)
      data.lastUpdated = new Date().toISOString()
      
      fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2))
      return res.status(200).json(data)
    } catch (err) {
      return res.status(500).json({ error: err.message })
    }
  }

  if (req.method === 'DELETE') {
    try {
      const { id } = req.body
      let data = { solicitations: [], lastUpdated: null }
      if (fs.existsSync(DATA_FILE)) {
        data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'))
      }
      
      data.solicitations = data.solicitations.filter(s => s.id !== id)
      data.lastUpdated = new Date().toISOString()
      
      fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2))
      return res.status(200).json(data)
    } catch (err) {
      return res.status(500).json({ error: err.message })
    }
  }

  res.status(405).json({ error: 'Method not allowed' })
}
