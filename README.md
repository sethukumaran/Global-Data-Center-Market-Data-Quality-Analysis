# Global-Data-Center-Market-Data-Quality-Analysis

## Project objective
Analyze the supplied data-center datasets from a senior business-analytics perspective, combining facility inventory, country summaries and externally reported country totals.

## Dataset scope
- `data_centers.csv`: 4,802 facility-level records.
- `country_summary.csv`: 116 country-level records.
- `reported_totals.csv`: 71 reported-total records across two source snapshots.

## Executive findings
1. The United States has **1,789 mapped facilities**, followed by France (371), Germany (300), the United Kingdom (293) and the Netherlands (167).
2. North America has **1,926 mapped facilities** and about **39.4M m²** of mapped footprint; Europe has 1,813 facilities and about 13.4M m².
3. **67.2%** of facility records are classified as `unclassified`, making facility-type market-share conclusions directional rather than complete.
4. The largest mapped operators by facility count include AWS (299), Equinix (177), Digital Realty (175), Microsoft (125) and Google (89).
5. Metadata coverage is uneven: name 76.4%, operator 60.1%, footprint 81.1%, city 34.7%, start date 4.0%.
6. Median mapped footprint is about **5,661 m²**, compared with a mean of about **17,391 m²**; the maximum is about **7.04M m²**, indicating strong right-skew.
7. The latest reported-vs-mapped comparison shows large gaps in several major markets, including the U.S. (+2,299), China (+244), U.K. (+213), Germany (+207) and India (+205).
8. These source gaps should be treated as reconciliation/coverage/definition issues, not automatically as evidence that either source is wrong.

## Business insights
### Geographic concentration
Data-center infrastructure is highly concentrated geographically. This matters for power availability, network connectivity, customer proximity, land, regulation and infrastructure planning.

### Market segmentation
Colocation and hyperscale are important classified segments, but the very large unclassified population means the segment mix should not be treated as a complete market-share estimate.

### Operator landscape
Operator counts show a concentrated presence among major global infrastructure providers. Operator footprint should be analyzed alongside facility count because site size varies substantially.

### Data-quality opportunity
The most valuable enrichment actions are:
1. classify unclassified facilities;
2. improve operator attribution;
3. improve city/state/postcode coverage;
4. standardize names;
5. increase start-date coverage;
6. validate extreme footprint values;
7. establish a repeatable reconciliation process between mapped and reported counts.

## Python
`src/data_center_analysis.py` performs:
- schema and data-type inspection
- missing-value analysis
- duplicate checks
- descriptive statistics
- country, continent, facility-type and operator analysis
- metadata completeness analysis
- latest reported-vs-mapped comparison
- eight business visualizations
- CSV output tables

## SQL
`sql/business_analysis.sql` contains 18 analytical queries covering inventory, market structure, footprint, metadata quality, operators, source reconciliation, location completeness and exception reporting.

## Visualizations
The `outputs/charts/` folder contains:
1. Top countries
2. Facility type mix
3. Facilities by continent
4. Top operators
5. Reported-vs-mapped gaps
6. Footprint distribution
7. Country footprint
8. Operator footprint

## Key business insights
- 4,802 mapped data-center facilities are present in the facility-level dataset.
- The United States has 1,789 mapped facilities, followed by France (371), Germany (300), UK (293), and Netherlands (167).
- North America contains 1,926 mapped facilities and approximately 39.4M m² of mapped footprint.
- 67.2% of facilities are unclassified, which is the biggest limitation for detailed market-segmentation analysis.
- Major operators by mapped facility count include AWS (299), Equinix (177), Digital Realty (175), Microsoft (125), and Google (89).
- Metadata completeness is uneven:
  Name: 76.4%
  Operator: 60.1%
  Footprint: 81.1%
  City: 34.7%
  Start date: 4.0%
- Median facility footprint is approximately 5,661 m², while the mean is approximately 17,391 m², indicating strong right-skew.
- External reported totals differ substantially from mapped counts. For example, the latest comparison shows:
  United States: +2,299
  China: +244
  UK: +213
  Germany: +207
  India: +205
These differences should be interpreted as source/definition/coverage differences, not automatically as evidence that one source is incorrect.

## Senior analyst conclusion
This dataset is strongest as a **global infrastructure inventory and market-screening layer**. It provides useful directional evidence on geographic concentration, operator presence and physical footprint.
Its biggest limitation is metadata completeness: classification, operator, city and development-date fields contain substantial gaps. Therefore, it should not be used alone for precise market sizing, development-pipeline estimation or investment decisions.
The external reported totals provide a valuable reconciliation layer. The observed differences identify countries where definitions, mapping completeness, update timing or source methodology need investigation.

However, before using it for high-confidence market sizing, competitive market share, investment analysis, or development-pipeline forecasting, the biggest priorities should be:
- Reduce the 67.2% unclassified population.
- Improve operator attribution.
- Improve city/geographic metadata.
- Validate extreme footprint values.
- Increase construction/start-date coverage.
- Establish a formal reconciliation process between mapped and externally reported facility counts.

