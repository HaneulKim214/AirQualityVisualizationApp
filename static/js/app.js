
var country_lat_lng = [56.1304, -106.3468]

var heatmap = L.map("map", {
  center: country_lat_lng, //center depends on user input country
  zoom: 5
});

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: leaflet_api
}).addTo(heatmap);

var heat_array = [[56.133, 30.5, 0.2],
[56.6, 30.4, 0.5]]

// var heat = L.heatLayer(heat_array,{
  //     radius: 25
  //     }).addTo(heatmap);