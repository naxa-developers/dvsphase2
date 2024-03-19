
from rest_framework import status
import os, shutil

from .file_handlers import handleShapeFile, handleCSV, handleGeoJSON, handleKML

from core.models import (
    VectorLayer,
    Layer,
    FeatureCollection,

)
import zipfile
import glob


def update_layer_data(id, geometry_type, bound_dict):
    layer = VectorLayer.objects.get(pk=id)
    layer.geometry_type = geometry_type
    layer.bbox = bound_dict.get("total_bounds", [])
    file_extension = get_file_extension(str(layer.file_upload.path))
    layer.file_extension = file_extension
    type_of_layer = validate_file_type(file_extension)
    if not type_of_layer:
        return (
            id,
            "error",
            "File extension does not match the selected type_of_layer.",
            status.HTTP_400_BAD_REQUEST,
        )
    layer.type_of_layer = type_of_layer
    layer.save()
    return id, "success", "Layer added Sucessfully", status.HTTP_200_OK

def get_file_extension(file_upload):
    split_tup = os.path.splitext(file_upload)
    file_extension = split_tup[1]
    allowed_extensions = [".zip", ".csv", ".geojson", ".kml"]
    if file_extension in allowed_extensions:
        return file_extension
    else:
        return (
            None,
            "error",
            "Invalid file extension. Supported extensions are: '.zip', '.csv', '.geojson', '.kml'",
            status.HTTP_400_BAD_REQUEST,
        )

def validate_file_type(file_extension):
    dict = {".zip": "Shapefile", ".csv": "CSV", ".geojson": "Geojson", ".kml": "KML"}
    try:
        return dict[file_extension]
    except Exception as e:
        return None


def upload_vector_layer(file_id):
    instance = VectorLayer.objects.get(id=file_id)
    file_extension = get_file_extension(str(instance.file_upload.path))
    if file_extension == ".zip":
        shapefile_extensions = [".shp", ".dbf", ".shx", ".prj"]
        shapefile = VectorLayer.objects.get(id=file_id)
        with zipfile.ZipFile(shapefile.file_upload, "r") as zip_ref:
            zip_ref.extractall(str(shapefile.file_upload))
        matching_files = []
        for extension in shapefile_extensions:
            matching_files.extend(
                glob.glob(
                    r"{}/**/*{}".format(str(shapefile.file_upload), extension),
                    recursive=True,
                )
            )
        if matching_files:
            shape = matching_files[0]
            try:
                geometry_type, bound_dict = handleShapeFile(
                    shape, file_id, FeatureCollection
                )
                # Remove the uploaded files
                shutil.rmtree(os.path.dirname(str(shapefile.file_upload)))
                return update_layer_data(file_id, geometry_type, bound_dict)
            except Exception as e:
                return file_id, "error", str(e), status.HTTP_400_BAD_REQUEST
        else:
            return (
                file_id,
                "error",
                "No valid files found in the zip archive.",
                status.HTTP_400_BAD_REQUEST,
            )

    elif file_extension == ".csv":
        csv = VectorLayer.objects.get(id=file_id)
        latitude = csv.lat_field
        longitude = csv.long_field
        try:
            geometry_type, total_bounds, bound_dict = handleCSV(
                VectorLayer, file_id, FeatureCollection, latitude, longitude
            )
            return update_layer_data(file_id, geometry_type, bound_dict)
        except Exception as e:
            return file_id, "error", str(e), status.HTTP_400_BAD_REQUEST

    elif file_extension == ".geojson":
        try:
            geometry_type, bound_dict = handleGeoJSON(
                VectorLayer, file_id, FeatureCollection
            )
            return update_layer_data(file_id, geometry_type, bound_dict)
        except Exception as e:
            return file_id, "error", str(e), status.HTTP_400_BAD_REQUEST

    elif file_extension == ".kml":
        geometry_type, total_bounds, bound_dict = handleKML(
            VectorLayer, file_id, FeatureCollection
        )
        return update_layer_data(file_id, geometry_type, bound_dict)

    else:
        return (
            file_id,
            "error",
            "Invalid file extension. Supported extensions are: '.zip', '.csv', '.geojson', '.kml'",
            status.HTTP_400_BAD_REQUEST,
        )

