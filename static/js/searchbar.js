var country_search = d3.select("#submit")

country_search.on("click", function(){
    d3.event.preventDefault();
    
    var user_input_country = d3.select("#user_country").node().value;
    d3.select("#user_country").node().value = "";
    
    // this runs clean_format function with user_input then runs callback func.
    clean_format(user_input_country, function(cleaned_input){
        console.log(`successfuly changed -> ${cleaned_input}`)

        d3.json(`/cities/${cleaned_input}`, function(error, response){

            // send it to markermap function to create a map
            markermap(response)
        })
    })
});

function clean_format(user_input_country, callback){
    const splitted = user_input_country.split(" ");
    // if no space in country name
    if (splitted.length === 1){
        cleaned_input = user_input_country.charAt(0).toUpperCase() + user_input_country.slice(1).toLowerCase()
    }
    // if space --> titlecase all other than of/and,...etc.
    else{
        for (var i=0; i <splitted.length; i++) { 
            // titlecase if word is not "of" or "and"
            if (splitted[i] != "of" && splitted[i] !="and"){
                splitted[i] = splitted[i].charAt(0).toUpperCase() + splitted[i].slice(1).toLowerCase()
            }
        }
        cleaned_input = splitted.join(" ")
    }

    // after above step, run call back function()
    callback(cleaned_input);
}
