from django.db import models
import requests
import json

routeNumber = [
        '01',
        '02',
        '03',
        '01-04',
        '03-05',
        '04',
        '05',
        '06',
        '07',
        '08',
        '12',
        '12-25',
        '15',
        '22',
        '25',
        '26',
        '27',
        '31',
        '34',
        '35',
        '36',
        '40',
        '47',
        'N15',
    ]

class RouteInfo(models.Model):
    buses = {}
    stops = {}
    for i, route in enumerate(routeNumber):
        stop_names = []
        url = 'https://transport.tamu.edu/BusRoutesFeed/api/route/' + route + '/stops'

        response = requests.get(url)

        data = response.text
        parsed = json.loads(data)

        magicLat = 117029.1868  # Conversion number for latitude
        magicLong = 111319.2856  # Conversion number for longitude
        oldLat = 0
        oldLong = 0

        for stop in parsed:
            oldLat = stop['Latitude']  # Original pre converted latitude
            oldLong = stop['Longtitude']  # Original pre converted longitude
            newLat = oldLat / magicLat
            newLong = oldLong / magicLong


            stop_names.append(stop['Name'])
            if stop['Name'] not in stops.keys():
                stops[stop['Name']] = (newLong, newLat)

        buses[route] = stop_names

    with open('stops_data.json', 'w') as fp:
        json.dump(stops, fp)

    with open('bus_data.json', 'w') as fp:
        json.dump(buses, fp)
