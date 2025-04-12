# -*- coding: utf-8 -*-

import os
import arcpy
from arcpy.sa import *

def check_input_files(input_files):
    """Check if input files exist"""
    missing_files = []
    for file_path in input_files:
        if not arcpy.Exists(file_path):
            missing_files.append(file_path)
    return missing_files

def create_directory(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    # Set workspace
    workspace = r"E:\least_cost_path_project"
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    # Check Spatial Analyst license
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
    else:
        arcpy.AddError("Spatial Analyst license is not available.")
        return

    # Define input data
    input_dem = os.path.join(workspace, "data", "dem.tif")
    input_landcover = os.path.join(workspace, "data", "landcover.tif")
    input_source = os.path.join(workspace, "data", "source.shp")
    input_destination = os.path.join(workspace, "data", "destination.shp")

    # Verify that all input files exist
    input_files = [input_dem, input_landcover, input_source, input_destination]
    missing_files = check_input_files(input_files)
    if missing_files:
        arcpy.AddError(f"Missing input files: {', '.join(missing_files)}")
        return

    # Create output directory
    results_dir = os.path.join(workspace, "results")
    create_directory(results_dir)

    try:
        # 1. Generate slope raster
        arcpy.AddMessage("Generating slope raster...")
        slope_raster = Slope(input_dem, "DEGREE")

        # 2. Reclassify slope to cost values
        arcpy.AddMessage("Reclassifying slope...")
        remap_slope = RemapRange([[0, 5, 1], [5, 10, 2], [10, 20, 3], 
                                  [20, 30, 4], [30, 90, 5]])
        slope_reclass = Reclassify(slope_raster, "Value", remap_slope)

        # 3. Reclassify landcover (ESA WorldCover)
        arcpy.AddMessage("Reclassifying landcover...")
        remap_landcover = RemapValue([[10, 4], [20, 3], [30, 2], [40, 1],
                                      [50, 5], [60, 2], [70, 9999], [80, 9999],
                                      [90, 7], [95, 9999], [100, 5]])
        landcover_reclass = Reclassify(input_landcover, "Value", remap_landcover)

        # 4. Combine slope and landcover into cost surface
        arcpy.AddMessage("Creating cost surface...")
        cost_surface = (slope_reclass * 0.5) + (landcover_reclass * 0.5)
        cost_surface.save(os.path.join(results_dir, "cost_surface.tif"))

        # 5. Calculate cost distance and backlink rasters
        arcpy.AddMessage("Calculating cost distance and backlink...")
        cost_distance, backlink = CostDistance(input_source, cost_surface,
                                               output_backlink_raster=os.path.join(results_dir, "backlink.tif"))
        cost_distance.save(os.path.join(results_dir, "cost_distance.tif"))

        # 6. Generate least cost path raster
        arcpy.AddMessage("Generating least cost path...")
        least_cost_path = CostPath(input_destination, cost_distance, backlink,
                                   path_type="EACH_CELL")
        least_cost_path.save(os.path.join(results_dir, "least_cost_path.tif"))

        # 7. Convert raster path to polyline
        arcpy.AddMessage("Converting raster path to vector polyline...")
        arcpy.RasterToPolyline_conversion(
            os.path.join(results_dir, "least_cost_path.tif"),
            os.path.join(results_dir, "least_cost_path.shp"),
            "ZERO", "0", "NO_SIMPLIFY", "Value"
        )

        arcpy.AddMessage("✅ Least Cost Path analysis completed successfully!")

    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages(2))
    except Exception as e:
        arcpy.AddError(f"An error occurred: {str(e)}")
    finally:
        # Release Spatial Analyst license
        arcpy.CheckInExtension("Spatial")

if __name__ == '__main__':
    main()
