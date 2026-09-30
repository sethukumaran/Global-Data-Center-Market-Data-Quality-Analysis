-- Global Data Center Market Analysis

-- 1. Overall inventory
SELECT COUNT(*) AS total_facilities FROM data_centers;

-- 2. Country ranking
SELECT country, COUNT(*) AS facilities
FROM data_centers
GROUP BY country
ORDER BY facilities DESC;

-- 3. Continent ranking
SELECT continent, COUNT(*) AS facilities
FROM data_centers
GROUP BY continent
ORDER BY facilities DESC;

-- 4. Facility type mix
SELECT facility_kind, COUNT(*) AS facilities,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),2) AS share_pct
FROM data_centers
GROUP BY facility_kind
ORDER BY facilities DESC;

-- 5. Country footprint
SELECT country, COUNT(*) AS facilities,
       SUM(footprint_area_m2) AS total_footprint_m2,
       AVG(footprint_area_m2) AS avg_footprint_m2,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY footprint_area_m2) AS median_footprint_m2
FROM data_centers
WHERE footprint_area_m2 IS NOT NULL
GROUP BY country
ORDER BY total_footprint_m2 DESC;

-- 6. Overall metadata completeness
SELECT COUNT(*) AS total_rows,
       ROUND(100.0*COUNT(name)/COUNT(*),2) AS name_coverage_pct,
       ROUND(100.0*COUNT(operator)/COUNT(*),2) AS operator_coverage_pct,
       ROUND(100.0*COUNT(city)/COUNT(*),2) AS city_coverage_pct,
       ROUND(100.0*COUNT(footprint_area_m2)/COUNT(*),2) AS footprint_coverage_pct
FROM data_centers;

-- 7. Countries with high unclassified exposure
SELECT country, COUNT(*) AS facilities,
       SUM(CASE WHEN facility_kind='unclassified' THEN 1 ELSE 0 END) AS unclassified,
       ROUND(100.0*SUM(CASE WHEN facility_kind='unclassified' THEN 1 ELSE 0 END)/COUNT(*),2) AS unclassified_pct
FROM data_centers
GROUP BY country
HAVING COUNT(*) >= 10
ORDER BY unclassified_pct DESC;

-- 8. Top operators by facility count
SELECT operator, COUNT(*) AS facilities
FROM data_centers
WHERE operator IS NOT NULL
GROUP BY operator
ORDER BY facilities DESC
LIMIT 20;

-- 9. Top operators by footprint
SELECT operator, COUNT(*) AS facilities, SUM(footprint_area_m2) AS footprint_m2
FROM data_centers
WHERE operator IS NOT NULL
GROUP BY operator
ORDER BY footprint_m2 DESC NULLS LAST
LIMIT 20;

-- 10. Facility size bands
SELECT CASE
         WHEN footprint_area_m2 < 1000 THEN '<1K m²'
         WHEN footprint_area_m2 < 5000 THEN '1K–5K m²'
         WHEN footprint_area_m2 < 10000 THEN '5K–10K m²'
         WHEN footprint_area_m2 < 50000 THEN '10K–50K m²'
         WHEN footprint_area_m2 < 200000 THEN '50K–200K m²'
         ELSE '200K+ m²'
       END AS size_band,
       COUNT(*) AS facilities
FROM data_centers
WHERE footprint_area_m2 IS NOT NULL
GROUP BY size_band
ORDER BY facilities DESC;

-- 11. Latest reported-vs-mapped comparison
WITH latest_report AS (
    SELECT DISTINCT ON (country_iso3)
           country_iso3, reported_facilities, as_of, source_url
    FROM reported_totals
    ORDER BY country_iso3, as_of DESC
)
SELECT c.country, c.osm_facilities, r.reported_facilities,
       r.reported_facilities-c.osm_facilities AS reported_minus_osm,
       ROUND(r.reported_facilities::numeric/NULLIF(c.osm_facilities,0),2)
           AS reported_to_osm_ratio,
       r.as_of
FROM country_summary c
JOIN latest_report r ON c.country_iso3=r.country_iso3
ORDER BY reported_minus_osm DESC;

-- 12. Mapped count exceeds reported count
WITH latest_report AS (
    SELECT DISTINCT ON (country_iso3) country_iso3, reported_facilities, as_of
    FROM reported_totals
    ORDER BY country_iso3, as_of DESC
)
SELECT c.country, c.osm_facilities, r.reported_facilities,
       c.osm_facilities-r.reported_facilities AS mapped_excess
FROM country_summary c
JOIN latest_report r ON c.country_iso3=r.country_iso3
WHERE c.osm_facilities > r.reported_facilities
ORDER BY mapped_excess DESC;

-- 13. Facility types by continent
SELECT continent, facility_kind, COUNT(*) AS facilities
FROM data_centers
GROUP BY continent, facility_kind
ORDER BY continent, facilities DESC;

-- 14. Operators with high average footprint
SELECT operator, COUNT(*) AS facilities,
       SUM(footprint_area_m2) AS footprint_m2,
       SUM(footprint_area_m2)/NULLIF(COUNT(footprint_area_m2),0) AS avg_footprint_m2
FROM data_centers
WHERE operator IS NOT NULL
GROUP BY operator
HAVING COUNT(footprint_area_m2) >= 5
ORDER BY avg_footprint_m2 DESC
LIMIT 20;

-- 15. Location completeness by country
SELECT country, COUNT(*) AS facilities,
       ROUND(100.0*COUNT(city)/COUNT(*),1) AS city_coverage_pct,
       ROUND(100.0*COUNT(state)/COUNT(*),1) AS state_coverage_pct,
       ROUND(100.0*COUNT(postcode)/COUNT(*),1) AS postcode_coverage_pct,
       ROUND(100.0*COUNT(street)/COUNT(*),1) AS street_coverage_pct
FROM data_centers
GROUP BY country
HAVING COUNT(*) >= 10
ORDER BY city_coverage_pct DESC;

-- 16. Start-year analysis
SELECT EXTRACT(YEAR FROM CAST(start_date AS DATE)) AS start_year,
       COUNT(*) AS facilities
FROM data_centers
WHERE start_date IS NOT NULL
GROUP BY start_year
ORDER BY start_year;

-- 17. Data-quality exception queue
SELECT osm_id, country, name, operator, city, facility_kind, footprint_area_m2
FROM data_centers
WHERE name IS NULL OR operator IS NULL OR city IS NULL OR footprint_area_m2 IS NULL
ORDER BY country, osm_id;

-- 18. Countries by average mapped footprint
SELECT country, COUNT(*) AS facilities,
       SUM(footprint_area_m2) AS total_footprint_m2,
       SUM(footprint_area_m2)/NULLIF(COUNT(footprint_area_m2),0) AS avg_footprint_m2
FROM data_centers
WHERE footprint_area_m2 IS NOT NULL
GROUP BY country
HAVING COUNT(footprint_area_m2) >= 5
ORDER BY avg_footprint_m2 DESC;
