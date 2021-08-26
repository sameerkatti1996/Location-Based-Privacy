#!c:/Python34/python.exe
import sys
import math
import random
from retrying import retry
import cgi


def hilbert(x0, y0, xi, xj, yi, yj, n):
    global x,y
    global count
    global val
    if n <= 0:
        X = x0 + (xi + yi) / 2
        Y = y0 + (xj + yj) / 2
        count = count + 1
        x.append(X)
        y.append(Y)
        val.append(count)
        # Output the coordinates of the cv
        #print('%s %s %s' % (X, Y, count))
    else:
        hilbert(x0, y0, yi / 2, yj / 2, xi / 2, xj / 2, n - 1)
        hilbert(x0 + xi / 2, y0 + xj / 2, xi / 2, xj / 2, yi / 2, yj / 2, n - 1)
        hilbert(x0 + xi / 2 + yi / 2, y0 + xj / 2 + yj / 2, xi / 2, xj / 2, yi / 2, yj / 2, n - 1)
        hilbert(x0 + xi / 2 + yi, y0 + xj / 2 + yj, -yi / 2, -yj / 2, -xi / 2, -xj / 2, n - 1)


def map_range(a, b, s, square):
    (a1, a2), (b1, b2) = a, b
    return math.floor( (random.randint(999,9999) + b1 + ((s - a1) * (b2 - b1) / (a2 - a1))) % math.pow(4, square))

def create_dummy_loc_block(k):
    global x
    global y
    global val
    square = 4
    hilbert(0.0, 0.0, 1.0, 0.0, 0.0, 1.0, square)
    mini_x = min(x)
    mini_y = min(y)
    """for i in range(0, len(x)):
        print("%s %s %s" % ((x[i] - mini_x) / (mini_x * 2), (y[i] - mini_y) / (mini_y * 2), val[i]))"""
    key1 = 1345267
    key2 = random.randint(999999, 9999999)
    key_final = (key1 * key2) % random.randint(999, 9999)
    #print(key_final)
    # for i in range(0,len(key)):
    mapped_val = []
    for s in range(1, k + 1):
        # print("%2g maps to %g" % (s, map_range((1, k+1), (0,math.pow(4,square)), s, square)))
        val = map_range((1, k + 1), (0, math.pow(4, square)), s, square)
        #print(val)
        if val not in mapped_val:
            mapped_val.append(val)
        else:
            while val not in mapped_val:
                val = (val + 1) % math.pow(4, square)
            mapped_val.append(val)
    mapped_val.sort()
    #print(mapped_val)
    return mapped_val, mini_x, mini_y

def create_dummy_loc(latitude, longitude, km, k):
    mapped_val, min_x, mini_y = create_dummy_loc_block(k)
    user_index = random.randint(0,len(mapped_val))
    user_block = mapped_val[user_index]
    user_x = x[user_index]
    user_y = x[user_index]
    #print(user_block)
    lat_lng = [[latitude, longitude]]
    lat = [latitude]
    lng = [longitude]
    for a in mapped_val:
        if a != user_block:
            dummy_x = x[a]
            dummy_y = y[a]
            dist_x = (dummy_x - user_x) * 0.01 * km
            dist_y = (dummy_y - user_y) * 0.01 * km
            lat_lng.append([latitude + dist_y, longitude + dist_x])
            lat.append(latitude + dist_y)
            lng.append(longitude + dist_x)
            #print(str(dist_x)+"   "+str(dist_y))
    #print(lat_lng)
    random.shuffle(lat_lng)
    #print(lat_lng)
    response = get_correct_response(lat_lng, [latitude, longitude])
    #print(json.loads(response)["results"][0]["formatted_address"])

def get_correct_response(lat_lng,user_lat_lng):
    for latlng in lat_lng:
        #print(latlng)
        latitude = latlng[0]
        longitude = latlng[1]
        response = get_address(latitude, longitude)
        if [latitude, longitude] == user_lat_lng:
            response = response.text
            import json
            #print(json.loads(response)["results"][0]["formatted_address"]+"<br/>\r\n")
    return response

@retry(stop_max_attempt_number=3)
def get_address(latitude, longitude):
    import requests, json
    request_string = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" \
                     + str(latitude) + "," + str(longitude) + "&sensor=true"
    response = requests.get(request_string)
    locat = response.text
    locat = json.loads(locat)
    location_info = locat["results"][0]["formatted_address"]
    print(location_info+"<br/>\r\n")
    return response



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
print("  <br><br>\r\n");
print("  K Value:<br>\r\n");
print("  <input type='text' name='k' value=''>\r\n");
print("  <br><br>\r\n");
print("  Distance:<br>\r\n");
print("  <input type='text' name='dist' value=''>\r\n");
print("  <br><br>\r\n");

print(" <br><br> <input type='submit' value='Submit'>\r\n");
print("</form>\r\n");
print("</body>\r\n")
form = cgi.FieldStorage()
lat = form["lat"].value
long = form["long"].value
k = form["k"].value
dist = form["dist"].value

print("\r\n<br>The latitude given is : "+str(lat))
print("\r\n<br>The longitude given is : "+str(long)+"\r\n")
print("<br/>")
x = []
y = []
val = []
count = 0
print("The given address: ")
get_address(lat, long)
print("<br/>\r\n")
create_dummy_loc(float(lat), float(long), float(dist), int(k))

