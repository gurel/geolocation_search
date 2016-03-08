from functools import partial
from heapq import heapify, heappush, heappop
import json
import logging
import os
import sys
from math import cos, sin, atan2, sqrt, acos, asin, radians

__author__ = "gurelerceis"
__copyright__ = "Copyright 2016"
__credits__ = ["gurelerceis", ""]
__license__ = "Private"
__version__ = "1.0.0"
__maintainer__ = "gurelerceis"
__email__ = "gurel.erceis@gmail.com"

# Always switch to unicode just in case
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['TZ'] = 'UTC'

COSINES = 0
HAVERSINE = 1
VINCENTY = 2

def geo_distance(la1, lo1, la2, lo2, formula=2, radius=6371):
    """
    This function will calculate the distance between the two given points on a sphere.
    It supports 3 formulas to calculate the distance. (https://en.wikipedia.org/wiki/Great-circle_distance)

    :param la1: latitude of point 1 (in radians)
    :param lo1: longitude of point 1 (in radians)
    :param la2: latitude of point 2 (in radians)
    :param lo2: longitude of point 2 (in radians)
    :param formula: COSINES | HAVERSINE | VINCENTY
    :default formula: VINCENTY
    :return: distance in kilometers
    """

    delta_longitude = abs(lo1 - lo2)

    if formula == 0:
        # Spherical law of cosines
        cos_la1, cos_la2, sin_la1, sin_la2 = cos(la1), cos(la2), sin(la1), sin(la2)
        cos_dlo = cos(delta_longitude)

        center_angle = acos(
            sin_la1 * sin_la2 + cos_la1 * cos_la2 * cos_dlo
        )
    elif formula == 1:
        # Haversine formula
        delta_latitude = abs(la1 - la2)
        cos_la1, cos_la2 = cos(la1), cos(la2)

        center_angle = 2*asin(
            sqrt(pow(sin(delta_latitude/2), 2) + cos_la1 * cos_la1 * pow(sin(delta_longitude/2), 2))
        )
    else:
        # Vincenty Formula
        cos_la1, cos_la2, sin_la1, sin_la2 = cos(la1), cos(la2), sin(la1), sin(la2)
        sin_dlo, cos_dlo = sin(delta_longitude), cos(delta_longitude)

        center_angle = atan2(
            sqrt(pow(cos_la2 * sin_dlo, 2) + pow((cos_la1 * sin_la2) - (sin_la1 * cos_la2 * cos_dlo), 2)),
            (sin_la1 * sin_la2) + (cos_la1 * cos_la2 * cos_dlo)
        )

    distance = radius * center_angle

    return distance


def record_iterator(input_file):
    """
    This is an generator for the given file
    It will read a line format it from a JSON and convert geo position to radians for convenience

    :param input_file: Path of file to be read
    :return:
    """
    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            obj = json.loads(line)
            obj['latitude'] = radians(float(obj['latitude']))
            obj['longitude'] = radians(float(obj['longitude']))

            yield obj
            line = f.readline()

if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger("GeoSearch")
    logger.setLevel(logging.INFO)

    if len(sys.argv) < 5:
        logger.error("Usage:")
        logger.error("\tpython GeoSearch.py 53.3381985 -6.2592576 100 customers.json")
        logger.error("parameters in order are: latitude, longitude, distance, input_file")

    # Read parameters
    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])
    distance = float(sys.argv[3])
    input_file = sys.argv[4]

    logger.debug("Inputed File: {}".format(input_file))
    logger.debug("Inputed latitude: {}".format(latitude))
    logger.debug("Inputed longitude: {}".format(longitude))
    logger.debug("Inputed distance: {}".format(distance))

    # It is crutial to convert the given geo locations to radians
    # This wrapped function will help us to perform calls easier
    get_distance = partial(geo_distance, radians(latitude), radians(longitude), formula=VINCENTY)

    users_in_range = []

    for record in record_iterator(input_file):
        # Check if the distance between the two points are smaller or equal to the search distance
        if get_distance(record['latitude'], record['longitude']) <= distance:
            # Add the user to the heap, this will help us to keep a sorted user list
            heappush(users_in_range, (record['user_id'], record))

    while users_in_range:
        user_id, user = heappop(users_in_range)
        # Since this is a simple JSON output, we will go on with a string format
        print '{"user_id": %s, "name": "%s"}' % (user['user_id'], user['name'])



