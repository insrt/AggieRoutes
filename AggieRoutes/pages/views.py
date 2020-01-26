from django.shortcuts import render
from .forms import LocationForm
import requests, json

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
				print("Origin Latitude:%s" % orig_lat)
				print("Origin Longitude:%s" % orig_lng)

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
				print("Dest Latitude:%s" % dest_lat)
				print("Dest Longitude:%s" % dest_lng)

	else:
		form = LocationForm()
	return render(request, "index.html", {'form':form,'orig_lat':orig_lat,'orig_lng':orig_lng,'dest_lat':dest_lat,'dest_lng':dest_lng})#{'lat':lat, 'lng':lng},)



def map_view(request, *args, **kwargs):

	return render(request, "map.html")
	
	