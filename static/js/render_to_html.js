// creating html tag with desired attributes and contents.
function RenderTextSummary(summarized_text){
    // since it will render one string for each <p> tag put all string as one item in list
    got_listed = ["placeholder",summarized_text]
    d3.select(".text-summarize").selectAll("p")
            .data(got_listed)
            .enter() // creating new p tag
            .append("p")
            .attr("data-aos", "zoom-in")
            .attr("data-aos-delay", "150")
            .attr("data-aos-duration", "3000")
            .text(function(summary){ // appending summairzed_text into <p> just created
                return summary;
            });
};

function RenderURL(country_name){
    url = [`https://en.wikipedia.org/wiki/${country_name}`]

    d3.select(".text-summarize").selectAll("a")
            .data(url)
            .enter()
            .append("p")
            .classed("wiki-url", true).text("Original article : ")
            .attr("data-aos", "fade-right")
            .attr("data-aos-delay", "150")
            .attr("data-aos-duration", "2000")
            .append("a")
            .attr("href", url)
            .text(function(data){
                return data;
            });
};

function RenderTitle(country_name){
    data = [country_name]

    d3.select(".text-summarize").selectAll("h3")
            .data(data)
            .enter()
            .append('h3')
            .attr("data-aos", "fade-down")
            .attr("data-aos-duration", "2000")
            .text(function(d){
                return d;
            });
};

function RenderMap(){
    data = [1]
    d3.select("map-container").selectAll("div")
            .data(data)
            .enter()
            .append("div")
            .attr("id", "map");
}