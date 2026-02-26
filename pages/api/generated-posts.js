import fs from 'fs'
import path from 'path'

export default function handler(req, res) {
  const jsonFile = path.join(process.cwd(), 'data', 'generated-posts.json')

  // GET - return posts
  if (req.method === 'GET') {
    try {
      if (fs.existsSync(jsonFile)) {
        const jsonData = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'))
        // Handle both raw array and { posts: [...] } format
        const posts = Array.isArray(jsonData) ? jsonData : (jsonData.posts || [])
        return res.status(200).json({ posts })
      }
      return res.status(200).json({
        generated: new Date().toISOString(),
        posts: [],
        message: 'No generated posts yet.'
      })
    } catch (err) {
      return res.status(200).json({
        generated: new Date().toISOString(),
        posts: [],
        error: err.message
      })
    }
  }

  // DELETE - remove a post by index
  if (req.method === 'DELETE') {
    try {
      const { index } = req.body
      if (fs.existsSync(jsonFile)) {
        const jsonData = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'))
        if (jsonData.posts && jsonData.posts[index] !== undefined) {
          jsonData.posts.splice(index, 1)
          fs.writeFileSync(jsonFile, JSON.stringify(jsonData, null, 2))
          return res.status(200).json({ success: true, posts: jsonData.posts })
        }
        return res.status(400).json({ error: 'Invalid index' })
      }
      return res.status(404).json({ error: 'No posts file found' })
    } catch (err) {
      return res.status(500).json({ error: err.message })
    }
  }

  res.status(405).json({ error: 'Method not allowed' })
}
