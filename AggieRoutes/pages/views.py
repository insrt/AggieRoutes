from django.shortcuts import render
from .forms import LocationForm
import requests, json

def home_view(request, *args, **kwargs):
	#default lat and lng -- MSC coords
	lat = 30.6102898
	lng = -96.3370759
	if(request.method=="POST"):
		form = LocationForm(request.POST)
		if(form.is_valid()):
			location = request.POST['location']
			api_key="AIzaSyACZvbk-O8xlqcPxNzjNEGQyDlGjaeUezk"

			#get formal address from Google Place Search API
			url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='{location}'&inputtype=textquery&fields=formatted_address&radius=25000&key={key}".format(location=location,key=api_key)
			response = requests.get(url)
			address = response.json()
			print(address)
			if(address != ""):
				print("ADDRESS:%s" % address)
				parsed_address= address["candidates"][0]["formatted_address"]

				#get latitude and longitude from Google Geocode API
				url2 = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}".format(address=parsed_address,key=api_key)
				response2 = requests.get(url2)
				latlong = response2.json()
				lat = latlong["results"][0]["geometry"]["location"]["lat"]
				lng = latlong["results"][0]["geometry"]["location"]["lng"]
				print("Latitude:%s" % lat)
				print("Longitude:%s" % lng)
	else:
		form = LocationForm()
	return render(request, "index.html", {'form':form,'lat':lat,'lng':lng})#{'lat':lat, 'lng':lng},)



def map_view(request, *args, **kwargs):

	return render(request, "map.html")
	
	