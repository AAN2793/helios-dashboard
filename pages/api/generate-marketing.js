import { execSync } from 'child_process'
import path from 'path'

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const { prompt } = req.body

  if (!prompt) {
    return res.status(400).json({ error: 'Prompt is required' })
  }

  try {
    // Create temp git repo (required for Claude Code)
    const SCRATCH = `/tmp/marketing_${Date.now()}`
    execSync(`mkdir -p ${SCRATCH} && cd ${SCRATCH} && git init`, { stdio: 'pipe' })
    
    // Run Claude Code
    const result = execSync(
      `echo "${prompt.replace(/"/g, '\\"')}" | "/Users/helios/Library/Application Support/Claude/claude-code/2.1.49/claude" --print`,
      { 
        timeout: 90000,
        maxBuffer: 10 * 1024 * 1024,
        stdio: 'pipe'
      }
    ).toString()

    // Clean up
    execSync(`rm -rf ${SCRATCH}`, { stdio: 'pipe' })

    return res.status(200).json({ content: result })
  } catch (error) {
    console.error('Error generating content:', error)
    return res.status(500).json({ error: error.message })
  }
}
