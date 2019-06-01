var api_key = "53efafc18c686b9dcae32b983edb6db4f3ef23d8"

var city = "beijing"
var url = `https://api.waqi.info/feed/${city}/?token=${api_key}`

d3.json(url).then(function(data){
    console.log(data);
});