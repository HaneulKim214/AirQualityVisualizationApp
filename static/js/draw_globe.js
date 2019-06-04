var planet = planetaryjs.planet();
var canvas = document.getElementById('globe');
// You can remove this statement if `world-110m.json`
// is in the same path as the HTML page:

// Make the planet fit well in its canvas
planet.projection.scale(250).translate([250, 250]);
planet.draw(canvas); 