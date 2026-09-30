"""
Global Data Center Market Analysis

"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(BASE,"data"); OUT=os.path.join(BASE,"outputs")
CHART=os.path.join(OUT,"charts"); TABLE=os.path.join(OUT,"tables")
os.makedirs(CHART,exist_ok=True); os.makedirs(TABLE,exist_ok=True)

country_summary=pd.read_csv(os.path.join(DATA,"country_summary.csv"))
data_centers=pd.read_csv(os.path.join(DATA,"data_centers.csv"))
reported=pd.read_csv(os.path.join(DATA,"reported_totals.csv"))

print("Shapes:", country_summary.shape, data_centers.shape, reported.shape)
print("\nMissing values:\n", data_centers.isna().sum().sort_values(ascending=False))
print("\nDuplicate osm_id:", data_centers["osm_id"].duplicated().sum())
print("\nNumeric summary:\n", data_centers[["latitude","longitude","footprint_area_m2","building_levels"]].describe())

# Feature engineering
data_centers["has_name"]=data_centers["name"].notna()
data_centers["has_operator"]=data_centers["operator"].notna()
data_centers["has_city"]=data_centers["city"].notna()
data_centers["has_footprint"]=data_centers["footprint_area_m2"].notna()
data_centers["start_date_parsed"]=pd.to_datetime(data_centers["start_date"],errors="coerce")
data_centers["start_year"]=data_centers["start_date_parsed"].dt.year

# Country analysis
country_rank=country_summary.sort_values("osm_facilities",ascending=False)
country_rank.to_csv(os.path.join(TABLE,"country_rank.csv"),index=False)
print("\nTop countries:\n",country_rank.head(15).to_string(index=False))

# Facility type
facility_type=data_centers["facility_kind"].value_counts().rename_axis("facility_kind").reset_index(name="facilities")
facility_type["share_pct"]=facility_type["facilities"]/len(data_centers)*100
facility_type.to_csv(os.path.join(TABLE,"facility_type_mix.csv"),index=False)
print("\nFacility types:\n",facility_type.to_string(index=False))

# Geography
continent=(data_centers.groupby("continent",dropna=False)
           .agg(facilities=("osm_id","count"),footprint_m2=("footprint_area_m2","sum"),
                median_footprint_m2=("footprint_area_m2","median"))
           .reset_index().sort_values("facilities",ascending=False))
continent.to_csv(os.path.join(TABLE,"continent_summary.csv"),index=False)

# Operators
operators=(data_centers.dropna(subset=["operator"]).groupby("operator")
           .agg(facilities=("osm_id","size"),footprint_m2=("footprint_area_m2","sum"))
           .reset_index().sort_values("facilities",ascending=False))
operators.to_csv(os.path.join(TABLE,"operator_summary.csv"),index=False)

# Data quality
cols=["name","operator","city","state","postcode","street","footprint_area_m2",
      "building_levels","height_m","start_date","website","wikidata","wikipedia"]
quality=pd.DataFrame({"column":cols})
quality["non_null_count"]=[data_centers[c].notna().sum() for c in cols]
quality["missing_count"]=len(data_centers)-quality["non_null_count"]
quality["coverage_pct"]=quality["non_null_count"]/len(data_centers)*100
quality.to_csv(os.path.join(TABLE,"data_quality.csv"),index=False)

# Latest external source snapshot by country
reported["as_of_parsed"]=pd.to_datetime(reported["as_of"],format="mixed",errors="coerce")
latest=(reported.sort_values("as_of_parsed").groupby("country_iso3",as_index=False).tail(1))
comparison=country_summary.merge(latest[["country_iso3","reported_facilities","as_of","tracker","source_url"]],
                                 on="country_iso3",how="inner")
comparison["reported_minus_osm"]=comparison["reported_facilities"]-comparison["osm_facilities"]
comparison["reported_to_osm_ratio"]=comparison["reported_facilities"]/comparison["osm_facilities"].replace(0,np.nan)
comparison.to_csv(os.path.join(TABLE,"reported_vs_osm_latest.csv"),index=False)
print("\nLargest source gaps:\n",
      comparison.sort_values("reported_minus_osm",ascending=False)
      [["country","osm_facilities","reported_facilities","reported_minus_osm","reported_to_osm_ratio"]]
      .head(15).to_string(index=False))

# Visualization helper
def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(CHART,name),dpi=180,bbox_inches="tight")
    plt.close()

x=country_rank.head(15).sort_values("osm_facilities")
plt.figure(figsize=(10,6)); plt.barh(x["country"],x["osm_facilities"])
plt.title("Top countries by mapped data-center facilities"); plt.xlabel("Mapped facilities"); save("01_top_countries.png")

x=facility_type.sort_values("facilities")
plt.figure(figsize=(10,6)); plt.barh(x["facility_kind"],x["facilities"])
plt.title("Facility type mix"); plt.xlabel("Facilities"); save("02_facility_type_mix.png")

x=continent.sort_values("facilities")
plt.figure(figsize=(10,6)); plt.barh(x["continent"].fillna("Unknown"),x["facilities"])
plt.title("Mapped facilities by continent"); plt.xlabel("Facilities"); save("03_continent_facilities.png")

x=operators.head(15).sort_values("facilities")
plt.figure(figsize=(10,6)); plt.barh(x["operator"],x["facilities"])
plt.title("Top operators by mapped facilities"); plt.xlabel("Mapped facilities"); save("04_top_operators.png")

x=comparison.nlargest(15,"reported_minus_osm").sort_values("reported_minus_osm")
plt.figure(figsize=(10,6)); plt.barh(x["country"],x["reported_minus_osm"])
plt.title("Largest positive gap: reported minus mapped facilities"); plt.xlabel("Facility count gap"); save("05_reported_vs_mapped_gap.png")

fp=data_centers["footprint_area_m2"].dropna(); fp=fp[fp>0]
plt.figure(figsize=(10,6)); plt.hist(np.log10(fp),bins=35)
plt.title("Distribution of mapped facility footprints (log10 m²)")
plt.xlabel("log10(footprint area in m²)"); plt.ylabel("Facilities"); save("06_footprint_distribution_log.png")

x=country_summary.nlargest(15,"total_footprint_m2").sort_values("total_footprint_m2")
plt.figure(figsize=(10,6)); plt.barh(x["country"],x["total_footprint_m2"]/1e6)
plt.title("Top countries by mapped total footprint"); plt.xlabel("Total footprint (million m²)"); save("07_country_footprint.png")

x=operators.nlargest(15,"footprint_m2").sort_values("footprint_m2")
plt.figure(figsize=(10,6)); plt.barh(x["operator"],x["footprint_m2"]/1e6)
plt.title("Top operators by mapped footprint"); plt.xlabel("Footprint (million m²)"); save("08_operator_footprint.png")

print("Analysis complete. Outputs written to outputs/.")
