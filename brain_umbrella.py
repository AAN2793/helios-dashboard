#!/usr/bin/env python3
"""
Brain Umbrella - Multi-Subagent Management System for OpenClaw

A professional orchestration framework that manages multiple AI subagents with
intelligent routing, budget tracking, auto-escalation, and result aggregation.

Author: OpenClaw System
License: MIT
"""

import asyncio
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar
from collections import defaultdict
import heapq


# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("BrainUmbrella")


# -----------------------------------------------------------------------------
# Enums and Constants
# -----------------------------------------------------------------------------

class SubagentType(Enum):
    """Enumeration of available subagent types with their characteristics."""
    CODEX_BUILDER = "codex-builder"      # Code generation and architecture
    SONNET_WRITER = "sonnet-writer"      # Creative writing and documentation
    MINIMAX_CHEAP = "minimax-cheap"      # Cost-efficient simple tasks
    GROK_RESEARCHER = "grok-researcher"  # Deep research and analysis


class TaskPriority(Enum):
    """Priority levels for task scheduling."""
    CRITICAL = 0    # Immediate execution, interrupts current work
    HIGH = 1        # Execute before normal tasks
    NORMAL = 2      # Standard priority
    LOW = 3         # Background tasks, execute when idle
    BATCH = 4       # Deferred to off-peak hours


class TaskStatus(Enum):
    """Lifecycle states for a task."""
    PENDING = auto()
    ASSIGNED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    ESCALATED = auto()
    CANCELLED = auto()


class ResultStatus(Enum):
    """Status of result delivery."""
    DELIVERED = auto()
    DELIVERY_FAILED = auto()
    PENDING_ACK = auto()


# Budget constraints
DAILY_BUDGET_USD = 2.80
BUDGET_WARNING_THRESHOLD = 0.80  # Warn at 80% of budget


# -----------------------------------------------------------------------------
# Data Classes
# -----------------------------------------------------------------------------

@dataclass
class SubagentConfig:
    """Configuration for a subagent type."""
    subagent_type: SubagentType
    model_name: str
    avg_cost_per_task: float  # USD estimate
    max_tasks_per_day: int
    timeout_seconds: int
    capabilities: List[str] = field(default_factory=list)
    escalation_chain: List[SubagentType] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.escalation_chain:
            self.escalation_chain = self._default_escalation()
    
    def _default_escalation(self) -> List[SubagentType]:
        """Define default escalation path."""
        chain_map = {
            SubagentType.MINIMAX_CHEAP: [SubagentType.SONNET_WRITER, SubagentType.GROK_RESEARCHER],
            SubagentType.CODEX_BUILDER: [SubagentType.GROK_RESEARCHER],
            SubagentType.SONNET_WRITER: [SubagentType.GROK_RESEARCHER],
            SubagentType.GROK_RESEARCHER: [],  # Final escalation
        }
        return chain_map.get(self.subagent_type, [])


@dataclass
class Task:
    """Represents a unit of work to be processed by a subagent."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content: str = ""
    task_type: SubagentType = SubagentType.MINIMAX_CHEAP
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    assigned_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assigned_to: Optional[str] = None
    result: Any = None
    error: Optional[str] = None
    escalation_count: int = 0
    max_escalations: int = 2
    metadata: Dict[str, Any] = field(default_factory=dict)
    callback: Optional[Callable[[Any], None]] = None
    
    def __lt__(self, other: 'Task') -> bool:
        """Enable comparison for priority queue (lower number = higher priority)."""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.created_at < other.created_at
    
    def age_seconds(self) -> float:
        """Calculate age of task in seconds."""
        return (datetime.now() - self.created_at).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize task to dictionary."""
        return {
            "id": self.id,
            "content": self.content[:100] + "..." if len(self.content) > 100 else self.content,
            "task_type": self.task_type.value,
            "priority": self.priority.name,
            "status": self.status.name,
            "created_at": self.created_at.isoformat(),
            "assigned_to": self.assigned_to,
            "age_seconds": self.age_seconds(),
            "escalation_count": self.escalation_count,
        }


@dataclass
class BudgetEntry:
    """Tracks spending for a single task."""
    task_id: str
    subagent_type: SubagentType
    estimated_cost: float
    actual_cost: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SubagentStatus:
    """Runtime status of a subagent instance."""
    session_id: str
    subagent_type: SubagentType
    current_task: Optional[Task] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    last_activity: datetime = field(default_factory=datetime.now)
    is_active: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize status to dictionary."""
        return {
            "session_id": self.session_id,
            "subagent_type": self.subagent_type.value,
            "current_task_id": self.current_task.id if self.current_task else None,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "is_active": self.is_active,
            "idle_seconds": (datetime.now() - self.last_activity).total_seconds(),
        }


@dataclass
class TaskResult:
    """Result wrapper for task completion."""
    task_id: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    processing_time_seconds: float = 0.0
    subagent_used: Optional[SubagentType] = None
    cost_usd: float = 0.0


# -----------------------------------------------------------------------------
# Budget Management
# -----------------------------------------------------------------------------

class BudgetTracker:
    """
    Tracks daily spending across all subagents with budget enforcement.
    """
    
    def __init__(self, daily_budget: float = DAILY_BUDGET_USD):
        self.daily_budget = daily_budget
        self.warning_threshold = daily_budget * BUDGET_WARNING_THRESHOLD
        self.entries: List[BudgetEntry] = []
        self._lock = asyncio.Lock()
        self._current_date = datetime.now().date()
    
    async def record_estimate(self, task: Task, config: SubagentConfig) -> bool:
        """
        Record estimated cost before task execution.
        Returns False if task would exceed budget.
        """
        async with self._lock:
            self._check_date_rollover()
            
            estimated = config.avg_cost_per_task
            current_spent = self._today_spend()
            
            if current_spent + estimated > self.daily_budget:
                logger.warning(
                    f"Budget rejection: task {task.id} would exceed daily budget "
                    f"(${current_spent:.2f} + ${estimated:.2f} > ${self.daily_budget:.2f})"
                )
                return False
            
            entry = BudgetEntry(
                task_id=task.id,
                subagent_type=config.subagent_type,
                estimated_cost=estimated
            )
            self.entries.append(entry)
            
            if current_spent + estimated > self.warning_threshold:
                logger.warning(
                    f"Budget at {((current_spent + estimated) / self.daily_budget * 100):.0f}%: "
                    f"${current_spent + estimated:.2f} / ${self.daily_budget:.2f}"
                )
            
            return True
    
    async def record_actual(self, task_id: str, actual_cost: float):
        """Update entry with actual cost after completion."""
        async with self._lock:
            for entry in self.entries:
                if entry.task_id == task_id and entry.actual_cost is None:
                    entry.actual_cost = actual_cost
                    break
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get current budget statistics."""
        async with self._lock:
            self._check_date_rollover()
            
            today_entries = [e for e in self.entries if e.timestamp.date() == self._current_date]
            by_subagent = defaultdict(lambda: {"estimated": 0.0, "actual": 0.0, "count": 0})
            
            for entry in today_entries:
                by_subagent[entry.subagent_type.value]["estimated"] += entry.estimated_cost
                by_subagent[entry.subagent_type.value]["actual"] += entry.actual_cost or entry.estimated_cost
                by_subagent[entry.subagent_type.value]["count"] += 1
            
            total_estimated = sum(e.estimated_cost for e in today_entries)
            total_actual = sum(e.actual_cost or e.estimated_cost for e in today_entries)
            
            return {
                "daily_budget": self.daily_budget,
                "spent_estimated": total_estimated,
                "spent_actual": total_actual,
                "remaining": self.daily_budget - total_actual,
                "percentage_used": (total_actual / self.daily_budget * 100),
                "by_subagent": dict(by_subagent),
                "task_count": len(today_entries),
            }
    
    def _check_date_rollover(self):
        """Clear entries if date has changed."""
        today = datetime.now().date()
        if today != self._current_date:
            logger.info(f"Date rollover: clearing budget entries for {self._current_date}")
            self.entries = []
            self._current_date = today
    
    def _today_spend(self) -> float:
        """Calculate today's actual or estimated spend."""
        today = datetime.now().date()
        today_entries = [e for e in self.entries if e.timestamp.date() == today]
        return sum(e.actual_cost or e.estimated_cost for e in today_entries)


# -----------------------------------------------------------------------------
# Task Queue
# -----------------------------------------------------------------------------

class TaskQueue:
    """
    Priority queue for task management with support for task lifecycle.
    """
    
    def __init__(self):
        self._queue: List[Task] = []
        self._tasks: Dict[str, Task] = {}
        self._lock = asyncio.Lock()
        self._counter = 0  # Tie-breaker for equal priorities
    
    async def enqueue(self, task: Task) -> str:
        """Add task to queue. Returns task ID."""
        async with self._lock:
            self._counter += 1
            # Store counter for FIFO ordering within same priority
            task.metadata["_queue_counter"] = self._counter
            heapq.heappush(self._queue, task)
            self._tasks[task.id] = task
            logger.info(f"Task {task.id} enqueued with priority {task.priority.name}")
            return task.id
    
    async def dequeue(self) -> Optional[Task]:
        """Get highest priority task. Returns None if empty."""
        async with self._lock:
            while self._queue:
                task = heapq.heappop(self._queue)
                if task.status == TaskStatus.PENDING:
                    task.status = TaskStatus.ASSIGNED
                    task.assigned_at = datetime.now()
                    return task
            return None
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        async with self._lock:
            return self._tasks.get(task_id)
    
    async def update_status(self, task_id: str, status: TaskStatus, 
                           result: Any = None, error: Optional[str] = None):
        """Update task status and optionally set result."""
        async with self._lock:
            task = self._tasks.get(task_id)
            if task:
                task.status = status
                if status == TaskStatus.COMPLETED:
                    task.completed_at = datetime.now()
                    task.result = result
                elif status == TaskStatus.FAILED:
                    task.error = error
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task."""
        async with self._lock:
            task = self._tasks.get(task_id)
            if task and task.status == TaskStatus.PENDING:
                task.status = TaskStatus.CANCELLED
                return True
            return False
    
    async def get_pending_count(self) -> int:
        """Count of pending tasks."""
        async with self._lock:
            return sum(1 for t in self._tasks.values() if t.status == TaskStatus.PENDING)
    
    async def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """List tasks with optional status filter."""
        async with self._lock:
            tasks = list(self._tasks.values())
            if status:
                tasks = [t for t in tasks if t.status == status]
            return sorted(tasks, key=lambda t: t.created_at, reverse=True)
    
    async def get_queue_snapshot(self) -> List[Dict[str, Any]]:
        """Get current queue state for dashboard."""
        async with self._lock:
            pending = [t for t in self._tasks.values() if t.status == TaskStatus.PENDING]
            return [t.to_dict() for t in sorted(pending)[:20]]  # Top 20


# -----------------------------------------------------------------------------
# Escalation Management
# -----------------------------------------------------------------------------

class EscalationManager:
    """
    Handles automatic escalation of failed tasks to alternative subagents.
    """
    
    def __init__(self, configs: Dict[SubagentType, SubagentConfig]):
        self.configs = configs
        self.escalation_history: Dict[str, List[SubagentType]] = defaultdict(list)
    
    def should_escalate(self, task: Task) -> bool:
        """Check if task should be escalated."""
        if task.escalation_count >= task.max_escalations:
            return False
        
        current_config = self.configs.get(task.task_type)
        if not current_config or not current_config.escalation_chain:
            return False
        
        return True
    
    def get_next_subagent(self, task: Task) -> Optional[SubagentType]:
        """Determine next subagent in escalation chain."""
        current_config = self.configs.get(task.task_type)
        if not current_config:
            return None
        
        escalation_chain = current_config.escalation_chain
        if task.escalation_count >= len(escalation_chain):
            return None
        
        return escalation_chain[task.escalation_count]
    
    def escalate_task(self, task: Task) -> bool:
        """
        Escalate task to next subagent in chain.
        Returns True if escalated, False if no more options.
        """
        if not self.should_escalate(task):
            logger.warning(f"Task {task.id} cannot be escalated further")
            return False
        
        next_subagent = self.get_next_subagent(task)
        if not next_subagent:
            return False
        
        self.escalation_history[task.id].append(task.task_type)
        task.task_type = next_subagent
        task.escalation_count += 1
        task.status = TaskStatus.ESCALATED
        
        logger.info(
            f"Task {task.id} escalated to {next_subagent.value} "
            f"(attempt {task.escalation_count}/{task.max_escalations})"
        )
        return True
    
    def get_escalation_path(self, task_id: str) -> List[str]:
        """Get the escalation path for a task."""
        return [s.value for s in self.escalation_history.get(task_id, [])]


# -----------------------------------------------------------------------------
# Subagent Router
# -----------------------------------------------------------------------------

class SubagentRouter:
    """
    Routes tasks to appropriate subagents based on task type and content analysis.
    """
    
    def __init__(self, configs: Dict[SubagentType, SubagentConfig]):
        self.configs = configs
        self.pattern_map = self._build_pattern_map()
    
    def _build_pattern_map(self) -> Dict[str, SubagentType]:
        """Build keyword-to-subagent mapping for intelligent routing."""
        return {
            # Code patterns -> Codex-Builder
            "code": SubagentType.CODEX_BUILDER,
            "function": SubagentType.CODEX_BUILDER,
            "class": SubagentType.CODEX_BUILDER,
            "module": SubagentType.CODEX_BUILDER,
            "repository": SubagentType.CODEX_BUILDER,
            "refactor": SubagentType.CODEX_BUILDER,
            "debug": SubagentType.CODEX_BUILDER,
            "implement": SubagentType.CODEX_BUILDER,
            "script": SubagentType.CODEX_BUILDER,
            "api": SubagentType.CODEX_BUILDER,
            "build": SubagentType.CODEX_BUILDER,
            
            # Writing patterns -> Sonnet-Writer
            "write": SubagentType.SONNET_WRITER,
            "draft": SubagentType.SONNET_WRITER,
            "document": SubagentType.SONNET_WRITER,
            "story": SubagentType.SONNET_WRITER,
            "blog": SubagentType.SONNET_WRITER,
            "essay": SubagentType.SONNET_WRITER,
            "content": SubagentType.SONNET_WRITER,
            "article": SubagentType.SONNET_WRITER,
            "email": SubagentType.SONNET_WRITER,
            "copy": SubagentType.SONNET_WRITER,
            "creative": SubagentType.SONNET_WRITER,
            
            # Research patterns -> Grok-Researcher
            "research": SubagentType.GROK_RESEARCHER,
            "analyze": SubagentType.GROK_RESEARCHER,
            "investigate": SubagentType.GROK_RESEARCHER,
            "search": SubagentType.GROK_RESEARCHER,
            "find": SubagentType.GROK_RESEARCHER,
            "compare": SubagentType.GROK_RESEARCHER,
            "evaluate": SubagentType.GROK_RESEARCHER,
            "study": SubagentType.GROK_RESEARCHER,
            "survey": SubagentType.GROK_RESEARCHER,
            "deep dive": SubagentType.GROK_RESEARCHER,
            
            # Simple task patterns -> MiniMax-Cheap
            "summarize": SubagentType.MINIMAX_CHEAP,
            "list": SubagentType.MINIMAX_CHEAP,
            "format": SubagentType.MINIMAX_CHEAP,
            "convert": SubagentType.MINIMAX_CHEAP,
            "simple": SubagentType.MINIMAX_CHEAP,
            "basic": SubagentType.MINIMAX_CHEAP,
            "quick": SubagentType.MINIMAX_CHEAP,
            "extract": SubagentType.MINIMAX_CHEAP,
        }
    
    def route_by_content(self, content: str) -> SubagentType:
        """
        Analyze content and determine best subagent type.
        Falls back to MINIMAX_CHEAP for uncertain matches.
        """
        content_lower = content.lower()
        scores = defaultdict(int)
        
        for pattern, subagent_type in self.pattern_map.items():
            if pattern in content_lower:
                scores[subagent_type] += 1
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return SubagentType.MINIMAX_CHEAP
    
    def get_config(self, subagent_type: SubagentType) -> Optional[SubagentConfig]:
        """Get configuration for subagent type."""
        return self.configs.get(subagent_type)
    
    def validate_route(self, task: Task) -> Tuple[bool, str]:
        """Validate that a task can be routed."""
        config = self.configs.get(task.task_type)
        if not config:
            return False, f"Unknown subagent type: {task.task_type.value}"
        return True, "Valid"


# -----------------------------------------------------------------------------
# Status Dashboard
# -----------------------------------------------------------------------------

class StatusDashboard:
    """
    Real-time dashboard tracking all subagent activity.
    """
    
    def __init__(self):
        self.subagents: Dict[str, SubagentStatus] = {}
        self.task_history: List[Dict[str, Any]] = []
        self._max_history = 100
        self._lock = asyncio.Lock()
    
    async def register_subagent(self, session_id: str, subagent_type: SubagentType):
        """Register a new subagent session."""
        async with self._lock:
            self.subagents[session_id] = SubagentStatus(
                session_id=session_id,
                subagent_type=subagent_type
            )
            logger.info(f"Subagent registered: {session_id} ({subagent_type.value})")
    
    async def unregister_subagent(self, session_id: str):
        """Remove a subagent session."""
        async with self._lock:
            if session_id in self.subagents:
                del self.subagents[session_id]
                logger.info(f"Subagent unregistered: {session_id}")
    
    async def update_activity(self, session_id: str, task: Optional[Task] = None):
        """Update subagent activity status."""
        async with self._lock:
            if session_id in self.subagents:
                status = self.subagents[session_id]
                status.current_task = task
                status.last_activity = datetime.now()
                status.is_active = task is not None
    
    async def record_completion(self, session_id: str, success: bool):
        """Record task completion or failure."""
        async with self._lock:
            if session_id in self.subagents:
                status = self.subagents[session_id]
                if success:
                    status.tasks_completed += 1
                else:
                    status.tasks_failed += 1
                status.current_task = None
                status.is_active = False
    
    async def add_history(self, entry: Dict[str, Any]):
        """Add entry to task history."""
        async with self._lock:
            entry["timestamp"] = datetime.now().isoformat()
            self.task_history.append(entry)
            if len(self.task_history) > self._max_history:
                self.task_history = self.task_history[-self._max_history:]
    
    async def get_dashboard(self) -> Dict[str, Any]:
        """Get complete dashboard snapshot."""
        async with self._lock:
            active_count = sum(1 for s in self.subagents.values() if s.is_active)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "active_subagents": active_count,
                "total_subagents": len(self.subagents),
                "subagent_details": [s.to_dict() for s in self.subagents.values()],
                "recent_history": self.task_history[-20:],
            }
    
    async def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get list of currently active tasks."""
        async with self._lock:
            active = []
            for status in self.subagents.values():
                if status.is_active and status.current_task:
                    active.append({
                        "subagent_session": status.session_id,
                        "subagent_type": status.subagent_type.value,
                        "task": status.current_task.to_dict(),
                    })
            return active


# -----------------------------------------------------------------------------
# Result Aggregation
# -----------------------------------------------------------------------------

class ResultAggregator:
    """
    Aggregates results from subagents and formats for delivery to main session.
    """
    
    def __init__(self):
        self.results: Dict[str, TaskResult] = {}
        self.delivery_status: Dict[str, ResultStatus] = {}
        self._lock = asyncio.Lock()
    
    async def store_result(self, result: TaskResult):
        """Store a task result."""
        async with self._lock:
            self.results[result.task_id] = result
            self.delivery_status[result.task_id] = ResultStatus.PENDING_ACK
    
    async def mark_delivered(self, task_id: str):
        """Mark result as delivered to main session."""
        async with self._lock:
            self.delivery_status[task_id] = ResultStatus.DELIVERED
    
    async def mark_delivery_failed(self, task_id: str):
        """Mark result as failed delivery."""
        async with self._lock:
            self.delivery_status[task_id] = ResultStatus.DELIVERY_FAILED
    
    async def get_result(self, task_id: str) -> Optional[TaskResult]:
        """Get result by task ID."""
        async with self._lock:
            return self.results.get(task_id)
    
    async def get_pending_deliveries(self) -> List[TaskResult]:
        """Get results pending delivery."""
        async with self._lock:
            pending = []
            for task_id, status in self.delivery_status.items():
                if status == ResultStatus.PENDING_ACK:
                    result = self.results.get(task_id)
                    if result:
                        pending.append(result)
            return pending
    
    def format_for_delivery(self, result: TaskResult) -> Dict[str, Any]:
        """Format result for main session consumption."""
        return {
            "task_id": result.task_id,
            "success": result.success,
            "data": result.data,
            "error": result.error,
            "subagent_used": result.subagent_used.value if result.subagent_used else None,
            "processing_time_seconds": result.processing_time_seconds,
            "cost_usd": result.cost_usd,
            "delivered_at": datetime.now().isoformat(),
        }
    
    async def get_summary_report(self) -> Dict[str, Any]:
        """Generate summary report of all results."""
        async with self._lock:
            total = len(self.results)
            successful = sum(1 for r in self.results.values() if r.success)
            failed = total - successful
            total_cost = sum(r.cost_usd for r in self.results.values())
            
            by_subagent = defaultdict(lambda: {"success": 0, "failed": 0, "cost": 0.0})
            for result in self.results.values():
                key = result.subagent_used.value if result.subagent_used else "unknown"
                by_subagent[key]["success" if result.success else "failed"] += 1
                by_subagent[key]["cost"] += result.cost_usd
            
            return {
                "timestamp": datetime.now().isoformat(),
                "total_tasks": total,
                "successful": successful,
                "failed": failed,
                "success_rate": (successful / total * 100) if total > 0 else 0,
                "total_cost_usd": total_cost,
                "by_subagent": dict(by_subagent),
            }


# -----------------------------------------------------------------------------
# Subagent Worker
# -----------------------------------------------------------------------------

class SubagentWorker:
    """
    Worker class that simulates subagent execution.
    In production, this would interface with actual subagent processes.
    """
    
    def __init__(self, session_id: str, config: SubagentConfig, 
                 dashboard: StatusDashboard, aggregator: ResultAggregator):
        self.session_id = session_id
        self.config = config
        self.dashboard = dashboard
        self.aggregator = aggregator
        self._running = False
    
    async def start(self):
        """Start the worker."""
        await self.dashboard.register_subagent(self.session_id, self.config.subagent_type)
        self._running = True
        logger.info(f"Worker started: {self.session_id}")
    
    async def stop(self):
        """Stop the worker."""
        self._running = False
        await self.dashboard.unregister_subagent(self.session_id)
        logger.info(f"Worker stopped: {self.session_id}")
    
    async def execute(self, task: Task) -> TaskResult:
        """
        Execute a task. This is a simulation - replace with actual subagent calls.
        """
        start_time = time.time()
        await self.dashboard.update_activity(self.session_id, task)
        
        try:
            # Simulate processing time based on subagent type
            processing_time = self._simulate_processing(task)
            await asyncio.sleep(processing_time)
            
            # Simulate result generation
            result_data = self._generate_result(task)
            
            processing_time_actual = time.time() - start_time
            
            # Calculate cost based on actual processing characteristics
            cost = self._calculate_cost(task, processing_time_actual)
            
            result = TaskResult(
                task_id=task.id,
                success=True,
                data=result_data,
                subagent_used=self.config.subagent_type,
                processing_time_seconds=processing_time_actual,
                cost_usd=cost
            )
            
            await self.dashboard.record_completion(self.session_id, True)
            await self.aggregator.store_result(result)
            
            logger.info(
                f"Task {task.id} completed by {self.session_id} "
                f"in {processing_time_actual:.2f}s, cost ${cost:.4f}"
            )
            
            return result
            
        except Exception as e:
            processing_time_actual = time.time() - start_time
            await self.dashboard.record_completion(self.session_id, False)
            
            result = TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                subagent_used=self.config.subagent_type,
                processing_time_seconds=processing_time_actual,
                cost_usd=self.config.avg_cost_per_task * 0.5  # Partial cost for failure
            )
            
            await self.aggregator.store_result(result)
            logger.error(f"Task {task.id} failed: {e}")
            
            return result
        finally:
            await self.dashboard.update_activity(self.session_id, None)
    
    def _simulate_processing(self, task: Task) -> float:
        """Simulate processing time based on task complexity."""
        base_times = {
            SubagentType.MINIMAX_CHEAP: 1.0,
            SubagentType.CODEX_BUILDER: 3.0,
            SubagentType.SONNET_WRITER: 4.0,
            SubagentType.GROK_RESEARCHER: 8.0,
        }
        base = base_times.get(self.config.subagent_type, 2.0)
        
        # Factor in content length
        length_factor = min(len(task.content) / 1000, 2.0)
        
        return base * (0.8 + length_factor * 0.2)
    
    def _generate_result(self, task: Task) -> Dict[str, Any]:
        """Generate simulated result data."""
        return {
            "subagent": self.config.subagent_type.value,
            "output": f"Processed by {self.config.model_name}",
            "task_preview": task.content[:50] + "..." if len(task.content) > 50 else task.content,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _calculate_cost(self, task: Task, processing_time: float) -> float:
        """Calculate actual cost based on processing characteristics."""
        # Base cost from config
        base = self.config.avg_cost_per_task
        
        # Adjust based on actual vs expected time
        expected_time = self._simulate_processing(task)
        time_factor = processing_time / expected_time if expected_time > 0 else 1.0
        
        # Cap variation at 50%
        adjusted = base * max(0.5, min(1.5, time_factor))
        
        return round(adjusted, 4)


# -----------------------------------------------------------------------------
# Main Orchestrator
# -----------------------------------------------------------------------------

class BrainUmbrella:
    """
    Central orchestrator that manages all subagents, routing, budget, and results.
    
    This is the main entry point for the Brain Umbrella system.
    """
    
    def __init__(self, daily_budget: float = DAILY_BUDGET_USD):
        # Initialize configurations
        self.configs = self._initialize_configs()
        
        # Initialize subsystems
        self.budget_tracker = BudgetTracker(daily_budget)
        self.task_queue = TaskQueue()
        self.router = SubagentRouter(self.configs)
        self.escalation_manager = EscalationManager(self.configs)
        self.dashboard = StatusDashboard()
        self.aggregator = ResultAggregator()
        
        # Worker management
        self.workers: Dict[str, SubagentWorker] = {}
        self._worker_counter = 0
        self._lock = asyncio.Lock()
        
        # Control flag
        self._running = False
        self._main_loop_task: Optional[asyncio.Task] = None
        
        logger.info("BrainUmbrella initialized")
    
    def _initialize_configs(self) -> Dict[SubagentType, SubagentConfig]:
        """Initialize default configurations for all subagent types."""
        return {
            SubagentType.CODEX_BUILDER: SubagentConfig(
                subagent_type=SubagentType.CODEX_BUILDER,
                model_name="o3-mini",
                avg_cost_per_task=0.25,
                max_tasks_per_day=30,
                timeout_seconds=120,
                capabilities=["code_generation", "architecture", "debugging", "refactoring"],
            ),
            SubagentType.SONNET_WRITER: SubagentConfig(
                subagent_type=SubagentType.SONNET_WRITER,
                model_name="claude-sonnet-4",
                avg_cost_per_task=0.40,
                max_tasks_per_day=20,
                timeout_seconds=180,
                capabilities=["writing", "documentation", "creative", "copywriting"],
            ),
            SubagentType.MINIMAX_CHEAP: SubagentConfig(
                subagent_type=SubagentType.MINIMAX_CHEAP,
                model_name="minimax-6.5s",
                avg_cost_per_task=0.08,
                max_tasks_per_day=100,
                timeout_seconds=60,
                capabilities=["summarization", "formatting", "simple_tasks", "extraction"],
            ),
            SubagentType.GROK_RESEARCHER: SubagentConfig(
                subagent_type=SubagentType.GROK_RESEARCHER,
                model_name="grok-2",
                avg_cost_per_task=0.75,
                max_tasks_per_day=10,
                timeout_seconds=300,
                capabilities=["research", "analysis", "deep_dive", "comparison"],
            ),
        }
    
    async def start(self):
        """Start the BrainUmbrella system."""
        self._running = True
        self._main_loop_task = asyncio.create_task(self._main_loop())
        logger.info("BrainUmbrella started")
    
    async def stop(self):
        """Stop the BrainUmbrella system."""
        self._running = False
        
        if self._main_loop_task:
            self._main_loop_task.cancel()
            try:
                await self._main_loop_task
            except asyncio.CancelledError:
                pass
        
        # Stop all workers
        for worker in self.workers.values():
            await worker.stop()
        
        logger.info("BrainUmbrella stopped")
    
    async def submit_task(self, content: str, 
                         task_type: Optional[SubagentType] = None,
                         priority: TaskPriority = TaskPriority.NORMAL,
                         metadata: Optional[Dict[str, Any]] = None,
                         callback: Optional[Callable[[Any], None]] = None) -> str:
        """
        Submit a new task to the system.
        
        Args:
            content: The task content/instructions
            task_type: Specific subagent type, or None for auto-routing
            priority: Task priority level
            metadata: Additional task metadata
            callback: Optional callback for completion notification
            
        Returns:
            Task ID string
        """
        # Auto-route if no type specified
        if task_type is None:
            task_type = self.router.route_by_content(content)
            logger.info(f"Auto-routed task to {task_type.value}")
        
        task = Task(
            content=content,
            task_type=task_type,
            priority=priority,
            metadata=metadata or {},
            callback=callback
        )
        
        # Check budget before enqueuing
        config = self.configs.get(task_type)
        if config:
            budget_ok = await self.budget_tracker.record_estimate(task, config)
            if not budget_ok:
                task.status = TaskStatus.CANCELLED
                logger.error(f"Task {task.id} rejected due to budget constraints")
                return task.id
        
        await self.task_queue.enqueue(task)
        return task.id
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a task."""
        task = await self.task_queue.get_task(task_id)
        if task:
            return task.to_dict()
        return None
    
    async def get_dashboard(self) -> Dict[str, Any]:
        """Get full system dashboard."""
        dashboard = await self.dashboard.get_dashboard()
        budget = await self.budget_tracker.get_stats()
        queue = await self.task_queue.get_queue_snapshot()
        
        return {
            "system": "BrainUmbrella",
            "status": "running" if self._running else "stopped",
            "dashboard": dashboard,
            "budget": budget,
            "pending_queue": queue,
        }
    
    async def get_results_report(self) -> Dict[str, Any]:
        """Get aggregated results report."""
        return await self.aggregator.get_summary_report()
    
    async def _main_loop(self):
        """Main processing loop for task execution."""
        while self._running:
            try:
                # Process pending tasks
                task = await self.task_queue.dequeue()
                
                if task:
                    await self._execute_task(task)
                else:
                    # No tasks, wait before checking again
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.exception(f"Error in main loop: {e}")
                await asyncio.sleep(5)
    
    async def _execute_task(self, task: Task):
        """Execute a single task with escalation handling."""
        # Get or create worker for this subagent type
        worker = await self._get_or_create_worker(task.task_type)
        
        if not worker:
            logger.error(f"No worker available for {task.task_type.value}")
            await self.task_queue.update_status(task.id, TaskStatus.FAILED, error="No worker available")
            return
        
        # Execute
        result = await worker.execute(task)
        
        # Handle result
        if result.success:
            await self.task_queue.update_status(task.id, TaskStatus.COMPLETED, result=result.data)
            await self.budget_tracker.record_actual(task.id, result.cost_usd)
            await self.dashboard.add_history({
                "event": "task_completed",
                "task_id": task.id,
                "subagent": task.task_type.value,
            })
            
            # Trigger callback if provided
            if task.callback:
                try:
                    task.callback(result.data)
                except Exception as e:
                    logger.warning(f"Callback failed for task {task.id}: {e}")
        else:
            # Check for escalation
            if self.escalation_manager.should_escalate(task):
                escalated = self.escalation_manager.escalate_task(task)
                if escalated:
                    await self.task_queue.enqueue(task)
                    await self.dashboard.add_history({
                        "event": "task_escalated",
                        "task_id": task.id,
                        "from": task.task_type.value,
                        "to": self.escalation_manager.get_next_subagent(task).value if self.escalation_manager.get_next_subagent(task) else None,
                    })
                    return
            
            # No escalation possible, mark as failed
            await self.task_queue.update_status(task.id, TaskStatus.FAILED, error=result.error)
            await self.dashboard.add_history({
                "event": "task_failed",
                "task_id": task.id,
                "error": result.error,
            })
    
    async def _get_or_create_worker(self, subagent_type: SubagentType) -> Optional[SubagentWorker]:
        """Get an existing worker or create a new one for the subagent type."""
        async with self._lock:
            # Look for idle worker of this type
            for session_id, worker in self.workers.items():
                if worker.config.subagent_type == subagent_type:
                    status = self.dashboard.subagents.get(session_id)
                    if status and not status.is_active:
                        return worker
            
            # Create new worker
            self._worker_counter += 1
            session_id = f"{subagent_type.value}-{self._worker_counter}"
            
            config = self.configs.get(subagent_type)
            if not config:
                return None
            
            worker = SubagentWorker(session_id, config, self.dashboard, self.aggregator)
            await worker.start()
            self.workers[session_id] = worker
            
            return worker
    
    async def deliver_results(self) -> List[Dict[str, Any]]:
        """
        Deliver pending results to main session.
        Returns list of delivered result summaries.
        """
        pending = await self.aggregator.get_pending_deliveries()
        delivered = []
        
        for result in pending:
            formatted = self.aggregator.format_for_delivery(result)
            
            # Simulate delivery to main session
            # In production, this would use actual message channel
            delivery_success = await self._deliver_to_main(formatted)
            
            if delivery_success:
                await self.aggregator.mark_delivered(result.task_id)
                delivered.append(formatted)
            else:
                await self.aggregator.mark_delivery_failed(result.task_id)
        
        return delivered
    
    async def _deliver_to_main(self, result: Dict[str, Any]) -> bool:
        """
        Simulate delivery to main session.
        Returns True if successful.
        """
        # In production, this would integrate with message channel
        # For now, just log and return success
        logger.info(f"Delivering result for task {result['task_id']} to main session")
        return True


# -----------------------------------------------------------------------------
# Factory and Helper Functions
# -----------------------------------------------------------------------------

async def create_umbrella(daily_budget: float = DAILY_BUDGET_USD) -> BrainUmbrella:
    """
    Factory function to create and start a BrainUmbrella instance.
    
    Args:
        daily_budget: Daily budget limit in USD (default: $2.80)
        
    Returns:
        Started BrainUmbrella instance
    """
    umbrella = BrainUmbrella(daily_budget)
    await umbrella.start()
    return umbrella


async def quick_task(content: str, priority: TaskPriority = TaskPriority.NORMAL) -> str:
    """
    Quick helper to submit a task with auto-routing.
    
    This creates a temporary umbrella instance for single task execution.
    For production use, maintain a persistent BrainUmbrella instance.
    """
    umbrella = await create_umbrella()
    try:
        task_id = await umbrella.submit_task(content, priority=priority)
        
        # Wait for completion (with timeout)
        max_wait = 60  # seconds
        for _ in range(max_wait):
            status = await umbrella.get_task_status(task_id)
            if status and status["status"] in ["COMPLETED", "FAILED", "CANCELLED"]:
                break
            await asyncio.sleep(1)
        
        # Deliver results
        results = await umbrella.deliver_results()
        
        return task_id
    finally:
        await umbrella.stop()


# -----------------------------------------------------------------------------
# CLI and Demo
# -----------------------------------------------------------------------------

async def demo():
    """Demonstrate BrainUmbrella capabilities."""
    print("=" * 60)
    print("BRAIN UMBRELLA - Multi-Subagent Management System")
    print("=" * 60)
    
    # Create and start
    umbrella = await create_umbrella(daily_budget=2.80)
    
    try:
        # Submit various tasks
        tasks = [
            ("Write a Python function to calculate fibonacci numbers", TaskPriority.NORMAL),
            ("Research the latest developments in quantum computing", TaskPriority.HIGH),
            ("Summarize this text about artificial intelligence", TaskPriority.LOW),
            ("Create a blog post about climate change solutions", TaskPriority.NORMAL),
            ("Debug this code that keeps throwing null pointer exceptions", TaskPriority.CRITICAL),
            ("List the top 10 Python libraries for data science", TaskPriority.BATCH),
        ]
        
        print("\nSubmitting tasks...")
        task_ids = []
        for content, priority in tasks:
            tid = await umbrella.submit_task(content, priority=priority)
            print(f"  Submitted: {tid} ({priority.name})")
            task_ids.append(tid)
        
        # Wait for processing
        print("\nProcessing tasks...")
        await asyncio.sleep(15)
        
        # Show dashboard
        print("\n" + "-" * 60)
        print("SYSTEM DASHBOARD")
        print("-" * 60)
        dashboard = await umbrella.get_dashboard()
        
        print(f"\nStatus: {dashboard['status']}")
        print(f"Active Subagents: {dashboard['dashboard']['active_subagents']}")
        print(f"Total Subagents: {dashboard['dashboard']['total_subagents']}")
        
        # Budget report
        print("\nBUDGET STATUS:")
        budget = dashboard['budget']
        print(f"  Daily Budget: ${budget['daily_budget']:.2f}")
        print(f"  Spent: ${budget['spent_actual']:.2f}")
        print(f"  Remaining: ${budget['remaining']:.2f}")
        print(f"  Usage: {budget['percentage_used']:.1f}%")
        
        # Deliver results
        print("\n" + "-" * 60)
        print("DELIVERING RESULTS")
        print("-" * 60)
        results = await umbrella.deliver_results()
        for r in results:
            print(f"\nTask {r['task_id']}:")
            print(f"  Success: {r['success']}")
            print(f"  Subagent: {r['subagent_used']}")
            print(f"  Time: {r['processing_time_seconds']:.2f}s")
            print(f"  Cost: ${r['cost_usd']:.4f}")
        
        # Summary report
        print("\n" + "=" * 60)
        print("SUMMARY REPORT")
        print("=" * 60)
        report = await umbrella.get_results_report()
        print(f"Total Tasks: {report['total_tasks']}")
        print(f"Successful: {report['successful']}")
        print(f"Failed: {report['failed']}")
        print(f"Success Rate: {report['success_rate']:.1f}%")
        print(f"Total Cost: ${report['total_cost_usd']:.4f}")
        
    finally:
        await umbrella.stop()
        print("\n" + "=" * 60)
        print("BrainUmbrella shutdown complete")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())
