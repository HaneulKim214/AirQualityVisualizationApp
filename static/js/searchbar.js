var country_search = d3.select("#submit")

country_search.on("click", function(){
    d3.event.preventDefault();

    var user_input_country = d3.select("#user_country").node().value;
    
    const splitted = user_input_country.split(" ");

    d3.select("#user_country").node().value = "";
    
    if (splitted.length === 1){
        var user_input_country = user_input_country.charAt(0).toUpperCase() + user_input_country.slice(1).toLowerCase()
    }
    else{
        for (var i=0; i <splitted.length; i++) {
            // titlecase except for the word "of"
            if (splitted[i] != "of"){
                splitted[i] = splitted[i].charAt(0).toUpperCase() + splitted[i].slice(1).toLowerCase()
            }
        }
        var user_input_country = splitted.join(" ")
    };
    
    // countries_cities = {countr1:[1,2,3,4,], countr2:[1,2,3,4,],...}
    if (countries_cities[user_input_country]){
        // title case if only one word.
        var list_of_cities = countries_cities[user_input_country]
        
        console.log(result(list_of_cities, get_aqi));
    }
    else{
        alert("Try different word for your country name.")
    };

    // // Sending variable to python 
    // search(cities);
})
