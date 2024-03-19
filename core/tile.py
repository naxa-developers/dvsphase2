from django.core.exceptions import FieldError
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from rest_framework.serializers import ValidationError
from rest_framework.renderers import BaseRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from math import atan, degrees, pi
from math import pow as math_pow
from math import sinh


def split_on_last_occurrence(sentence, word):
    words = sentence.rsplit(word, 1)
    if len(words) > 1:
        return [words[0].strip(), words[1].strip()]
    else:
        return [sentence]


# ------------
# Manager
# ------------
class MVTManager(models.Manager):
    """
    Args:
        geom_col (str): Column name with the geometry. The default is "geom".
        source_name (str): Connection source to use.  If not provided the app's default
                           connection is used.
    """

    def __init__(self, *args, geom_col="geom", source_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.geom_col = geom_col
        self.source_name = source_name

    def intersect(self, bbox="", limit=-1, offset=0, filters={}, queryset=None):
        """
        Args:
            bbox (str): A string representing a bounding box, e.g., '-90,29,-89,35'.
            limit (int): Number of entries to include in the result.  The default
                         is -1 (includes all results).
            offset (int): Index to start collecting entries from.  Index size is the limit
                          size.  The default is 0.
            filters (dict): The keys represent column names and the values represent column
                            values to filter on.
        Returns:
            bytes:
            Bytes representing a Google Protobuf encoded Mapbox Vector Tile.  The
            vector tile will store each applicable row from the database as a
            feature.  Applicable rows fall within the passed in bbox.

        Raises:
            ValidationError: If filters include keys or values not accepted by
                             the manager's model.

        Note:
            The sql execution follows the guidelines from Django below.  As suggested, the executed
            query string does NOT contain quoted parameters.

            https://docs.djangoproject.com/en/2.2/topics/db/sql/#performing-raw-queries
        """
        limit = "ALL" if limit == -1 else limit
        query, parameters = self._build_query(filters=filters, queryset=queryset)
        with self._get_connection().cursor() as cursor:
            cursor.execute(query, [str(bbox), str(bbox)] + parameters + [limit, offset])
            mvt = cursor.fetchall()[-1][-1]  # should always return one tile on success
        return mvt

    def _get_non_geom_columns(self):
        """
        Retrieves all table columns that are NOT the defined geometry column
        """
        columns = []
        for field in self.model._meta.get_fields():
            if hasattr(field, "get_attname_column"):
                column_name = field.get_attname_column()[1]
                if column_name and column_name != self.geom_col:
                    columns.append(column_name)
        return columns

    def _build_query(self, filters={}, queryset=None):
        """
        Args:
            filters (dict): keys represent column names and values represent column
                            values to filter on.
        Returns:
            tuple:
            A tuple of length two.  The first element is a string representing a
            parameterized SQL query.  The second element is a list of parameters
            used as inputs to the query's WHERE clause.
        """
        # sql, params = queryset.sql_with_params()
        table = self.model._meta.db_table.replace('"', "")
        if queryset is not None:
            select_statement = queryset["select_statement"]
            from_statement = queryset["from_statement"]
            where_clause = (
                queryset["where_statement"] if queryset["where_statement"] else ""
            )
            parameterized_where_clause = self._create_where_clause(table, where_clause)
            where_clause_parameters = (
                queryset["where_params"] if queryset["where_params"] else []
            )

        if queryset is None:
            from_statement = table
            select_statement = self._create_select_statement()

            (
                parameterized_where_clause,
                where_clause_parameters,
            ) = self._create_where_clause_with_params(table, filters)
        query = f"""
        SELECT NULL AS id, ST_AsMVT(q, 'default', 4096, 'mvt_geom')
            FROM ({select_statement} ,
                ST_AsMVTGeom(ST_Transform({table}.{self.geom_col}, 3857),
                ST_Transform(ST_SetSRID(ST_GeomFromText(%s), 4326), 3857), 4096, 0, false) AS mvt_geom
            FROM {from_statement}
            WHERE {parameterized_where_clause}
            LIMIT %s
            OFFSET %s) AS q;
        """
        return (query.strip(), where_clause_parameters)

    def _create_where_clause(self, table, where_clause):
        extra_wheres = " AND " + where_clause if where_clause is not None else ""
        where_clause = (
            f"ST_Intersects(ST_Transform({table}.{self.geom_col}, 4326), "
            f"ST_SetSRID(ST_GeomFromText(%s), 4326)){extra_wheres}"
        )
        return where_clause

    def _create_where_clause_with_params(self, table, filters):
        """
        Args:
            table (str): A string representing the name of the table to query on.
            filters (dict): keys represent column names and values represent column
                            values to filter on.
        Returns:
            tuple:
            A tuple of length two.  The first element is a string representing a
            parameterized SQL query WHERE clause.  The second element is a list
            of parameters used as inputs to the WHERE clause.
        """
        filter_dict = {}
        for key, value in filters.items():
            if "," in value:
                filter_dict[key + "__in"] = value.split(",")
            else:
                filter_dict[key] = value
        try:
            sql, params = self.filter(**filter_dict).query.sql_with_params()
        except FieldError as error:
            raise ValidationError(str(error)) from error
        extra_wheres = " AND " + sql.split("WHERE")[1].strip() if params else ""
        where_clause = (
            f"ST_Intersects(ST_Transform({table}.{self.geom_col}, 4326), "
            f"ST_SetSRID(ST_GeomFromText(%s), 4326)){extra_wheres}"
        )
        return where_clause, list(params)

    def _create_select_statement(self):
        """
        Create a SELECT statement that only includes columns defined on the
        model.  Each column must be named in the SELECT statement to specify
        only the required columns.  Including the geom column raises an error
        in the PostGIS ST_AsMVT function.

        Returns:
            str:
            A string representing a parameterized SQL query SELECT statement.
        """
        columns = self._get_non_geom_columns()
        sql, _ = self.only(*columns).query.sql_with_params()
        select_sql = sql.split("FROM")[0].lstrip("SELECT ").strip()
        return "SELECT " + select_sql

    def _get_connection(self):
        """

        Returns:
            (django.db.connection):
            The 'default' Django database connection if source_name is not defined on the instance.
        """
        # pylint: disable=import-outside-toplevel
        from django.db import connection, connections

        return connection if self.source_name is None else connections[self.source_name]


# ------------
# Renderer
# ------------
class BinaryRenderer(BaseRenderer):
    media_type = "application/*"
    format = "binary"
    charset = None
    render_style = "binary"

    # pylint: disable=no-self-use,unused-argument
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


# ------------
# Views
# ------------
def num_tiles(z):
    return math_pow(2, z)


def lat_edges(y, z):
    n = num_tiles(z)
    unit = 1 / n
    relY1 = y * unit
    relY2 = relY1 + unit
    lat1 = mercator_to_lat(pi * (1 - 2 * relY1))
    lat2 = mercator_to_lat(pi * (1 - 2 * relY2))
    return (lat1, lat2)


def lon_edges(x, z):
    n = num_tiles(z)
    unit = 360 / n
    lon1 = -180 + x * unit
    lon2 = lon1 + unit
    return (lon1, lon2)


def tile_edges(x, y, z):
    lat1, lat2 = lat_edges(y, z)
    lon1, lon2 = lon_edges(x, z)
    return (lon1, lat2, lon2, lat1)  # w, s, e, n


def mercator_to_lat(mercatorY):
    return degrees(atan(sinh(mercatorY)))


class BaseMVTView(APIView):
    """
    Base view for serving a model as a Mapbox Vector Tile given X/Y/Z tile constraints.
    """

    # pylint: disable=unused-argument
    def get(self, request, z, x, y, model, queryset=None):
        """
        Args:
            request (:py:class:`rest_framework.request.Request`): Standard DRF request object
        Returns:
            :py:class:`rest_framework.response.Response`:  Standard DRF response object
        """
        params = request.GET.dict()
        limit = params.pop("limit", None)
        offset = params.pop("offset", None)
        try:
            if limit is not None and offset is not None:
                try:
                    limit, offset = int(limit), int(offset)
                except ValueError as value_error:
                    raise ValidationError(
                        "Query param validation error: " + str(value_error)
                    ) from value_error
        except ValidationError:
            limit, offset = None, None

        bbox = Polygon.from_bbox(tile_edges(x=x, y=y, z=z))
        try:
            mvt = model.vector_tiles.intersect(
                bbox=bbox, limit=limit, offset=offset, filters=params, queryset=queryset
            )
            status = 200 if mvt else 204
        except ValidationError:
            mvt = b""
            status = 400
        return Response(
            bytes(mvt),
            content_type="application/vnd.mapbox-vector-tile",
            status=status,
            headers={"tile-cache": "false"},
        )
