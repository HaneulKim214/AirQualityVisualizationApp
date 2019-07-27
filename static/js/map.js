function markermap(response){

  var map_center = [response[0]["lat"], response[0]['lng']]
  
  var marker_map = L.map("map", {
    center: map_center, //center depends on user input country
    zoom: 7
  });
  
  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: leaflet_api
}).addTo(marker_map);

var co_2Icon = L.icon({
  // since it is rendered from html, relative path from html
  iconUrl: '../static/images/34498.png',
  iconSize: [33,35],
  iconAnchor: [0,0],
  popupAnchor: [1, 0] // moving popup little to the right [right/-left, down/-up]
})



// $$$$$$$$$$$$$$$$$$$$$$$$$ YOU NEED PLUGIN FOR MarkerClusterGroup
// Creating marker cluster group. after adding all to cluster group, add it to layer.
var markers = new L.markerClusterGroup();
for (var i = 0; i < response.length; i++) {
  // L.marker([response[i]["lat"], response[i]["lng"]],{icon: co_2Icon}).addTo(marker_map);
  markers.addLayer(L.marker([response[i]["lat"], response[i]["lng"]], {icon: co_2Icon})
                  .bindPopup("<p>" + `City = ${response[i]["City"]}<br>
                  Air quality index = ${response[i]["Aqi"]}<br>
                  Time = ${response[i]["time"]}</p>`)                
  );
};
marker_map.addLayer(markers);

}; // markermap function ends
