var country_search = d3.select("#submit")

country_search.on("click", function(){
    d3.event.preventDefault();

    var user_input_country = d3.select("#user_country").node().value;
    
    // making it Titlecased
    var user_input_country = user_input_country.charAt(0).toUpperCase() + user_input_country.slice(1).toLowerCase()

    d3.select("#user_country").node().value = "";
    
    var cities = countries_cities[user_input_country] 
    console.log(cities)
    // // Sending variable to python 
    // search(cities);
})
