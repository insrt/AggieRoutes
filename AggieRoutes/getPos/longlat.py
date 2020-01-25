import requests
import json


class busStop:
    stopName = ''
    routeNum = -1
    latitude = -1
    longitude = -1

    def __init__(self, stop, num, lat, lon):
        self.stopName = stop
        self.routeNum = num
        self.latitude = lat
        self.longitude = lon

    def printAll(self):
        print(self.stopName)
        print(self.routeNum)
        print(self.latitude)
        print(self.longitude)


routeNumber = '01-04'

url = 'https://transport.tamu.edu/BusRoutesFeed/api/route/' + routeNumber + '/stops'

response = requests.get(url)

data = response.text
parsed = json.loads(data)

magicLat = 117029.1868  # Conversion number for latitude
magicLong = 111319.2856  # Conversion number for longitude
oldLat = 0
oldLong = 0

stopList = []

for stop in parsed:
    # print(stop['Name'])
    oldLat = stop['Latitude']  # Original pre converted latitude
    oldLong = stop['Longtitude']  # Original pre converted longitude
    # print('Lat/Long:')
    newLat = oldLat / magicLat
    newLong = oldLong / magicLong
    # print(newLat)
    # print(newLong)
    # print('\n')

    currStop = busStop(stop['Name'], routeNumber, newLat, newLong)
    stopList.append(currStop)

for stop in stopList:
    stop.printAll()
    print('\n')

# print(json.dumps(parsed, indent=4))
