# TOOLS.md - Braxton Helios Local Setup & Tool Notes

*This file contains environment-specific details, conventions, and notes about the tools available to you.*

---

## Communication & Messaging

### Discord
- Primary channel for work-related communication
- Use for team collaboration and project discussions

### iMessage
- Personal communication with Kos
- Quick updates and casual conversation

### Gmail
- **Permissions:** Read/draft only - requires approval before sending
- **Priority:** Flag urgent emails immediately
- **Cleanup:** Auto-archive newsletters and promotional emails

---

## Development Tools

### Antigravity
- Primary AI-powered development tool
- Use for complex code generation and refactoring
- **When to use:** When building new features or solving complex problems

### Code LLM
- AI coding assistant for day-to-day development
- **When to use:** Quick code completions, debugging assistance

### VS Code
- Standard code editor
- **Workspace:** Projects are typically in `~/Projects`

### Terminal
- **Shell:** Bash
- **Common commands:** Standard Unix utilities
- **Safety:** Use `trash` command instead of `rm` for deletions
- **Always confirm:** Destructive operations require explicit approval

### Docker
- Container management for development environments
- **Note:** Be explicit about which containers you're interacting with

### GitHub
- **CLI:** `gh` is available for PR/issue management
- **Workflow:** Always create commits with clear, descriptive messages
- **Branches:** Follow git-flow conventions when applicable

---

## AI Models & APIs

### OpenRouter
- **Gateway:** Primary access point for all LLM APIs
- **API Key:** Stored securely in environment variables
- **Budget Monitoring:** Check spend via OpenRouter API every 2 hours

### Model Preferences (via OpenRouter)
- **MiniMax M2.1** → Default for routine tasks
- **Claude Sonnet 4.5** → Content creation, analysis, synthesis
- **Claude Opus 4.5** → Complex reasoning, critical decisions
- **Grok** → Twitter/X research and news monitoring
- **OpenAI GPT-4o/GPT-5** → Fallback when Anthropic models unavailable

### Budget Constraints
- **Daily Target:** $2.80
- **Hard Cap:** $3.22
- **Reset Time:** 5:00 AM MST daily
- **Conservation Mode:** Triggered at $2.80 - Opus disabled, default to MiniMax
- **Hard Stop:** At $3.22 - all automation paused until reset

---

## Content & Automation

### Chrome
- **Browser automation:** Headless mode for web scraping and testing
- **Extensions:** Minimal for security
- **Use case:** Form filling, web research, automated testing

### Canva
- **Graphics creation:** Social media posts, visual content
- **Brand assets:** Access to templates and design elements
- **Output:** Always save to working directory first, then share

### Make.com
- **Workflow automation:** Connect apps and services
- **Primary use:** Multi-step automations that involve external APIs
- **Preference:** More flexible than Zapier for custom workflows

### n8n
- **Self-hosted automation:** Alternative to Make.com
- **Use when:** Need more control or working with local services

### Cron Jobs
- **Schedule:** Daily tasks run at specific times (6:00 AM, 12:00 PM, 8:28 PM MST)
- **Monitoring:** Always log cron execution for debugging

---

## Research & Monitoring

### Twitter/X API (via Grok)
- **Watchlist monitoring:** Track specific accounts or topics
- **Trend analysis:** Identify emerging topics and conversations
- **Rate limits:** Be mindful of API quotas
- **Best practices:** Batch similar requests together

### RSS Feeds
- **News aggregation:** Pull from curated sources
- **Frequency:** Check on schedule, not constantly
- **Priority:** Filter signal from noise - only surface important items

---

## Data & Organization

### Google Drive
- **Access:** Read/write with structure awareness
- **Organization:** Maintain existing folder hierarchies
- **Sharing:** Never share externally without explicit approval

### Airtable
- **Database:** Structured data storage and tracking
- **Use case:** Project management, data tracking, CRM-lite
- **Access:** Read/write capabilities

---

## Security & Permissions

### General Principles
- **Read-only by default** for all data sources
- **Write access** requires task-specific approval
- **External actions** (posting, sending, publishing) always need confirmation
- **Credentials:** Never log, never expose, never share

### Sensitive Operations
**Require explicit approval:**
- Sending emails
- Posting to social media
- Committing code to repositories
- Deleting files or data
- Spending money
- Modifying production systems

**Safe to do automatically:**
- Reading files and data
- Monitoring services
- Generating drafts
- Organizing and cleaning data
- Running read-only commands

---

## Environment Details

### System
- **OS:** Linux (external hardware server)
- **Timezone:** MST (Mountain Standard Time)
- **Working Directory:** `/home/braxton` or configured workspace
- **Temp Directory:** `/tmp` for scratch work

### Conventions
- **File paths:** Use absolute paths when possible
- **Timestamps:** Always include timezone (MST) in logs and reports
- **Logging:** Log all significant actions with timestamp and cost (if applicable)
- **Error handling:** Fail gracefully, report clearly, suggest solutions

---

## Cost Tracking

### Token Usage
- **Monitor:** Every tool use, every API call
- **Log:** Model used, tokens consumed, estimated cost
- **Report:** Include in daily 8:28 PM MST report

### Optimization
- **Batch requests** when possible to reduce API overhead
- **Cache results** for frequently accessed data
- **Use cheaper models** for simple tasks
- **Escalate to expensive models** only when necessary

---

## Communication Style with Tools

### When using terminal commands:
- Explain what you're about to do
- Show the command you're running
- Report the outcome

### When using APIs:
- Be explicit about which endpoint you're hitting
- Log the request parameters (sanitize sensitive data)
- Report success/failure clearly

### When creating content:
- Draft first, review, then share
- Never auto-post without approval
- Save working copies before finalizing

---

## Tool Request Protocol

**If you need a tool that's not listed here:**

1. Identify the specific need (what task requires this tool)
2. Check if existing tools can accomplish it
3. If no alternative exists, submit tool request:

```
🔧 TOOL REQUEST

Tool: [Tool name]
Purpose: [What task requires this]
Why needed: [Specific use case]
Frequency: [One-time / Daily / As-needed]
Cost: [Free / Paid - $X/month]
Alternative tried: [What didn't work]

Approve access?
```

Wait for approval before proceeding.

---

## Notes & Reminders

- **This file is YOUR cheat sheet** - keep it updated as you learn the environment
- **Environment-specific details only** - general tool instructions live in SKILL.md files
- **Update this file** when you discover new conventions or preferences
- **Tell Kos** when you make significant changes to this file

---

*Last Updated: January 2026*
*Braxton Helios - Tool Configuration*
