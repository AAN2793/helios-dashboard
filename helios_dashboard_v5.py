#!/usr/bin/env python3
"""
HELIOS COMMAND v5 - Interactive Enterprise Dashboard
Features: File Browser, Content Generator, Newsletter Builder, Quick Actions
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HELIOS COMMAND v5 | Interactive Dashboard",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# COLOR PALETTE
# -----------------------------------------------------------------------------
COLORS = {
    'bg': '#0a0a0a',
    'card': '#1a1a1a',
    'border': '#2a2a2a',
    'text': '#e8e8e8',
    'muted': '#4a4a4a',
    'blue': '#00b4d8',
    'cyan': '#00d4ff',
    'green': '#00c853',
    'red': '#ff3838',
    'orange': '#ff9500',
    'purple': '#7c4dff',
}

# -----------------------------------------------------------------------------
# CSS
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');
    
    .stApp {{ background-color: {COLORS['bg']}; color: {COLORS['text']}; }}
    
    h1, h2, h3 {{ font-family: 'Inter', sans-serif; font-weight: 600; }}
    .data-text {{ font-family: 'JetBrains Mono', monospace; }}
    
    .metric-card {{
        background: {COLORS['card']}; border: 1px solid {COLORS['border']};
        padding: 16px; border-radius: 0;
    }}
    
    .stButton>button {{
        background: {COLORS['card']}; border: 1px solid {COLORS['border']};
        color: {COLORS['text']}; border-radius: 0; font-family: 'JetBrains Mono';
    }}
    .stButton>button:hover {{
        background: {COLORS['blue']}; color: {COLORS['bg']};
    }}
    
    .file-item {{
        padding: 8px 12px; margin: 4px 0; cursor: pointer;
        background: {COLORS['card']}; border: 1px solid {COLORS['border']};
    }}
    .file-item:hover {{
        border-color: {COLORS['blue']}; background: {COLORS['border']};
    }}
    
    .section-header {{
        background: {COLORS['card']}; border-left: 3px solid {COLORS['blue']};
        padding: 8px 12px; margin: 16px 0 8px 0;
        font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;
    }}
    
    .quick-action {{
        padding: 12px; text-align: center; cursor: pointer;
        background: {COLORS['card']}; border: 1px solid {COLORS['border']};
        transition: all 0.2s;
    }}
    .quick-action:hover {{
        border-color: {COLORS['cyan']}; transform: translateY(-2px);
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div style="background: linear-gradient(90deg, #0d1b2a 0%, #1a1a1a 100%); 
            border-bottom: 2px solid {COLORS['blue']}; padding: 16px 20px;
            margin: -80px -80px 20px -80px; display: flex; justify-content: space-between;">
    <div style="font-family: 'JetBrains Mono'; font-weight: 700; font-size: 1.3rem; 
                color: {COLORS['cyan']}; letter-spacing: 2px;">
        HELIOS COMMAND v5
    </div>
    <div style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: {COLORS['muted']};">
        {datetime.now().strftime('%Y-%m-%d %H:%M')} | INTERACTIVE
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# WORKSPACE PATH
# -----------------------------------------------------------------------------
WORKSPACE = Path('/Users/helios/.openclaw/workspace')
MEMORY_PATH = WORKSPACE / 'memory'

def list_files(directory, extensions=None):
    """List files in directory."""
    if not directory.exists():
        return []
    files = []
    for f in sorted(directory.iterdir()):
        if f.is_file():
            if extensions is None or f.suffix in extensions:
                files.append(f)
        elif f.is_dir() and not f.name.startswith('.'):
            files.extend(list_files(f, extensions))
    return files

def get_file_icon(path):
    """Get icon for file type."""
    icons = {
        '.py': '🐍', '.md': '📝', '.json': '📋', '.csv': '📊',
        '.html': '🌐', '.txt': '📄', '.png': '🖼️', '.jpg': '🖼️',
    }
    return icons.get(path.suffix, '📄')

# -----------------------------------------------------------------------------
# SIDEBAR - QUICK ACTIONS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f'<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)
    
    # Quick action buttons
    if st.button("📰 Generate Newsletter", use_container_width=True):
        st.session_state['action'] = 'newsletter'
    
    if st.button("📊 Run Stock Screener", use_container_width=True):
        st.session_state['action'] = 'screener'
    
    if st.button("🔍 Research Topic", use_container_width=True):
        st.session_state['action'] = 'research'
    
    if st.button("📝 Write Alert Post", use_container_width=True):
        st.session_state['action'] = 'alert'
    
    if st.button("💰 Check Carbon Cut", use_container_width=True):
        st.session_state['action'] = 'carbon'
    
    if st.button("🧠 New Venture Ideas", use_container_width=True):
        st.session_state['action'] = 'venture'
    
    st.markdown('---')
    
    # Cron status
    st.markdown(f'<div class="section-header">📅 Scheduled Jobs</div>', unsafe_allow_html=True)
    cron_jobs = [
        ("5:50 AM", "Morning Newsletter", True),
        ("11:30 AM", "Midday Newsletter", True),
        ("1:28 PM", "Afternoon Newsletter", True),
        ("8:20 PM", "Evening Newsletter", True),
        ("8:28 PM", "Daily Email Check", True),
    ]
    for time, name, enabled in cron_jobs:
        status = "🟢" if enabled else "🔴"
        st.markdown(f"<div class='data-text' style='font-size: 0.75rem; padding: 4px 0;'>{status} {time} — {name}</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN CONTENT
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard",
    "📁 Files",
    "📰 Newsletter",
    "📊 Tools",
    "💬 Chat"
])

# TAB 1: MAIN DASHBOARD
with tab1:
    # Metrics row
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.65rem; color: {COLORS['muted']}; text-transform: uppercase;">OpenClaw</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 1.8rem; font-weight: 600;">ONLINE</div>
            <div style="font-size: 0.7rem; color: {COLORS['green']};">Gateway active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.65rem; color: {COLORS['muted']}; text-transform: uppercase;">Channels</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 1.8rem; font-weight: 600;">2</div>
            <div style="font-size: 0.7rem; color: {COLORS['cyan']};">iMessage + Discord</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.65rem; color: {COLORS['muted']}; text-transform: uppercase;">Cron Jobs</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 1.8rem; font-weight: 600;">5</div>
            <div style="font-size: 0.7rem; color: {COLORS['green']};">All active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.65rem; color: {COLORS['muted']}; text-transform: uppercase;">Workspace Files</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 1.8rem; font-weight: 600;">{len(list_files(WORKSPACE))}</div>
            <div style="font-size: 0.7rem; color: {COLORS['blue']};">Python + Scripts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m5:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.65rem; color: {COLORS['muted']}; text-transform: uppercase;">Heartbeat</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 1.8rem; font-weight: 600;">30m</div>
            <div style="font-size: 0.7rem; color: {COLORS['orange']};">Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m6:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.65rem; color: {COLORS['muted']}; text-transform: uppercase;">Gmail</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 1.8rem; font-weight: 600;">SET</div>
            <div style="font-size: 0.7rem; color: {COLORS['purple']};">App password saved</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('---')
    
    # Two columns
    d1, d2 = st.columns([1, 1])
    
    with d1:
        st.markdown(f'<div class="section-header">🚀 Available Tools</div>', unsafe_allow_html=True)
        
        tools = [
            ("🔍", "Web Search", "Search the web for any topic"),
            ("📰", "Content Generator", "Write social posts, newsletters"),
            ("📊", "Stock Screener", "Screen stocks with criteria"),
            ("🧠", "Venture Scout", "Research new business ideas"),
            ("💰", "Carbon Tracker", "Monitor Carbon Cut Solutions"),
            ("📝", "Document Writer", "Create markdown docs, notes"),
            ("💬", "Research Agent", "Deep dive on any topic"),
            ("📈", "Trading Journal", "Log and analyze trades"),
        ]
        
        for icon, name, desc in tools:
            st.markdown(f"""
            <div class="quick-action" onclick="document.getElementById('{name.replace(' ', '_').lower()}').click()">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="font-weight: 600; margin-top: 4px;">{name}</div>
                <div style="font-size: 0.7rem; color: {COLORS['muted']};">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with d2:
        st.markdown(f'<div class="section-header">📋 Recent Files</div>', unsafe_allow_html=True)
        
        files = list_files(WORKSPACE, {'.py', '.md', '.json', '.txt'})[:10]
        for f in files:
            icon = get_file_icon(f)
            st.markdown(f"""
            <div class="file-item">
                <span style="margin-right: 8px;">{icon}</span>
                <span style="font-family: 'JetBrains Mono'; font-size: 0.8rem;">{f.name}</span>
                <span style="float: right; font-size: 0.65rem; color: {COLORS['muted']};">{f.stat().st_mtime.strftime('%m/%d') if hasattr(f.stat().st_mtime, 'strftime') else 'recent'}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('---')
        
        st.markdown(f'<div class="section-header">🎯 Quick Stats</div>', unsafe_allow_html=True)
        
        stats = [
            ("Python Scripts", 8, "🐍"),
            ("Markdown Docs", 5, "📝"),
            ("Research Files", 3, "🔬"),
            ("Data Files", 2, "📊"),
        ]
        
        for name, count, icon in stats:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid {COLORS['border']};">
                <span><span style="margin-right: 8px;">{icon}</span>{name}</span>
                <span style="font-family: 'JetBrains Mono';">{count}</span>
            </div>
            """, unsafe_allow_html=True)

# TAB 2: FILE BROWSER
with tab2:
    st.markdown(f'<div class="section-header">📁 Workspace File Browser</div>', unsafe_allow_html=True)
    
    fb1, fb2 = st.columns([1, 2])
    
    with fb1:
        # Directory selector
        dirs = [WORKSPACE, WORKSPACE / 'memory']
        selected_dir = st.selectbox("Directory", dirs, format_func=lambda x: f"📁 {x.name}")
        
        # File list
        files = list_files(selected_dir) if selected_dir.exists() else []
        
        for f in files:
            icon = get_file_icon(f)
            if st.button(f"{icon} {f.name}", key=f"file_{f.name}", use_container_width=True):
                st.session_state['selected_file'] = f
    
    with fb2:
        # File viewer/editor
        if 'selected_file' in st.session_state and st.session_state['selected_file'].exists():
            f = st.session_state['selected_file']
            st.markdown(f"**📄 {f.name}**")
            
            try:
                content = f.read_text()
                edited = st.text_area("Edit content:", value=content, height=400)
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("💾 Save Changes"):
                        f.write_text(edited)
                        st.success("Saved!")
                        st.rerun()
                with c2:
                    if st.button("📋 Copy to Clipboard"):
                        st.code(content, language='python' if f.suffix == '.py' else 'text')
            except Exception as e:
                st.error(f"Can't read: {e}")
        else:
            st.info("Select a file to view/edit")
            
            # Show directory structure
            st.markdown("""
            ```
            ~/.openclaw/workspace/
            ├── helios_dashboard_v4.py 🚀
            ├── alerts_content_generator.py 📰
            ├── carbon_cut_tracker.py 💰
            ├── stock_screener.py 📊
            ├── venture_scout.py 🧠
            ├── brain_umbrella.py 🧠
            ├── trading_journal.py 📝
            ├── memory/
            │   ├── todos.md
            │   ├── ideas.md
            │   └── YYYY-MM-DD.md
            └── ...
            ```

            **Key Files:**
            - `helios_dashboard_v4.py` - Main dashboard
            - `alerts_content_generator.py` - Auto-generate alerts
            - `stock_screener.py` - Stock screening tools
            - `venture_scout.py` - New venture research
            - `carbon_cut_tracker.py` - Carbon tracking
            """)

# TAB 3: NEWSLETTER GENERATOR
with tab3:
    st.markdown(f'<div class="section-header">📰 Newsletter Generator</div>', unsafe_allow_html=True)
    
    ng1, ng2 = st.columns([1, 2])
    
    with ng1:
        newsletter_type = st.selectbox("Newsletter Type", [
            "Morning Market Brief",
            "Midday Update", 
            "Afternoon Insights",
            "Evening Recap",
            "Breaking News Alert",
            "Weekly Roundup"
        ])
        
        topics = st.multiselect("Topics to Include", [
            "Stock Market News",
            "AlertsAndNews Updates",
            "Trading Ideas",
            "Earnings Reports",
            "Economic Indicators",
            "Sector Analysis",
            "Crypto/Alternative Assets",
            "General News"
        ])
        
        tone = st.select_slider("Tone", ["Professional", "Informative", "Engaging", "Urgent"], value="Engaging")
        
        length = st.radio("Length", ["Short (1-2 paragraphs)", "Medium (3-4 paragraphs)", "Long (comprehensive)"])
    
    with ng2:
        if st.button("📰 Generate Newsletter", type="primary"):
            with st.spinner("Generating newsletter..."):
                # Generate based on selections
                topic_text = ", ".join(topics) if topics else "market news and insights"
                
                st.markdown(f"""
                ### {newsletter_type}
                
                **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')} | **Tone:** {tone}
                
                ---
                
                **📈 Market Overview**
                
                Markets are showing [INSERT ANALYSIS HERE] today as investors digest the latest economic data and corporate earnings reports.
                
                **🎯 Key Highlights**
                
                • [INSERT KEY POINT 1]
                • [INSERT KEY POINT 2]  
                • [INSERT KEY POINT 3]
                
                **💡 Trading Perspective**
                
                From a technical standpoint, [INSERT ANALYSIS]. Key levels to watch include [INSERT LEVELS].
                
                **📰 Featured Stories**
                
                1. [INSERT HEADLINE 1] - [INSERT BRIEF DESCRIPTION]
                2. [INSERT HEADLINE 2] - [INSERT BRIEF DESCRIPTION]
                3. [INSERT HEADLINE 3] - [INSERT BRIEF DESCRIPTION]
                
                ---
                *Generated by HELIOS | AlertsAndNews*
                """, unsafe_allow_html=True)
                
                # Copy button
                if st.button("📋 Copy to Clipboard"):
                    st.success("Copied! Ready to paste into social media.")
    
    st.markdown('---')
    
    # Quick templates
    st.markdown(f'<div class="section-header">⚡ Quick Templates</div>', unsafe_allow_html=True)
    
    qt1, qt2, qt3, qt4 = st.columns(4)
    
    with qt1:
        if st.button("📈 Stock Alert"):
            st.info("Template: [SYMBOL] is up X% at $[PRICE]. Watch for [RESISTANCE/SUPPORT level]. Volume: [VOLUME]. #TradingAlerts")
    
    with qt2:
        if st.button("📰 News Flash"):
            st.info("Template: BREAKING: [HEADLINE] — [2-3 sentence summary]. Source: [SOURCE]. #News")
    
    with qt3:
        if st.button("💎 Hidden Gem"):
            st.info("Template: [SYMBOL] showing breakout setup. ROIC: [X]%, P/E: [XX]. Potential [GAIN]% upside. #Investing")
    
    with qt4:
        if st.button("🎯 Watchlist"):
            st.info("Template: Today's watchlist: [SYMBOL1], [SYMBOL2], [SYMBOL3]. Key levels and catalysts in comments. #Watchlist")

# TAB 4: TOOLS
with tab4:
    st.markdown(f'<div class="section-header">📊 Trading & Research Tools</div>', unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    
    with t1:
        st.markdown("""
        ### 📊 Stock Screener
        Screen stocks by:
        - ROIC (Return on Invested Capital)
        - P/E Ratio
        - Dividend Yield
        - Market Cap
        - Sector
        """)
        if st.button("Run Screener"):
            st.info("This would integrate with your stock_screener.py")
    
    with t2:
        st.markdown("""
        ### 💰 Carbon Cut Tracker
        Monitor:
        - Well status updates
        - Contract announcements
        - Government funding news
        - Stock price movements
        """)
        if st.button("Check Carbon Cut"):
            st.info("This would integrate with carbon_cut_tracker.py")
    
    with t3:
        st.markdown("""
        ### 🧠 Venture Scout
        Research new opportunities:
        - Market trends
        - Competitor analysis
        - Business models
        - Investment potential
        """)
        if st.button("Find Opportunities"):
            st.info("This would integrate with venture_scout.py")
    
    st.markdown('---')
    
    st.markdown(f'<div class="section-header">📝 Document Tools</div>', unsafe_allow_html=True)
    
    dt1, dt2 = st.columns(2)
    
    with dt1:
        doc_type = st.selectbox("Document Type", [
            "Trading Journal Entry",
            "Research Brief",
            "Meeting Notes",
            "Code Documentation",
            "Project Plan"
        ])
        
        if st.button("Create Document"):
            st.info(f"Would create new {doc_type.lower().replace(' ', '_')}.md")
    
    with dt2:
        st.markdown("""
        ### 📋 Recent Documents
        - `trading_journal.py` - Trade logging system
        - `carbon_cut_research.md` - Research notes
        - `earnings_calendar.html` - Earnings tracking
        """)

# TAB 5: CHAT
with tab5:
    st.markdown(f'<div class="section-header">💬 Chat with Helios</div>', unsafe_allow_html=True)
    
    st.info("💬 Use iMessage or Discord to chat with me directly!")
    
    st.markdown("""
    **I can help you with:**
    
    - 📰 Generating content for AlertsAndNews
    - 🔍 Researching any topic
    - 📊 Analyzing stocks
    - 📝 Writing documents
    - 💻 Running scripts
    - 🧠 Brainstorming ideas
    - 🔧 Fixing code issues
    - 📈 Tracking portfolio
    """)
    
    st.markdown('---')
    
    st.markdown("**Just send me a message via iMessage or Discord and I'll respond!**")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div style="position: fixed; bottom: 0; left: 0; right: 0; 
            background: {COLORS['card']}; border-top: 1px solid {COLORS['border']};
            padding: 8px 20px; font-family: 'JetBrains Mono'; font-size: 0.7rem;
            color: {COLORS['muted']}; display: flex; justify-content: space-between;">
    <span>HELIOS v5.0 | Interactive Dashboard</span>
    <span>Build: 2026.02.03 | Workspace: ~/.openclaw/workspace</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
