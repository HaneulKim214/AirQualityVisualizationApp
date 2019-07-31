var country_search = d3.select("#submit")

country_search.on("click", function(){
    d3.event.preventDefault();
    
    var user_input_country = d3.select("#user_country").node().value;
    d3.select("#user_country").node().value = "";
    
    // this runs clean_format function with user_input then runs callback func.
    clean_format(user_input_country, function(cleaned_input){
        // two api calls: 1. for marker map  2. for nlp
        d3.json(`/cities/${cleaned_input}`, function(error, response){
            map = d3.select(".map-container")
            map.selectAll("div").remove();
            // create div with id=map inside .map-container before we input map inside of it.
            CreateMapTag();
            
            // run markermap function after 3s.
            setTimeout(function(){ markermap(response) }, 1000); // this inserts map in to tag that has id="map"
        });
        d3.json(`/nlp/${cleaned_input}`, function(error, summarized_text){
            // empty DOM element before rendering new country
            div = d3.select(".text-summarize");
            div.selectAll("p").remove();
            div.selectAll("h3").remove();
            
            // receive summarized text from python
            RenderTitle(cleaned_input);                
            RenderURL(cleaned_input);
            RenderTextSummary(summarized_text);
        });
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
