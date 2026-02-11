#!/usr/bin/env python3
"""
Orphan Well Bid Analysis Tool
Analyzes winning bids for orphan well plugging contracts in PA and OH (2021-2025)
"""

import json
import csv
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import os

@dataclass
class OrphanWellContract:
    """Represents a single orphan well plugging contract"""
    state: str
    year: int
    contract_id: str
    contractor: str
    county: str
    num_wells: int
    winning_bid: float
    bid_per_well: float
    date_awarded: str
    source: str
    notes: str = ""

@dataclass
class ContractSummary:
    """Summary statistics for contracts"""
    total_contracts: int
    total_wells: int
    total_value: float
    avg_bid_per_well: float
    top_contractors: Dict[str, int]
    avg_contract_value: float

class OrphanWellAnalyzer:
    def __init__(self):
        self.pa_contracts: List[OrphanWellContract] = []
        self.oh_contracts: List[OrphanWellContract] = []
        
    def add_contract(self, contract: OrphanWellContract):
        """Add a contract to the analyzer"""
        if contract.state == "PA":
            self.pa_contracts.append(contract)
        elif contract.state == "OH":
            self.oh_contracts.append(contract)
    
    def load_from_json(self, filepath: str):
        """Load contracts from JSON file"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                for item in data:
                    contract = OrphanWellContract(**item)
                    self.add_contract(contract)
    
    def load_from_csv(self, filepath: str):
        """Load contracts from CSV file"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['winning_bid'] = float(row['winning_bid'])
                    row['bid_per_well'] = float(row['bid_per_well'])
                    row['num_wells'] = int(row['num_wells'])
                    row['year'] = int(row['year'])
                    contract = OrphanWellContract(**row)
                    self.add_contract(contract)
    
    def save_to_json(self, filepath: str):
        """Save all contracts to JSON file"""
        all_contracts = [asdict(c) for c in self.pa_contracts + self.oh_contracts]
        with open(filepath, 'w') as f:
            json.dump(all_contracts, f, indent=2)
    
    def get_summary(self, state: Optional[str] = None) -> ContractSummary:
        """Get summary statistics"""
        contracts = []
        if state == "PA":
            contracts = self.pa_contracts
        elif state == "OH":
            contracts = self.oh_contracts
        else:
            contracts = self.pa_contracts + self.oh_contracts
        
        if not contracts:
            return ContractSummary(0, 0, 0, 0, {}, 0)
        
        total_value = sum(c.winning_bid for c in contracts)
        total_wells = sum((c.num_wells or 0) for c in contracts)
        
        # Count contracts per contractor
        contractor_counts = {}
        for c in contracts:
            contractor_counts[c.contractor] = contractor_counts.get(c.contractor, 0) + 1
        
        return ContractSummary(
            total_contracts=len(contracts),
            total_wells=total_wells,
            total_value=total_value,
            avg_bid_per_well=total_value / total_wells if total_wells > 0 else sum((c.bid_per_well or 0) for c in contracts) / len([c for c in contracts if c.bid_per_well]) if any(c.bid_per_well for c in contracts) else 0,
            top_contractors=dict(sorted(contractor_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            avg_contract_value=total_value / len(contracts)
        )
    
    def generate_report(self, state: Optional[str] = None) -> str:
        """Generate a text report"""
        summary = self.get_summary(state)
        contracts = []
        if state == "PA":
            contracts = self.pa_contracts
        elif state == "OH":
            contracts = self.oh_contracts
        else:
            contracts = self.pa_contracts + self.oh_contracts
        
        report = []
        report.append("=" * 80)
        report.append("ORPHAN WELL BID ANALYSIS REPORT")
        report.append(f"State: {state if state else 'PA + OH'}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        report.append("SUMMARY STATISTICS")
        report.append("-" * 40)
        report.append(f"Total Contracts: {summary.total_contracts}")
        report.append(f"Total Wells Plugged: {summary.total_wells:,}")
        report.append(f"Total Contract Value: ${summary.total_value:,.2f}")
        report.append(f"Average Bid Per Well: ${summary.avg_bid_per_well:,.2f}")
        report.append(f"Average Contract Value: ${summary.avg_contract_value:,.2f}")
        report.append("")
        report.append("TOP CONTRACTORS (by number of contracts)")
        report.append("-" * 40)
        for contractor, count in summary.top_contractors.items():
            report.append(f"  {contractor}: {count} contracts")
        report.append("")
        report.append("ALL CONTRACTS")
        report.append("-" * 40)
        for c in sorted(contracts, key=lambda x: (-x.year, -x.winning_bid)):
            report.append(f"  [{c.year}] {c.contractor}")
            report.append(f"      County: {c.county} | Wells: {c.num_wells}")
            bid_per_well_str = f"${c.bid_per_well:,.2f}/well" if c.bid_per_well else "TBD"
            report.append(f"      Bid: ${c.winning_bid:,.2f} ({bid_per_well_str})")
            report.append(f"      ID: {c.contractor} | {c.date_awarded}")
            report.append("")
        
        return "\n".join(report)
    
    def export_winning_bids_csv(self, filepath: str):
        """Export winning bids to CSV for analysis in Excel/Numbers"""
        contracts = self.pa_contracts + self.oh_contracts
        with open(filepath, 'w', newline='') as f:
            fieldnames = ['state', 'year', 'contract_id', 'contractor', 'county', 
                         'num_wells', 'winning_bid', 'bid_per_well', 'date_awarded', 'source', 'notes']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in contracts:
                writer.writerow(asdict(c))

# Pennsylvania Data (from research)
PA_INITIAL_DATA = [
    # 2022 - Initial $25M Grant, 13 contracts, 227 wells
    {"state": "PA", "year": 2022, "contract_id": "PA-2022-001", "contractor": "TBD - DEP Awarded 13 Contracts", 
     "county": "Various", "num_wells": 227, "winning_bid": 25000000.00, "bid_per_well": 110132.16, 
     "date_awarded": "2022-08-25", "source": "PA DEP IIJA Report", "notes": "Initial Grant - 13 contracts"},
    
    # 2023 - Additional contracts
    {"state": "PA", "year": 2023, "contract_id": "PA-2023-001", "contractor": "DK Construction Services, LLC", 
     "county": "Various", "num_wells": None, "winning_bid": 420000.00, "bid_per_well": None, 
     "date_awarded": "2025-01-08", "source": "PA DGS Bids", "notes": "Recent award"},
    
    {"state": "PA", "year": 2023, "contract_id": "PA-2023-002", "contractor": "Fred L Burns, Inc.", 
     "county": "Various", "num_wells": None, "winning_bid": 402600.00, "bid_per_well": None, 
     "date_awarded": "2024-12-12", "source": "PA DGS Bids", "notes": "Recent award"},
    
    # 2024 - Formula Grant $76M
    {"state": "PA", "year": 2024, "contract_id": "PA-2024-FORMULA", "contractor": "Pending Awards", 
     "county": "Various", "num_wells": 0, "winning_bid": 76406474.00, "bid_per_well": None, 
     "date_awarded": "Pending", "source": "PA DEP IIJA", "notes": "Formula Grant 1 - $76.4M applied Dec 2023, awaiting approval"},
]

# Ohio Data (from research)
OH_INITIAL_DATA = [
    # 2022 - Initial $25M Grant
    {"state": "OH", "year": 2022, "contract_id": "OH-2022-INIT", "contractor": "2 Construction Managers", 
     "county": "Various", "num_wells": None, "winning_bid": 22000000.00, "bid_per_well": None, 
     "date_awarded": "2022-10", "source": "Ohio River Valley Institute", 
     "notes": "Initial Grant - 2 CMs at $11M each over 4 years"},
    
    # 2023 - Phase 1 Formula Grant $57.7M
    {"state": "OH", "year": 2023, "contract_id": "OH-2023-FORMULA", "contractor": "Various Contractors", 
     "county": "Various", "num_wells": None, "winning_bid": 57700000.00, "bid_per_well": None, 
     "date_awarded": "2023-07", "source": "Ohio Capital Journal", "notes": "Phase 1 Formula Grant"},
    
    # 2024 - Traditional Program
    {"state": "OH", "year": 2024, "contract_id": "OH-2024-001", "contractor": "Various", 
     "county": "Various", "num_wells": 346, "winning_bid": 36808068.29, "bid_per_well": 106381.41, 
     "date_awarded": "2024", "source": "ODNR 2024 Annual Report", 
     "notes": "Traditional Program - 346 wells at $36.8M"},
    
    # Active bid examples from cleat.ai
    {"state": "OH", "year": 2024, "contract_id": "OH-2024-VINTON-4", "contractor": "TBD", 
     "county": "Vinton", "num_wells": 10, "winning_bid": 0.00, "bid_per_well": None, 
     "date_awarded": "Open Bid", "source": "CLEAT/ODNR", "notes": "10 wells - Vinton County #4"},
    
    {"state": "OH", "year": 2024, "contract_id": "OH-2024-BELMONT-7", "contractor": "TBD", 
     "county": "Belmont", "num_wells": 4, "winning_bid": 0.00, "bid_per_well": None, 
     "date_awarded": "Open Bid", "source": "CLEAT/ODNR", "notes": "4 wells - Belmont County #7"},
    
    {"state": "OH", "year": 2024, "contract_id": "OH-2024-MORROW-9", "contractor": "TBD", 
     "county": "Morrow", "num_wells": 3, "winning_bid": 0.00, "bid_per_well": None, 
     "date_awarded": "Open Bid", "source": "CLEAT/ODNR", "notes": "3 wells - Morrow County"},
]

def main():
    """Main function to demonstrate the analyzer"""
    analyzer = OrphanWellAnalyzer()
    
    # Load initial data
    for item in PA_INITIAL_DATA:
        analyzer.add_contract(OrphanWellContract(**item))
    
    for item in OH_INITIAL_DATA:
        analyzer.add_contract(OrphanWellContract(**item))
    
    # Save to files
    analyzer.save_to_json("orphan_well_data.json")
    analyzer.export_winning_bids_csv("orphan_well_bids.csv")
    
    # Generate reports
    print(analyzer.generate_report("PA"))
    print("\n" + "=" * 80 + "\n")
    print(analyzer.generate_report("OH"))
    
    print("\n" + "=" * 80)
    print("Files generated:")
    print("  - orphan_well_data.json (full dataset)")
    print("  - orphan_well_bids.csv (Excel-ready)")
    print("=" * 80)

if __name__ == "__main__":
    main()