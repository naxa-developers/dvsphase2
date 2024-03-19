import fiona
import pandas as pd
import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.prototypes.io import wkt_w


def handleShapeFile(shape, file_id, feature_collection_model):
    gdf = gpd.read_file(shape)
    geometry_type = gdf["geometry"].iloc[0].geom_type
    total_bounds = gdf.total_bounds
    bound_dict = {"total_bounds": total_bounds.tolist()}
    for index, row in gdf.iterrows():
        dropped_geometry = row.drop(["geometry"])
        dropped_geometry_dict = dropped_geometry.to_dict()
        geom = GEOSGeometry(str(row["geometry"]))
        wkt = wkt_w(dim=2).write(geom).decode()
        geom = GEOSGeometry(wkt)
        feature_collection_model.objects.create(
            feature_id=file_id, attr_data=dropped_geometry_dict, geom=geom
        )
    return geometry_type, bound_dict


def handleCSV(file_model, file_id, feature_collection_model, latitude, longitude):
    shapefile = file_model.objects.get(id=file_id)
    shape = shapefile.file_upload
    df = pd.read_csv(
        shape, keep_default_na=False, encoding="utf-8"
    )  # Specify the encoding as 'utf-8'
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[longitude], df[latitude]))
    crs = {"init": "epsg:4326"}
    gdf = gpd.GeoDataFrame(df, crs=crs)
    gdf.fillna("")
    geometry_type = gdf["geometry"].iloc[0].geom_type
    total_bounds = gdf.total_bounds
    bound_dict = {"total_bounds": total_bounds.tolist()}

    for index, row in gdf.iterrows():
        dropped_geometry = row.drop(["geometry"])
        dropped_geometry_dict = dropped_geometry.to_dict()
        geom = GEOSGeometry(str(row["geometry"]))
        wkt = wkt_w(dim=2).write(geom).decode()
        geom = GEOSGeometry(wkt)
        feature_collection_model.objects.create(
            feature_id=file_id, attr_data=dropped_geometry_dict, geom=geom
        )
    return geometry_type, bound_dict


def handleGeoJSON(file_model, file_id, feature_collection_model):
    shapefile = file_model.objects.get(id=file_id)
    shape = shapefile.file_upload
    gdf = gpd.read_file(shape)
    crs_name = str(gdf.crs.srs)
    total_bounds = gdf.total_bounds
    bound_dict = {"total_bounds": total_bounds.tolist()}
    geometry_type = gdf["geometry"].iloc[0].geom_type
    epsg = int(crs_name.replace("epsg:", ""))
    if epsg is None:
        epsg = 4326
    for index, row in gdf.iterrows():
        dropped_geometry = row.drop(["geometry"])
        dropped_geometry_dict = dropped_geometry.to_dict()
        geom = GEOSGeometry(str(row["geometry"]))
        wkt = wkt_w(dim=2).write(geom).decode()
        geom = GEOSGeometry(wkt)
        feature_collection_model.objects.create(
            feature_id=file_id, attr_data=dropped_geometry_dict, geom=geom
        )
    return geometry_type, bound_dict


def handleKML(file_model, file_id, feature_collection_model):
    shapefile = file_model.objects.get(id=file_id)
    shape = shapefile.file_upload
    fiona.drvsupport.supported_drivers["KML"] = "rw"
    gdf = gpd.read_file(shape, driver="KML")
    crs_name = str(gdf.crs.srs)
    geometry_type = gdf["geometry"].iloc[0].geom_type
    total_bounds = gdf.total_bounds
    bound_dict = {"total_bounds": total_bounds.tolist()}
    epsg = int(crs_name.replace("epsg:", ""))
    if epsg is None:
        epsg = 4326
    for index, row in gdf.iterrows():
        dropped_geometry = row.drop(["geometry"])
        dropped_geometry_dict = dropped_geometry.to_dict()
        geom = GEOSGeometry(str(row["geometry"]))
        wkt = wkt_w(dim=2).write(geom).decode()
        geom = GEOSGeometry(wkt)
        feature_collection_model.objects.create(
            file_id_id=file_id, attr_data=dropped_geometry_dict, geom=geom
        )
    return geometry_type, bound_dict
