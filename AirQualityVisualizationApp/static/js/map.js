function markermap(response){

  var map_center = [response[0]["lat"], response[0]['lng']]
 
  var marker_map = L.map("map",{
    center: map_center,
    zoom: 3
  });
  
  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
    accessToken: leaflet_api
  }).addTo(marker_map);

var co_2Icon = L.icon({
  // since it is rendered from html, relative path from html
  iconUrl: '../static/images/34498.png',
  iconSize: [33,35],
  iconAnchor: [0,0],
  popupAnchor: [1, 0] // moving popup little to the right [right/-left, down/-up]
})

// Creating marker cluster group. after adding all to cluster group, add it to layer.
var markers = new L.markerClusterGroup();
for (var i = 0; i < response.length; i++) {
  o3 = response[i]["o3"]
  so2 = response[i]["so2"]
  no2 = response[i]["no2"]
  pm25 = response[i]["pm25"]
  co = response[i]["co"]

  // L.marker([response[i]["lat"], response[i]["lng"]],{icon: co_2Icon}).addTo(marker_map);
  markers.addLayer(L.marker([response[i]["lat"], response[i]["lng"]], {icon: co_2Icon})
                  .bindPopup(`<p>City = ${response[i]["City"]}<br>` +
                  `Air quality index = ${response[i]["Aqi"]}<br>` +
                  `Time = ${response[i]["time"]}</p>` +
                  `<p> o3 = ${o3}</p>`+
                  `<p> so2 = ${so2}</p>`+
                  `<p> no2 = ${no2}</p>`+
                  `<p> pm25 = ${pm25}</p>`+
                  `<p> co = ${co}</p>`)                
  );
};
marker_map.addLayer(markers);

}; // markermap function ends

