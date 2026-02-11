# Orphan Well Bid Analysis Tool

Analyzes winning bids for orphan well plugging contracts in Pennsylvania and Ohio (2021-2025).

## Files Generated

| File | Description |
|------|-------------|
| `orphan_well_analyzer.py` | Main Python tool |
| `orphan_well_data.json` | Full dataset in JSON format |
| `orphan_well_bids.csv` | Excel-ready CSV with all contracts |
| `PA_contracts.json` | Pennsylvania-only data |
| `OH_contracts.json` | Ohio-only data |

## Usage

```bash
# Run the analyzer
python3 orphan_well_analyzer.py

# Import into your own scripts
from orphan_well_analyzer import OrphanWellAnalyzer, OrphanWellContract

analyzer = OrphanWellAnalyzer()
analyzer.load_from_json("orphan_well_data.json")

# Get summary statistics
summary = analyzer.get_summary("PA")  # or "OH" or None for both
print(f"Total Value: ${summary.total_value:,.2f}")
print(f"Avg Bid/Well: ${summary.avg_bid_per_well:,.2f}")

# Generate report
print(analyzer.generate_report())

# Export to CSV for Excel
analyzer.export_winning_bids_csv("my_analysis.csv")
```

## Data Sources

### Pennsylvania
- **PA DEP IIJA Project Tracker** - https://www.pa.gov/agencies/dep/programs-and-services/oil-and-gas/legacy-wells/infrastructure-investment-and-jobs-act-iija
- **Initial Grant:** $25M (Aug 2022) → 13 contracts, 227 wells
- **Formula Grant:** $76.4M (applied Dec 2023, pending)
- **Performance Grant:** Up to $40M available

### Ohio
- **ODNR Orphan Well Program** - https://dx-stg.ohio.gov/wps/portal/gov/odnr/discover-and-learn/safety-conservation/about-ODNR/oil-gas/orphan-wells
- **Initial Grant:** $25M (Oct 2022)
- **Phase 1 Formula:** $57.7M (July 2023)
- **2024 Traditional Program:** 346 wells at $36.8M ($106,381/well avg)
- **Eligible through 2030:** Up to $326M total

## Key Findings (from available data)

| Metric | Pennsylvania | Ohio |
|--------|-------------|------|
| Total Contract Value | $102.2M | $116.5M |
| Wells Plugged (confirmed) | 227 | 346 |
| Avg Bid/Well | $110,132 | $106,381 |
| Top Contractors | 13 firms (2022 batch) | 44 approved, 20 active |

## To Do / Next Steps

- [ ] Access "antigravity" data source for complete bid data
- [ ] Pull PA DEP contract awards database directly
- [ ] Integrate Ohio's active bid portal (CLEAT)
- [ ] Add mapping/visualization of wells by county
- [ ] Calculate ROI analysis for contractors

## Contact

Questions? Reach out to Kos for data access requests.