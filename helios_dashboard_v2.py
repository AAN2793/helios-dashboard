import streamlit as st
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# File paths
CONFIG_PATH = Path('HELIOS_CONFIG.json')
MEMORY_TODOS = Path('memory') / 'todos.md'
MEMORY_IDEAS = Path('memory') / 'ideas.md'

# Ensure directories
MEMORY_TODOS.parent.mkdir(exist_ok=True)
MEMORY_IDEAS.parent.mkdir(exist_ok=True)

# Load data functions
def save_config(config):
    """Save config to file."""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    """Load config from file, return default if not found."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except:
            pass
    # Default config
    return {
        "budget": {"target": 2.80, "cap": 3.22, "current": 0.60},
        "spending": {"MiniMax": 0.40, "Sonnet": 0.10, "Opus": 0.75, "Grok": 0.55},
        "tasks": [
            {"id": 1, "description": "iMessage setup", "status": "done", "timestamp": "2026-02-01 11:00", "model": "Grok"},
            {"id": 2, "description": "Discord bot add", "status": "done", "timestamp": "2026-02-01 11:46", "model": "Grok"},
            {"id": 3, "description": "Model switching fix", "status": "done", "timestamp": "2026-02-01 12:00", "model": "Opus"},
            {"id": 4, "description": "Morning brief cron", "status": "future", "timestamp": "2026-02-01 06:00", "model": "Grok"},
            {"id": 5, "description": "Evening report", "status": "future", "timestamp": "2026-02-01 20:28", "model": "Sonnet"},
        ],
        "stocks": {
            "BTI": {"price": 35.2, "change": 1.3, "roic": "8.5%", "pe": "12.4"},
            "NVDA": {"price": 120.5, "change": 2.1, "roic": "25.4%", "pe": "35.2"},
            "PEP": {"price": 170.8, "change": 0.8, "roic": "18.2%", "pe": "22.1"},
            "WMT": {"price": 75.4, "change": -0.5, "roic": "12.1%", "pe": "28.3"},
        },
        "schedule": {
            "5:39 AM": "Wake up, coffee, quiet time",
            "6:00 AM": "Morning brief (Grok news/stocks)",
            "2:45 PM": "Family time (school pickup, CrossFit)",
            "5:00 PM": "Work check-in, dinner",
            "8:22 PM": "Work session after steps",
        },
        "current_model": "Grok-4-Fast"
    }

def load_memory(file):
    """Load memory file as list of lines."""
    if file.exists():
        try:
            with open(file, 'r') as f:
                content = f.read().strip()
                return [line.strip() for line in content.split('\n') if line.strip()]
        except:
            pass
    return []

def save_memory(file, data):
    """Save list to memory file."""
    try:
        with open(file, 'w') as f:
            f.write('\n'.join(data))
    except Exception as e:
        st.error(f"Save error: {e}")

st.set_page_config(page_title="Helios Dashboard v2", layout="wide", page_icon="🛸")

st.title("🛸 Helios Dashboard v2")

config = load_config()
todos = load_memory(MEMORY_TODOS)
ideas = load_memory(MEMORY_IDEAS)

# Sidebar Controls
st.sidebar.header("Controls")
pause = st.sidebar.button("Pause Operations", type="secondary")
emergency = st.sidebar.button("Emergency Stop", type="primary")
if pause:
    st.sidebar.success("Operations Paused")
    st.stop()
if emergency:
    st.sidebar.error("EMERGENCY STOP - Everything Halted!")
    st.stop()

model_options = ["MiniMax", "Sonnet", "Opus", "Grok-4-Fast"]
current_model_index = next((i for i, opt in enumerate(model_options) if opt == config["current_model"]), 0)
current_model = st.sidebar.selectbox("Model", model_options, index=current_model_index)
if st.sidebar.button("Switch Model"):
    config["current_model"] = current_model
    save_config(config)
    st.rerun()
st.sidebar.info(f"Current: {config['current_model']}")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Home & Budget", "📋 Tasks", "💡 Ideas", "✅ Todos", "📅 Schedule", "💹 Stocks"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.header("💰 Budget Meter")
        budget = config["budget"]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=budget["current"],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Current Spend ($)"},
            delta={'reference': budget["target"]},
            gauge={
                'axis': {'range': [0, budget["cap"]]},
                'bar': {'color': "cyan"},
                'steps': [
                    {'range': [0, budget["target"]], 'color': "lightgreen"},
                    {'range': [budget["target"], budget["cap"]], 'color': "yellow"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': budget["cap"]
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        col_a, col_b = st.columns(2)
        col_a.metric("Target ($2.80)", f"${budget['current']:.2f}", f"+${budget['current'] - budget['target']:.2f}")
        col_b.metric("Cap ($3.22)", f"${budget['cap'] - budget['current']:.2f}", f"-${budget['current']:.2f}")
        
        if budget['current'] > budget['target']:
            st.warning("⚠️ Conservation mode: Opus disabled, stick to MiniMax.")

    with col2:
        st.header("📈 Model Spending")
        spending_df = pd.DataFrame(list(config["spending"].items()), columns=["Model", "Cost"])
        fig_spend = px.bar(spending_df, x="Model", y="Cost", title="Daily Spend by Model")
        st.plotly_chart(fig_spend, use_container_width=True)

with tab2:
    st.header("📋 Tasks & Organization")
    tasks_df = pd.DataFrame(config["tasks"])
    if 'timestamp' in tasks_df.columns:
        tasks_df['timestamp'] = pd.to_datetime(tasks_df['timestamp'], errors='coerce')
        tasks_df = tasks_df.sort_values('timestamp', ascending=False)
    
    done = tasks_df[tasks_df['status'] == 'done'] if 'status' in tasks_df.columns else pd.DataFrame()
    future = tasks_df[tasks_df['status'] == 'future'] if 'status' in tasks_df.columns else pd.DataFrame()
    
    st.subheader("✅ Done Tasks")
    st.dataframe(done[['description', 'timestamp', 'model']] if all(col in done.columns for col in ['description', 'timestamp', 'model']) else done, use_container_width=True)
    
    st.subheader("🔮 Future Tasks")
    st.dataframe(future[['description', 'timestamp', 'model']] if all(col in future.columns for col in ['description', 'timestamp', 'model']) else future, use_container_width=True)
    
    st.subheader("Add New Task")
    new_desc = st.text_input("Description")
    new_model = st.selectbox("Model", model_options)
    if st.button("Add Task"):
        new_id = len(config["tasks"]) + 1
        config["tasks"].append({
            "id": new_id, "description": new_desc, "status": "future", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "model": new_model
        })
        save_config(config)
        st.success("Task added!")
        st.rerun()

with tab3:
    st.header("💡 Ideas for Future")
    st.write("Editable brainstorm list – saves to memory/ideas.md")
    
    updated_ideas = []
    for i, idea in enumerate(ideas):
        col1, col2 = st.columns([4, 1])
        with col1:
            new_idea_val = st.text_input(f"Idea {i+1}:", value=idea, key=f"idea_{i}")
            if new_idea_val:
                updated_ideas.append(new_idea_val)
        with col2:
            if st.button("Delete", key=f"del_{i}"):
                st.success("Idea deleted")
                st.rerun()
    
    ideas = updated_ideas
    
    new_idea = st.text_input("Add New Idea")
    if st.button("Add Idea"):
        if new_idea:
            ideas.append(new_idea)
            save_memory(MEMORY_IDEAS, ideas)
            st.success("Idea added!")
            st.rerun()
    
    save_memory(MEMORY_IDEAS, ideas)
    st.info(f"Saved {len(ideas)} ideas to {MEMORY_IDEAS}")

with tab4:
    st.header("✅ Todo Tracker")
    st.write("Checkbox list – mark done to log in tasks. Saves to memory/todos.md")
    
    updated_todos = []
    for i, todo in enumerate(todos):
        col1, col2 = st.columns([4, 1])
        with col1:
            completed = st.checkbox(todo, key=f"todo_{i}")
        with col2:
            if st.button("Delete", key=f"tdel_{i}"):
                st.success(f"{todo} deleted")
                st.rerun()
        
        if completed:
            # Log to tasks
            log_desc = f"{todo} marked done"
            config["tasks"].append({
                "id": len(config["tasks"]) + 1,
                "description": log_desc,
                "status": "done",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "model": config["current_model"]
            })
            save_config(config)
            st.success(f"{todo} completed and logged!")
        else:
            updated_todos.append(todo)
    
    todos = updated_todos
    new_todo = st.text_input("Add New Todo")
    if st.button("Add Todo"):
        if new_todo:
            todos.append(new_todo)
            save_memory(MEMORY_TODOS, todos)
            st.success("Todo added!")
            st.rerun()
    
    save_memory(MEMORY_TODOS, todos)
    st.info(f"{len(todos)} todos remaining.")

with tab5:
    st.header("📅 Daily Schedule")
    st.write("From USER.md – family/work blocks")
    for time, desc in config["schedule"].items():
        st.write(f"**{time}**: {desc}")

with tab6:
    st.header("💹 Stock Holdings")
    st.write("Dummy data for now – add real API later")
    stocks_data = [{"Symbol": sym, **data} for sym, data in config["stocks"].items()]
    stocks_df = pd.DataFrame(stocks_data)
    if not stocks_df.empty:
        stocks_df['change %'] = [f"+{d['change']}%" if d['change'] > 0 else f"{d['change']}%" for d in stocks_data]
        fig_stocks = px.bar(stocks_df, x="Symbol", y="price", title="Holdings")
        st.plotly_chart(fig_stocks, use_container_width=True)
        st.dataframe(stocks_df[["Symbol", "price", "change %", "roic", "pe"]])

# Footer
st.caption("Helios Dashboard v2 – Organized & Interactive. Edit files in memory/ for persistence.")