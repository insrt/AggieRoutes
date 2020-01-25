from django.shortcuts import render
import requests, json

def home_view(request, *args, **kwargs):
	
	return render(request, "index.html")

def map_view(request, *args, **kwargs):
	location = request.POST.get("location")
	api_key="AIzaSyACZvbk-O8xlqcPxNzjNEGQyDlGjaeUezk"
	url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={location}&inputtype=textquery&fields=formatted_address,place_id&key={key}".format(location=location,key=api_key)
	address = requests.get(url)
	response = address.json()
	print(response)
	return render(request, "map.html")
	
	