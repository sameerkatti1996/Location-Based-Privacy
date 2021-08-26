#!c:/Python34/python.exe
import requests
import geocoder
import json
from retrying import retry
import cgi


class location_obfuscation:
    """This module helps in generalizing the location based on
    the given location"""

    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.long = longitude

    @retry(stop_max_attempt_number=3)
    def get_location(self):
        """
        Overview:
        Given the location in the form of latitude and longitude, the
        function makes an API call using Google API, gets the response
        and returns the same.

        Arguments Required: None to be passed.

        Returns: Response containing the Location Details"""

        request_string = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" \
                         + str(self.lat) + "," + str(self.long) + "&sensor=true"
        response = requests.get(request_string)
        return response

    @retry(stop_max_attempt_number=3)
    def location_generalization(self):
        """
        Overview:
        The method gets the location details, converts it to JSON format.
        The sublocalities present in the response are fetched. If sublocality is not present,
        then locality is taken.

        Arguments: None to be passed.

        Returns: The area_list consisting of the sublocalities/locality and location response.

        """
        response = self.get_location()
        locat = response.text
        locat = json.loads(locat)
        location_info = locat["results"][0]["address_components"]
        area_list = []
        subarea_area = {}
        for entity in location_info:
            if "sublocality_level_1" in entity["types"] or "sublocality_level_2" in entity["types"] or "sublocality_level_3" in entity["types"]:
                area_list.append(entity['long_name'])
        city = ""
        for entity in location_info:
            if "locality" in entity["types"]:
                city += entity['long_name']

        if len(area_list) == 0:
            area_list.append(city)

        return area_list, city, locat

    @property
    def select_location(self):
        """
        Overview:
        This method creates the four corners of imaginary box where the actual
        location lies and selects, processes all the four corners as individual points.

        Returns:
        """
        area_list, city, location = self.location_generalization()
        ne = location["results"][0]["geometry"]["viewport"]["northeast"]
        ne_lat = ne['lat']
        ne_long = ne['lng']
        sw = location["results"][0]["geometry"]["viewport"]["southwest"]
        sw_lat = sw['lat']
        sw_long = sw['lng']

        subarea_area = {}

        lat = [ne_lat, sw_lat]
        long = [ne_long, sw_long]

        min_lat, min_lng = self.get_minimized_square(lat, long)

        small_lat, small_long = self.get_minimized_square(min_lat, min_lng)

        obfus_area = []

        for i in range(0, 2):
            for j in range(0, 2):
                area, city, loc = location_obfuscation(lat[i], long[j]).location_generalization()
                m = 0
                for m in range(0, len(area) - 1):
                    if area[m] not in subarea_area.keys():
                        subarea_area.update({area[m]: area[m + 1]})
                if area[m] not in subarea_area.keys():
                    subarea_area.update({area[m]: city})
                obfus_area.append(area)

        for i in range(0, 2):
            for j in range(0, 2):
                area, city, loc = location_obfuscation(min_lat[i], min_lng[j]).location_generalization()
                m = 0
                for m in range(0, len(area) - 1):
                    if area[m] not in subarea_area.keys():
                        subarea_area.update({area[m]: area[m + 1]})
                if area[m] not in subarea_area.keys():
                    subarea_area.update({area[m], city})
                obfus_area.append(area)

        for i in range(0, 2):
            for j in range(0, 2):
                area, city, loc = location_obfuscation(small_lat[i], small_long[j]).location_generalization()
                m = 0
                for m in range(0, len(area) - 1):
                    if area[m] not in subarea_area.keys():
                        subarea_area.update({area[m]: area[m + 1]})
                if area[m] not in subarea_area.keys():
                    subarea_area.update({area[m], city})
                obfus_area.append(area)

        return obfus_area, subarea_area, city

    def get_minimized_square(self, lat, lng):
        lat.sort()
        lng.sort()
        diff = lat[1] - lat[0]
        diff = diff / 4
        lat[0] = lat[0] + diff
        lat[1] = lat[1] - diff

        diff = lng[1] - lng[0]
        diff = diff / 4
        lng[0] = lng[0] + diff
        lng[1] = lng[1] - diff

        return lat, lng

    @retry(stop_max_attempt_number=3)
    def find_obfuscated_area(self):
        obfus_area, subarea_area, city = self.select_location
        dict = {}
        for area in obfus_area:
            for loc in area:
                if loc in dict.keys():
                    value = int(dict[loc])
                    value += 1
                    dict[loc] = value
                else:
                    dict.update({loc: 1})

        area = list(dict.keys())

        max = 0

        key = area[0]

        for val in area:
            if int(dict[val]) > max:
                max = int(dict[val])
                key = []
                key.append(val)
            elif int(dict[val]) == max:
                key.append(val)
        if len(key) == 1:
            if key[0] in subarea_area.keys():
                print(key[0] + ", " + subarea_area[key[0]])
            else:
                print(key[0] + ", " + city)
        else:
            import sys
            min = sys.maxsize
            val = ""
            for k in key:
                if k in subarea_area.keys():
                    lat, lng = self.find_coord(k, subarea_area[k])
                    if (self.calculate_dist(self.lat, self.long, lat, lng) < min):
                        min = self.calculate_dist(self.lat, self.long, lat, lng)
                        val = k + ", " + subarea_area[k]
            print(val)

    @retry(stop_max_attempt_number=3)
    def find_coord(self, subloc, loc):
        request_string = "https://maps.googleapis.com/maps/api/geocode/json?address=" + subloc + ",+" + loc
        response = requests.get(request_string)
        response = json.loads(response.text)
        lat = response["results"][0]["geometry"]['location']['lat']
        lng = response["results"][0]["geometry"]['location']['lng']
        return lat, lng

    def calculate_dist(self, lat1, lng1, lat2, lng2):
        from math import sin, cos, sqrt, atan2, radians

        R = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lng1)
        lat2 = radians(lat2)
        lon2 = radians(lng2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance






print("Content-type: text/html\r\n")
print("<head>\r\n")
print("<title>Location Based Privacy</title>\r\n")
print("</head>\r\n")
print("<body>\r\n")
print("<h1>LOCATION BASED PRIVACY</h1>\r\n")
print("<h2>Enter Lat Long</h2>\r\n")
print("<form  >\r\n");
print("  Latitude:<br>\r\n");
print("  <input type='text' name='lat' value=''>\r\n");
print("  <br>\r\n");
print("  Longitude:<br>\r\n");
print("  <input type='text' name='long' value=''>\r\n");
print(" <br><br> <input type='submit' value='Submit'>\r\n");
print("</form>\r\n");
print("</body>\r\n")
form = cgi.FieldStorage()
lat = form["lat"].value
long = form["long"].value
print("\r\n<br>The latitude given is : "+str(lat))
print("\r\n<br>The longitude given is : "+str(long)+"\r\n")
g = geocoder.ip('me')
ob = location_obfuscation(float(lat), float(long))
resp = ob.get_location()
resp = json.loads(resp.text)
exact_loc = resp["results"][0]["formatted_address"]
print("Lat, Long :\r\n")
print(str(ob.lat) + ", " + str(ob.long))
print("<br/>Address :\r\n")
print(exact_loc)
print("<br/>Obfuscated Location : \r\n")
ob.find_obfuscated_area()


