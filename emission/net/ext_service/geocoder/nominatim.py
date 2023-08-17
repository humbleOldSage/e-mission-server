from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import logging
import json
import os

from emission.core.wrapper.trip_old import Coordinate
try:
    NOMINATIM_QUERY_URL_env = os.environ.get("NOMINATIM_QUERY_URL", "")
    NOMINATIM_QUERY_URL = NOMINATIM_QUERY_URL_env if NOMINATIM_QUERY_URL_env != "" else "http://nominatim.openstreetmap.org"

except:
    print("nominatim not configured either, place decoding must happen on the client")

class Geocoder(object):

    def __init__(self):
        pass
        
    @classmethod
    def make_url_geo(cls, address):
        params = {
            "q" : address,
            "format" : "json"
        }

        query_url = NOMINATIM_QUERY_URL + "/search?"
        encoded_params = urllib.parse.urlencode(params)
        url = query_url + encoded_params
        logging.debug("For geocoding, using URL %s" % url)
        return url

    @classmethod
    def get_json_geo(cls, address):
        request = urllib.request.Request(cls.make_url_geo(address))
        print("request", request)
        response = urllib.request.urlopen(request)
        print("response", response)
        jsn = json.loads(response.read())
        print("jsn", jsn)
        return jsn

    @classmethod
    def geocode(cls, address):
        jsn = cls.get_json_geo(address)
        lat = float(jsn[0]["lat"])
        lon = float(jsn[0]["lon"])
        return Coordinate(lat, lon)

    @classmethod
    def make_url_reverse(cls, lat, lon):
        params = {
            "lat" : lat, 
            "lon" : lon,
            "format" : "json"
        }

        query_url = NOMINATIM_QUERY_URL + "/reverse?"
        encoded_params = urllib.parse.urlencode(params)
        url = query_url + encoded_params
        logging.debug("For reverse geocoding, using URL %s" % url)
        return url

    @classmethod
    def get_json_reverse(cls, lat, lng):
        request = urllib.request.Request(cls.make_url_reverse(lat, lng))
        response = urllib.request.urlopen(request)
        parsed_response = json.loads(response.read())
        logging.debug("parsed_response = %s" % parsed_response)
        print("parsed res", parsed_response)
        print("restype", type(parsed_response))
        return parsed_response

    @classmethod
    def reverse_geocode(cls, lat, lng):
        jsn = cls.get_json_reverse(lat, lng)
        address = jsn["display_name"]
        return address