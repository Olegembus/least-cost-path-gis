# 🥾 Least Cost Path Analysis (Automated GIS Workflow)

A project for automated analysis of the optimal path using ArcGIS 10.8, ArcPy, and Spatial Analyst extension.

## 📌 Overview

This script performs a complete **Least Cost Path analysis** based on a digital elevation model (DEM) and land cover data. It calculates the optimal route between two points by taking into account terrain slope and land cover types (e.g. forests, water bodies, urban areas).

---

## 📁 Project Structure

E:\least_cost_path_project
│
├── 📂 data/                      # Input data
│   ├── 📄 dem.tif               # Digital Elevation Model 
│   ├── 📄 landcover.tif         # Land cover classification (ESA WorldCover)
│   ├── 📄 source.shp            # Starting point (shapefile)
│   └── 📄 destination.shp       # Destination point (shapefile)
│
├── 📂 results/                  # Output directory (auto-generated)
│
├── 📂 scripts/                  # Python scripts
│   └── 📄 least_cost_path_automatization.py  # Main analysis script
│
└── 📄 README.md                 # Project documentation


---

## ✅ Requirements

- ArcGIS Desktop 10.8
- **Spatial Analyst** license
- Python 2.7 (built into ArcMap)
- All input data must use the same projection (preferably UTM, in meters)

---

## 🔍 Input Data

1. `dem.tif` — Digital Elevation Model (GeoTIFF)
2. `landcover.tif` — ESA WorldCover raster (10 m resolution)
3. `source.shp` — Starting point (shapefile)
4. `destination.shp` — Destination point (shapefile)

### Land Cover Reclassification (ESA WorldCover)

| Code | Class Name           | Cost |
|------|----------------------|------|
| 10   | Tree cover           | 4    |
| 20   | Shrubland            | 3    |
| 30   | Grassland            | 2    |
| 40   | Cropland             | 1    |
| 50   | Built-up             | 5    |
| 60   | Bare/sparse vegetation | 2  |
| 70   | Snow and ice         | 9999 |
| 80   | Permanent water      | 9999 |
| 90   | Wetlands             | 7    |
| 95   | Mangroves            | 9999 |
| 100  | Moss and lichen      | 5    |

### Slope Reclassification

| Slope (degrees) | Cost |
|-----------------|------|
| 0–5°            | 1    |
| 5–10°           | 2    |
| 10–20°          | 3    |
| 20–30°          | 4    |
| >30°            | 5    |

---

## 📤 Output Files (results/)

1. `cost_surface.tif` — Combined cost raster (slope + landcover)
2. `cost_distance.tif` — Accumulated cost distance from source point
3. `backlink.tif` — Backlink raster for path reconstruction
4. `least_cost_path.tif` — Least cost path (raster)
5. `least_cost_path.shp` — Least cost path (vector line)

---

## 🚀 How to Run

1. Place all required input data in the `data/` folder
2. Open Python 2.7 terminal (ArcGIS environment)
3. Run the script:

```bash
python E:\least_cost_path_project\scripts\least_cost_path_automatization.py
