
// This function gets a list of cities and return list of aqi.
let get_aqi = function(list_of_cities){
    var cities = ["toronto", "montreal"]
    
    var heatArray = []
    cities.forEach(function(city){
        var url = `https://api.waqi.info/feed/${city}/?token=${beijing_api}`
        d3.json(url, function(response){
            if (response.status == "ok"){ // Only considering working api.
                heatArray_element = [response.data.city.geo[0],response.data.city.geo[1], response.data.aqi]    
                heatArray.push(heatArray_element);
                console.log(heatArray)
            };
        });
    });
};

let result = function(list_of_cities,callback){
    callback(list_of_cities, get_aqi);
    return heatArray
}






// Creat [lat,lng, aqi] --> for heatArray
// [[lat,lng,aqi], [lat,lng,aqi],...,[lat,lng,aqi]]