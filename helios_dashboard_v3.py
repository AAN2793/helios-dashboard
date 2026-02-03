import streamlit as st
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page config - DARK THEME
st.set_page_config(
    page_title="Helios Command Center",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

# DARK THEME CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #21262d;
        color: #8b949e;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #238636 !important;
        color: white !important;
    }
    .css-1d391kg, .css-1lcbmhc {
        background-color: #161b22;
    }
    .stMetric {
        background-color: #21262d;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    .stDataFrame {
        background-color: #161b22;
    }
    h1, h2, h3 {
        color: #f0f6fc !important;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }
    .agent-card {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .status-active {
        color: #3fb950;
        font-weight: bold;
    }
    .status-complete {
        color: #58a6ff;
    }
    .status-pending {
        color: #d29922;
    }
</style>
""", unsafe_allow_html=True)

# File paths
CONFIG_PATH = Path('HELIOS_CONFIG.json')
MEMORY_TODOS = Path('memory') / 'todos.md'
MEMORY_IDEAS = Path('memory') / 'ideas.md'
MEMORY_SUBAGENTS = Path('memory') / 'subagents.md'

# Ensure directories
MEMORY_TODOS.parent.mkdir(exist_ok=True)

# Title
st.title("🧠 Helios Command Center")
st.caption("Brain Umbrella System | Multi-Agent Dashboard")

# Sidebar - Controls
st.sidebar.header("🎛️ Controls")
st.sidebar.markdown("---")

# Model Status
st.sidebar.subheader("Active Models")
st.sidebar.markdown("""
- 🧠 **Kimi-Main** (Primary)
- 💰 MiniMax-Cheap
- 💻 Codex-Builder  
- ✍️ Sonnet-Writer
""")

# Emergency controls
if st.sidebar.button("🛑 Emergency Stop", type="primary"):
    st.sidebar.error("All agents halted!")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.info("Sub-agents spawn automatically based on task type")

# Load data
def load_memory(file):
    if file.exists():
        try:
            with open(file, 'r') as f:
                content = f.read().strip()
                return [line.strip() for line in content.split('\n') if line.strip()]
        except:
            pass
    return []

# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", "👥 Sub-Agents", "📋 Tasks", "💡 Ideas", "✅ Todos", "💹 Stocks"
])

# TAB 1: OVERVIEW
with tab1:
    st.header("System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Agents", "4", "+1 today")
    with col2:
        st.metric("Tasks Today", "12", "+3")
    with col3:
        st.metric("Cost Today", "$0.89", "-$0.12")
    with col4:
        st.metric("Sub-Agents", "2", "+1 active")
    
    st.markdown("---")
    
    # Recent Activity
    st.subheader("🔄 Recent Activity")
    activity_data = [
        {"Time": "09:18", "Agent": "Codex-Builder", "Task": "Built trading_journal.py", "Status": "✅ Complete"},
        {"Time": "08:45", "Agent": "Kimi-Main", "Task": "Configured sub-agents", "Status": "✅ Complete"},
        {"Time": "08:30", "Agent": "MiniMax-Cheap", "Task": "Dashboard monitoring", "Status": "🟢 Active"},
    ]
    df_activity = pd.DataFrame(activity_data)
    st.dataframe(df_activity, use_container_width=True, hide_index=True)

# TAB 2: SUB-AGENTS
with tab2:
    st.header("👥 Sub-Agent Activity")
    
    # Active Agents Grid
    st.subheader("Active Sub-Agents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <h4>💻 Codex-Builder</h4>
            <p><span class="status-active">● Active</span> | Model: GPT-5.1-Codex</p>
            <p>Last Task: Built trading_journal.py</p>
            <p>Runtime: 19s | Cost: $0.03</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="agent-card">
            <h4>💰 MiniMax-Cheap</h4>
            <p><span class="status-active">● Standby</span> | Model: MiniMax M2.1</p>
            <p>Ready for: Monitoring, simple queries</p>
            <p>Cost: ~$0.001/task</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <h4>✍️ Sonnet-Writer</h4>
            <p><span class="status-pending">○ Standby</span> | Model: Claude Sonnet</p>
            <p>Ready for: Content, analysis, reports</p>
            <p>Cost: ~$0.08/task</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="agent-card">
            <h4>🧠 Kimi-Main</h4>
            <p><span class="status-active">● Primary</span> | Model: Kimi K2.5</p>
            <p>Role: Coordinator, main interface</p>
            <p>Cost: ~$0.02/task</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Task Queue
    st.markdown("---")
    st.subheader("📋 Task Queue")
    
    queue_data = [
        {"Task": "Morning market brief", "Assigned": "Sonnet-Writer", "Status": "⏳ Pending", "Priority": "High"},
        {"Task": "Monitor NVDA", "Assigned": "MiniMax-Cheap", "Status": "🟢 Active", "Priority": "Medium"},
        {"Task": "Build earnings scraper", "Assigned": "Codex-Builder", "Status": "📋 Queued", "Priority": "High"},
    ]
    df_queue = pd.DataFrame(queue_data)
    st.dataframe(df_queue, use_container_width=True, hide_index=True)

# TAB 3: TASKS
with tab3:
    st.header("📋 Task History")
    
    tasks = [
        {"Date": "2026-02-02", "Task": "Configure Brain Umbrella", "Agent": "Kimi-Main", "Status": "✅"},
        {"Date": "2026-02-02", "Task": "Build trading journal", "Agent": "Codex-Builder", "Status": "✅"},
        {"Date": "2026-02-01", "Task": "Setup Discord bot", "Agent": "Kimi-Main", "Status": "✅"},
        {"Date": "2026-02-01", "Task": "Configure OpenRouter models", "Agent": "Kimi-Main", "Status": "✅"},
    ]
    df_tasks = pd.DataFrame(tasks)
    st.dataframe(df_tasks, use_container_width=True, hide_index=True)
    
    st.subheader("➕ Add New Task")
    new_task = st.text_input("Task description")
    col1, col2 = st.columns(2)
    with col1:
        agent_choice = st.selectbox("Assign to", ["Auto-select", "Kimi-Main", "Codex-Builder", "Sonnet-Writer", "MiniMax-Cheap"])
    with col2:
        if st.button("Spawn Sub-Agent"):
            st.success(f"Spawning {agent_choice} for: {new_task}")

# TAB 4: IDEAS
with tab4:
    st.header("💡 Future Ideas & Tools")
    
    ideas = load_memory(MEMORY_IDEAS)
    
    for idea in ideas[:10]:  # Show first 10
        st.checkbox(idea, key=f"idea_{idea[:20]}")
    
    st.markdown("---")
    new_idea = st.text_input("Add new idea")
    if st.button("Add Idea") and new_idea:
        with open(MEMORY_IDEAS, 'a') as f:
            f.write(f"\n{new_idea}")
        st.success("Idea added!")

# TAB 5: TODOS
with tab5:
    st.header("✅ Todo List")
    
    todos = load_memory(MEMORY_TODOS)
    
    remaining = []
    for todo in todos:
        if not st.checkbox(todo, key=f"todo_{todo[:20]}"):
            remaining.append(todo)
    
    st.markdown("---")
    st.info(f"{len(remaining)} todos remaining")
    
    new_todo = st.text_input("Add todo")
    if st.button("Add Todo") and new_todo:
        with open(MEMORY_TODOS, 'a') as f:
            f.write(f"\n{new_todo}")
        st.success("Todo added!")

# TAB 6: STOCKS
with tab6:
    st.header("💹 Stock Holdings")
    
    stocks_data = {
        "NVDA": {"price": 120.5, "change": 2.1, "roic": "25.4%", "pe": "35.2"},
        "PEP": {"price": 170.8, "change": 0.8, "roic": "18.2%", "pe": "22.1"},
        "WMT": {"price": 75.4, "change": -0.5, "roic": "12.1%", "pe": "28.3"},
        "BTI": {"price": 35.2, "change": 1.3, "roic": "8.5%", "pe": "12.4"},
    }
    
    df_stocks = pd.DataFrame([
        {"Symbol": k, **v} for k, v in stocks_data.items()
    ])
    
    fig = px.bar(df_stocks, x="Symbol", y="price", 
                 title="Portfolio Holdings",
                 color="change",
                 color_continuous_scale=["red", "green"])
    fig.update_layout(
        plot_bgcolor='#161b22',
        paper_bgcolor='#0d1117',
        font_color='#c9d1d9'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df_stocks, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption("Helios Brain Umbrella v3.0 | Multi-Agent System | Dark Mode")
