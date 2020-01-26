from django.shortcuts import render
from .forms import LocationForm
from django.conf import settings
import numpy as np 
import requests, json

def bus_locations(origin, dest):
	with open(settings.BASE_DIR + settings.STATIC_URL + 'json/bus_data.json') as json_file:
	    bus_data = json.load(json_file)

	with open(settings.BASE_DIR + settings.STATIC_URL + 'json/stops_data.json') as json_file:
	    stops_data = json.load(json_file)

	origin = np.array(origin)

	best = np.inf
	orig_stop = {}
	stop_dest = {}
	for stop_name in stops_data:
		candidate = np.array((stops_data[stop_name][0], stops_data[stop_name][1]))
		orig_stop[stop_name] = np.linalg.norm(origin-candidate)
		stop_dest[stop_name] = np.linalg.norm(candidate-dest)

	for stop_0 in orig_stop:
		for stop_1 in stop_dest:
			for bus in bus_data:
				if stop_0 in bus_data[bus] and stop_1 in bus_data[bus]:
					dist = orig_stop[stop_0] + stop_dest[stop_1]

					if dist < best:
						best = dist
						best_bus = bus
						start = stop_0
						stop = stop_1

	return (start, stops_data[start]), (stop, stops_data[stop]), best_bus


def home_view(request, *args, **kwargs):
	#default lat and lng -- MSC coords
	#lat = 30.6102898
	#lng = -96.3370759
	orig_lat = ""
	orig_lng = ""
	dest_lat = ""
	dest_lng = ""

	if(request.method=="POST"):
		api_key="AIzaSyACZvbk-O8xlqcPxNzjNEGQyDlGjaeUezk"
		form = LocationForm(request.POST)
		#proceed if form is valid
		if(form.is_valid()):
			#gets coords for starting point
			origin = request.POST['origin']
			print("ORIGIN:%s"%origin)
			#get formal address from Google Place Search API
			url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={location}&inputtype=textquery&fields=formatted_address&radius=25000&key={key}".format(location=origin,key=api_key)
			response = requests.get(url)
			address = response.json()
			if(address != ""):
				parsed_address= address["candidates"][0]["formatted_address"]

				#get latitude and longitude from Google Geocode API
				url2 = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}".format(address=parsed_address,key=api_key)
				response2 = requests.get(url2)
				orig_latlong = response2.json()
				orig_lat = orig_latlong["results"][0]["geometry"]["location"]["lat"]
				orig_lng = orig_latlong["results"][0]["geometry"]["location"]["lng"]

			#gets coords for destination
			dest = request.POST['dest']
			#get formal address from Google Place Search API
			url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='{location}'&inputtype=textquery&fields=formatted_address&radius=25000&key={key}".format(location=dest,key=api_key)
			response = requests.get(url)
			address = response.json()
			if(address != ""):
				parsed_address= address["candidates"][0]["formatted_address"]

				#get latitude and longitude from Google Geocode API
				url2 = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}".format(address=parsed_address,key=api_key)
				response2 = requests.get(url2)
				dest_latlong = response2.json()
				dest_lat = dest_latlong["results"][0]["geometry"]["location"]["lat"]
				dest_lng = dest_latlong["results"][0]["geometry"]["location"]["lng"]
				(start_bus, start_loc), (stop_bus, stop_loc), best_bus = bus_locations((orig_lng,orig_lat),(dest_lng,dest_lat))

	else:
		form = LocationForm()
	return render(request, "index.html", {'form':form,'orig_lat':orig_lat,'orig_lng':orig_lng,'dest_lat':dest_lat,'dest_lng':dest_lng, 'start_bus':start_bus, 'start_loc':start_loc, 'stop_bus':stop_bus, 'stop_loc':stop_loc, 'best_bus':best_bus})#{'lat':lat, 'lng':lng},)



def map_view(request, *args, **kwargs):

	return render(request, "map.html")
	
	