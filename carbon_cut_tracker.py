#!/usr/bin/env python3
"""
Carbon Cut Solutions - Action Item Tracker

A comprehensive tracking system for immediate action items extracted from
the Carbon Cut Solutions research report. Organizes tasks by owner and
deadline with automated reminder capabilities.

Usage:
    python carbon_cut_tracker.py                    # Display all tasks
    python carbon_cut_tracker.py --owner Nick       # Filter by owner
    python carbon_cut_tracker.py --week 1           # Filter by week
    python carbon_cut_tracker.py --complete 1       # Mark task complete
    python carbon_cut_tracker.py --reminders        # Check overdue items
    python carbon_cut_tracker.py --export           # Export to CSV

Author: Helios Brain Umbrella System
Version: 1.0.0
"""

import json
import argparse
import csv
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional
from pathlib import Path


@dataclass
class Task:
    """Represents a single action item."""
    id: int
    title: str
    owner: str  # "Kos", "Nick", "Eric", or "All"
    week: int  # 1-4
    description: str
    category: str
    status: str = "pending"  # pending, in_progress, complete, blocked
    priority: str = "high"  # critical, high, medium, low
    notes: str = ""
    completed_date: Optional[str] = None
    
    @property
    def deadline_label(self) -> str:
        """Return human-readable deadline."""
        week_map = {
            1: "Week 1 (Days 1-7)",
            2: "Week 2 (Days 8-14)",
            3: "Week 3 (Days 15-21)",
            4: "Week 4 (Days 22-30)"
        }
        return week_map.get(self.week, f"Week {self.week}")


# =============================================================================
# IMMEDIATE ACTION ITEMS (Extracted from Research Report)
# =============================================================================

DEFAULT_TASKS = [
    # ==================== WEEK 1 ====================
    Task(
        id=1,
        title="Get 3 insurance quotes (liability bundles)",
        owner="Nick",
        week=1,
        description="Obtain quotes for General Liability ($1-2M), Environmental Liability ($5-10M), "
                   "Professional Liability ($1-2M), Workers Comp, and Commercial Auto. "
                   "Approach brokers: HUB International, Lockton, or energy-specialist brokers.",
        category="Insurance",
        status="pending",
        priority="critical",
        notes="Target: AIG, Zurich, Chubb. Cost estimate: $15k-30k annually. COIs needed for grants."
    ),
    Task(
        id=2,
        title="Review operating agreement, add capital call provisions",
        owner="Kos",
        week=1,
        description="Amend SD LLC operating agreement to include capital call provisions for future "
                   "fundraising rounds. Ensure preemptive rights and dilution protections are documented.",
        category="Legal/Structure",
        status="pending",
        priority="critical",
        notes="Critical for investor due diligence. Prevent disputes during capital raises."
    ),
    Task(
        id=3,
        title="Complete expense categorization for tax purposes",
        owner="Eric",
        week=1,
        description="Categorize all historical expenses into proper tax categories. Separate "
                   "personal vs business expenses. Prepare documentation for CPA review.",
        category="Accounting",
        status="pending",
        priority="high",
        notes="Essential for Q1 tax filings and establishing clean financial baseline."
    ),
    
    # ==================== WEEK 2 ====================
    Task(
        id=4,
        title="Review and sign buy-sell agreement draft",
        owner="All",
        week=2,
        description="All partners review buy-sell agreement covering: trigger events, valuation method, "
                   "purchase mechanics, funding, non-compete, drag-along/tag-along, dispute resolution.",
        category="Legal/Partnership",
        status="pending",
        priority="critical",
        notes="Must include: death/disability triggers, life insurance funding, 2-5 year non-compete."
    ),
    Task(
        id=5,
        title="Research Series LLC conversion vs holding company",
        owner="Kos",
        week=2,
        description="Evaluate Option A (Series LLC) vs Option B (Holding Company Structure). "
                   "Compare liability isolation benefits vs administrative burden. Get SD attorney consultation.",
        category="Legal/Structure",
        status="pending",
        priority="high",
        notes="Series LLC = simpler for now. Holding company better once >$500k revenue."
    ),
    Task(
        id=6,
        title="Set up accounting system (Quickbooks) with chart of accounts",
        owner="Nick",
        week=2,
        description="Implement Quickbooks or similar accounting software. Establish chart of accounts "
                   "tailored to well plugging operations. Set up separate business accounts.",
        category="Accounting",
        status="pending",
        priority="high",
        notes="Include categories: equipment, subcontractor costs, insurance, grant revenue, carbon credits."
    ),
    
    # ==================== WEEK 3 ====================
    Task(
        id=7,
        title="File any missing foreign registrations (PA/OH)",
        owner="Kos",
        week=3,
        description="Complete foreign LLC registration in Pennsylvania and Ohio if not already filed. "
                   "Verify registered agents are current in all states.",
        category="Compliance",
        status="pending",
        priority="critical",
        notes="Required for PA grants and OH vendor status. Check SD Secretary of State filings too."
    ),
    Task(
        id=8,
        title="Apply for life insurance policies on all partners",
        owner="Nick",
        week=3,
        description="Obtain life insurance quotes for all 3 partners ($500k-1M coverage each). "
                   "Policies needed to fund buy-sell agreement death triggers.",
        category="Insurance",
        status="pending",
        priority="high",
        notes="Mandatory for buy-sell agreement. Term policies are cost-effective option."
    ),
    Task(
        id=9,
        title="Draft standard operating procedures (field operations)",
        owner="Eric",
        week=3,
        description="Create SOPs for well plugging operations: safety protocols, equipment checks, "
                   "environmental safeguards, OSHA compliance procedures, incident reporting.",
        category="Operations",
        status="pending",
        priority="critical",
        notes="Critical for $10M environmental liability coverage compliance and OSHA requirements."
    ),
    
    # ==================== WEEK 4 ====================
    Task(
        id=10,
        title="Attorney review of all agreements",
        owner="All",
        week=4,
        description="SD business attorney reviews: operating agreement, buy-sell agreement, "
                   "insurance policies, grant applications. PA environmental attorney for state-specific issues.",
        category="Legal",
        status="pending",
        priority="critical",
        notes="Budget $5k-10k for legal review. Critical before any capital raising activities."
    ),
    Task(
        id=11,
        title="Set up business credit cards (separate from personal)",
        owner="Kos",
        week=4,
        description="Establish business credit cards for each partner. Set spending limits and "
                   "expense approval workflows. Never commingle personal and business funds.",
        category="Finance",
        status="pending",
        priority="high",
        notes="Essential for LLC asset protection. SD courts pierce veils for commingling."
    ),
    Task(
        id=12,
        title="Finalize expense report and reimbursement workflow",
        owner="Eric",
        week=4,
        description="Create standardized expense report template. Establish reimbursement schedule "
                   "and approval process. Integrate with Quickbooks accounting system.",
        category="Accounting",
        status="pending",
        priority="medium",
        notes="Monthly expense reviews recommended. Reconcile with bank statements."
    ),
]


# =============================================================================
# ADDITIONAL QUICK-WIN TASKS (From Research Report Checklists)
# =============================================================================

ADDITIONAL_TASKS = [
    # Buy-Sell Agreement Components
    Task(id=13, title="Template buy-sell agreement (SD attorney)", owner="Kos", week=2,
         description="Obtain template buy-sell agreement from SD business attorney.",
         category="Legal/Partnership", priority="high"),
    Task(id=14, title="Valuation methodology agreed", owner="All", week=2,
         description="Partners agree on valuation method: appraisal, EBITDA multiple, book value, or formula.",
         category="Legal/Partnership", priority="high"),
    Task(id=15, title="All partners sign and notarize agreements", owner="All", week=2,
         description="Execute buy-sell agreement with notarization. Each partner keeps signed copy.",
         category="Legal/Partnership", priority="critical"),
    
    # Multi-State Compliance
    Task(id=16, title="Verify PA DEP vendor approval maintained", owner="Kos", week=3,
         description="Confirm PA Department of Environmental Protection vendor status is current.",
         category="Compliance", priority="critical"),
    Task(id=17, title="Confirm ODNR vendor certification current", owner="Kos", week=3,
         description="Verify Ohio Department of Natural Resources vendor certification is active.",
         category="Compliance", priority="critical"),
    Task(id=18, title="Annual SD LLC report filed", owner="Kos", week=4,
         description="File annual report with SD Secretary of State (due anniversary month 1st day).",
         category="Compliance", priority="high",
         notes="No state income tax in SD = advantage. Keep registered agent current."),
    
    # Insurance Certificates
    Task(id=19, title="Submit COIs to PA PUC", owner="Nick", week=2,
         description="Submit Certificates of Insurance to Pennsylvania Public Utility Commission.",
         category="Insurance", priority="high"),
    Task(id=20, title="Submit COIs to ODNR", owner="Nick", week=2,
         description="Submit Certificates of Insurance to Ohio Department of Natural Resources.",
         category="Insurance", priority="high"),
    
    # Immediate Opportunity Tasks
    Task(id=21, title="Apply for PA DEP plugging grants", owner="Kos", week=3,
         description="Submit application to PA DEP for well plugging grants (up to $100k per well).",
         category="Grants", priority="critical",
         notes="Quarterly application cycle. 3.7M orphan wells = massive opportunity."),
    Task(id=22, title="Research DOI orphaned well grants", owner="Kos", week=3,
         description="Apply for Department of Interior federal orphan well grants.",
         category="Grants", priority="high",
         notes="$4.7B federal funding via Bipartisan Infrastructure Law."),
    Task(id=23, title="Investigate carbon credit opportunities", owner="Eric", week=4,
         description="Research methane capture carbon offset credits. Reach out to Microsoft, Google, ESG buyers.",
         category="Revenue", priority="medium",
         notes="Additional revenue: $10-50 per ton CO2e. High-margin opportunity."),
]


class ActionTracker:
    """Main class for managing action items."""
    
    def __init__(self, data_file: str = "carbon_cut_tasks.json"):
        self.data_file = Path(data_file)
        self.tasks: List[Task] = []
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from JSON file or initialize with defaults."""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.tasks = [Task(**task) for task in data]
        else:
            # Initialize with all tasks
            self.tasks = DEFAULT_TASKS + ADDITIONAL_TASKS
            self._save_tasks()
    
    def _save_tasks(self):
        """Persist tasks to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump([asdict(t) for t in self.tasks], f, indent=2)
    
    def get_tasks(self, owner: Optional[str] = None, week: Optional[int] = None, 
                  status: Optional[str] = None) -> List[Task]:
        """Filter tasks by criteria."""
        result = self.tasks
        
        if owner and owner.lower() != "all":
            result = [t for t in result if t.owner.lower() == owner.lower()]
        
        if week:
            result = [t for t in result if t.week == week]
        
        if status:
            result = [t for t in result if t.status.lower() == status.lower()]
        
        return sorted(result, key=lambda t: (t.week, t.id))
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as complete."""
        for task in self.tasks:
            if task.id == task_id:
                task.status = "complete"
                task.completed_date = datetime.now().isoformat()
                self._save_tasks()
                return True
        return False
    
    def update_status(self, task_id: int, status: str) -> bool:
        """Update task status."""
        valid_statuses = ["pending", "in_progress", "complete", "blocked"]
        if status not in valid_statuses:
            print(f"Invalid status. Use: {', '.join(valid_statuses)}")
            return False
        
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                if status == "complete":
                    task.completed_date = datetime.now().isoformat()
                self._save_tasks()
                return True
        return False
    
    def add_note(self, task_id: int, note: str) -> bool:
        """Add a note to a task."""
        for task in self.tasks:
            if task.id == task_id:
                timestamp = datetime.now().strftime("%Y-%m-%d")
                task.notes = f"{task.notes}\n[{timestamp}] {note}".strip()
                self._save_tasks()
                return True
        return False
    
    def check_reminders(self) -> List[Task]:
        """Check for overdue or critical tasks needing attention."""
        reminders = []
        for task in self.tasks:
            if task.status == "complete":
                continue
            
            # Critical tasks are always reminded
            if task.priority == "critical":
                reminders.append(task)
            # Blocked tasks need attention
            elif task.status == "blocked":
                reminders.append(task)
        
        return reminders
    
    def get_stats(self) -> dict:
        """Get completion statistics."""
        total = len(self.tasks)
        complete = len([t for t in self.tasks if t.status == "complete"])
        pending = len([t for t in self.tasks if t.status == "pending"])
        in_progress = len([t for t in self.tasks if t.status == "in_progress"])
        blocked = len([t for t in self.tasks if t.status == "blocked"])
        
        by_owner = {}
        for task in self.tasks:
            by_owner.setdefault(task.owner, {"total": 0, "complete": 0})
            by_owner[task.owner]["total"] += 1
            if task.status == "complete":
                by_owner[task.owner]["complete"] += 1
        
        by_week = {}
        for task in self.tasks:
            by_week.setdefault(task.week, {"total": 0, "complete": 0})
            by_week[task.week]["total"] += 1
            if task.status == "complete":
                by_week[task.week]["complete"] += 1
        
        return {
            "total": total,
            "complete": complete,
            "pending": pending,
            "in_progress": in_progress,
            "blocked": blocked,
            "percent_complete": round(complete / total * 100, 1) if total > 0 else 0,
            "by_owner": by_owner,
            "by_week": by_week
        }
    
    def export_csv(self, filename: str = "carbon_cut_tasks.csv"):
        """Export tasks to CSV."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Owner', 'Week', 'Status', 'Priority', 
                           'Category', 'Description', 'Notes', 'Completed Date'])
            for task in self.tasks:
                writer.writerow([task.id, task.title, task.owner, task.week, 
                               task.status, task.priority, task.category,
                               task.description, task.notes, task.completed_date])
        return filename
    
    def display_tasks(self, tasks: List[Task], show_details: bool = False):
        """Pretty print tasks."""
        if not tasks:
            print("\n📭 No tasks found matching criteria.")
            return
        
        print(f"\n{'=' * 90}")
        print(f"{'ID':<4} {'Status':<12} {'Owner':<8} {'Week':<15} {'Priority':<10} {'Title'}")
        print(f"{'-' * 90}")
        
        status_icons = {
            "pending": "⏳",
            "in_progress": "🔄",
            "complete": "✅",
            "blocked": "🚫"
        }
        
        priority_colors = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }
        
        for task in tasks:
            icon = status_icons.get(task.status, "⏳")
            priority_icon = priority_colors.get(task.priority, "⚪")
            week_label = f"W{task.week}"
            
            print(f"{task.id:<4} {icon} {task.status:<10} {task.owner:<8} {week_label:<15} "
                  f"{priority_icon} {task.priority:<8} {task.title}")
            
            if show_details:
                print(f"    📁 Category: {task.category}")
                print(f"    📝 Description: {task.description}")
                if task.notes:
                    print(f"    📌 Notes: {task.notes}")
                if task.completed_date:
                    print(f"    ✅ Completed: {task.completed_date}")
                print()
        
        print(f"{'=' * 90}")
        print(f"Showing {len(tasks)} task(s)\n")
    
    def display_stats(self):
        """Display completion statistics."""
        stats = self.get_stats()
        
        print("\n" + "=" * 60)
        print("📊 CARBON CUT SOLUTIONS - ACTION PLAN DASHBOARD")
        print("=" * 60)
        
        print(f"\n📈 OVERALL PROGRESS: {stats['percent_complete']}% ({stats['complete']}/{stats['total']})")
        print(f"   ✅ Complete: {stats['complete']}")
        print(f"   🔄 In Progress: {stats['in_progress']}")
        print(f"   ⏳ Pending: {stats['pending']}")
        print(f"   🚫 Blocked: {stats['blocked']}")
        
        print("\n📋 BY OWNER:")
        for owner, data in sorted(stats['by_owner'].items()):
            pct = round(data['complete'] / data['total'] * 100, 1)
            print(f"   {owner:<6}: {pct:>5}% ({data['complete']}/{data['total']})")
        
        print("\n📅 BY WEEK:")
        for week, data in sorted(stats['by_week'].items()):
            pct = round(data['complete'] / data['total'] * 100, 1)
            status = "✅" if pct == 100 else "⏳"
            print(f"   Week {week}: {status} {pct:>5}% ({data['complete']}/{data['total']})")
        
        print("\n" + "=" * 60)
    
    def display_reminders(self):
        """Display overdue reminders."""
        reminders = self.check_reminders()
        
        if not reminders:
            print("\n🎉 No critical reminders! All up to date.")
            return
        
        print("\n" + "=" * 60)
        print("⏰ REMINDERS - TASKS REQUIRING ATTENTION")
        print("=" * 60)
        
        critical = [t for t in reminders if t.priority == "critical" and t.status != "complete"]
        blocked = [t for t in reminders if t.status == "blocked"]
        
        if critical:
            print(f"\n🔴 CRITICAL TASKS ({len(critical)}):")
            for task in critical:
                print(f"   [{task.id}] {task.owner} - Week {task.week}: {task.title}")
        
        if blocked:
            print(f"\n🚫 BLOCKED TASKS ({len(blocked)}):")
            for task in blocked:
                print(f"   [{task.id}] {task.owner}: {task.title}")
                if task.notes:
                    print(f"       Note: {task.notes}")
        
        print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Carbon Cut Solutions Action Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python carbon_cut_tracker.py                     # Show all tasks
  python carbon_cut_tracker.py --owner Nick       # Show Nick's tasks
  python carbon_cut_tracker.py --week 1           # Show Week 1 tasks
  python carbon_cut_tracker.py --complete 5       # Mark task 5 complete
  python carbon_cut_tracker.py --status 5 blocked # Mark task 5 blocked
  python carbon_cut_tracker.py --stats            # Show dashboard
  python carbon_cut_tracker.py --reminders        # Check reminders
  python carbon_cut_tracker.py --export           # Export to CSV
        """
    )
    
    parser.add_argument("--owner", help="Filter by owner (Kos, Nick, Eric, All)")
    parser.add_argument("--week", type=int, help="Filter by week (1-4)")
    parser.add_argument("--status", help="Update task status (pending, in_progress, complete, blocked)")
    parser.add_argument("--complete", type=int, metavar="ID", help="Mark task as complete")
    parser.add_argument("--add-note", nargs=2, metavar=("ID", "NOTE"), help="Add note to task")
    parser.add_argument("--stats", action="store_true", help="Show statistics dashboard")
    parser.add_argument("--reminders", action="store_true", help="Check for reminders")
    parser.add_argument("--export", action="store_true", help="Export to CSV")
    parser.add_argument("--details", action="store_true", help="Show full task details")
    
    args = parser.parse_args()
    
    tracker = ActionTracker()
    
    # Handle status updates
    if args.complete:
        if tracker.complete_task(args.complete):
            print(f"✅ Task {args.complete} marked as complete!")
        else:
            print(f"❌ Task {args.complete} not found.")
        return
    
    if args.status and len(args.status.split()) == 2:
        # Parse: --status "5 blocked" format
        parts = args.status.split()
        if len(parts) == 2:
            try:
                task_id = int(parts[0])
                new_status = parts[1]
                if tracker.update_status(task_id, new_status):
                    print(f"📝 Task {task_id} status updated to: {new_status}")
                else:
                    print(f"❌ Task {task_id} not found.")
                return
            except ValueError:
                pass
    
    if args.add_note:
        task_id = int(args.add_note[0])
        note = args.add_note[1]
        if tracker.add_note(task_id, note):
            print(f"📝 Note added to task {task_id}")
        else:
            print(f"❌ Task {task_id} not found.")
        return
    
    # Handle display modes
    if args.stats:
        tracker.display_stats()
        return
    
    if args.reminders:
        tracker.display_reminders()
        return
    
    if args.export:
        filename = tracker.export_csv()
        print(f"📁 Exported to {filename}")
        return
    
    # Default: display tasks
    tasks = tracker.get_tasks(owner=args.owner, week=args.week)
    tracker.display_tasks(tasks, show_details=args.details)


if __name__ == "__main__":
    main()
