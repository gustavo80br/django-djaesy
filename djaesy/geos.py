from django.contrib.gis import geos


def circle_maker(center, radius):

    center = geos.Point(center[0], center[1], srid=4326)
    # center.srid = 900913
    center.transform(4326)

    radius = radius # * 1.852
    buffer_width = radius / 40000000.0 * 360.0
    polygon = center.buffer(buffer_width)
    return polygon
