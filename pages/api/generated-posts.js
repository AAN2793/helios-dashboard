import fs from 'fs'
import path from 'path'

export default function handler(req, res) {
  const jsonFile = path.join(process.cwd(), 'data', 'generated-posts.json')

  try {
    if (fs.existsSync(jsonFile)) {
      const jsonData = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'))
      return res.status(200).json(jsonData)
    }
    
    // Return empty state if no generated posts
    res.status(200).json({
      generated: new Date().toISOString(),
      posts: [],
      message: 'No generated posts yet. Run tom-content subagent to create content.'
    })
  } catch (err) {
    res.status(200).json({
      generated: new Date().toISOString(),
      posts: [],
      error: err.message
    })
  }
}
