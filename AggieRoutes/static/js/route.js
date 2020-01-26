//import * as views from pages.views;

var map;
function initMap() {
  const center = {lat: 30.61353, lng: -96.34167};
  const options = {zoom: 15, scaleControl: true, center: center};
  map = new google.maps.Map(
    document.getElementById('map'), options);
// Locations of landmarks
//30.6102898,-96.3370759    MSC
// 30.61353, -96.34167      Bus stop

  var defaultBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(30.381617, -96.569054),
    new google.maps.LatLng(30.818559, -95.985715))

  var opt = {
    bounds: defaultBounds
  }

  var input = document.getElementById('pac-input');
  map.controls.push(input);

  // var autocomplete = new google.maps.places.Autocomplete(input,opt);
  var MSC = {lat: dest_lat, lng: dest_lng};
  const Bus_Stop = {lat: 30.61353, lng: -96.34167};
  

  var mk1 = new google.maps.Marker({position: MSC, map: map});
  var mk2 = new google.maps.Marker({position: Bus_Stop, map: map});
  
  let directionsService = new google.maps.DirectionsService();
  let directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map); 

  const route = {
      origin: MSC,
      destination: Bus_Stop,
      travelMode: 'WALKING'
  }

directionsService.route(route,
  function(response, status) { 
    if (status !== 'OK') {
      window.alert('Directions request failed due to ' + status);
      return;
    } else {
      directionsRenderer.setDirections(response); 
      var directionsData = response.routes[0].legs[0]; 
      if (!directionsData) {
        window.alert('Directions request failed');
        return;
      }
      //Print message about distance and time
      else {
        document.getElementById('msg').innerHTML += directionsData.distance.text + " (" + directionsData.duration.text + ").";
      }
    }
  });
}