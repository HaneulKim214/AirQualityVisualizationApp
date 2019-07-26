// creating html tag with desired attributes and contents.
function RenderTextSummary(summarized_text){
    // since it will render one string for each <p> tag put all string as one item in list
    got_listed = [summarized_text]
    d3.select(".text-summarize").selectAll("p")
            .data(got_listed)
            .enter()
            .append("p")
            .attr("data-aos", "fade-right")
            .attr("data-aos-delay", "50")
            .attr("data-aos-duration", "2000")
            .text(function(summary){ // appending summairzed_text into <p> just created
                return summary;
            });
};