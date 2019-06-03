var api_key = "53efafc18c686b9dcae32b983edb6db4f3ef23d8"
// Loop through each cities in canada and perform API call
var Cities = [];
var AQI = [];
canadian_cities.forEach(function(city){
	var url = `https://api.waqi.info/feed/${city}/?token=${api_key}`
	
	// call api
	d3.json(url).then(function(response){
		// ignore calls with status:error => no station in that city
		if (response.status == "ok"){
			console.log(response);
			
			// Create array of Cities, AQI,
			Cities.push(city);
			// console.log(Cities);
		};
	});
	
});


// var url = `https://api.waqi.info/feed/toronto/?token=${api_key}`
// 	d3.json(url).then(function(response){
// 		console.log(response.status);
// 		// AQI of the city
// 		console.log(response.data.aqi);
	
// 		// different pollutants
// 		console.log(response.data.iaqi);
// 	});


// function from choropleth_globe.js that draws 3-d globe
drawGlobe();


// from js api call --> pass it to python and save it into db --> grab data from different
// js function
