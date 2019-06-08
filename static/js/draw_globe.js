var globe = planetaryjs.planet();
var canvas = document.getElementById('globe');

function autorotate(degPerSec) {
    // Planetary.js plugins are functions that take a `planet` instance
    // as an argument...
    return function(planet) {
        var lastTick = null;
        var paused = false;
        planet.plugins.autorotate = {
        pause:  function() { paused = true;},
        resume: function() { paused = false;}
        };
        // ...and configure hooks into certain pieces of its lifecycle.
        planet.onDraw(function() {
        if (paused || !lastTick) {
            lastTick = new Date();
        } else {
            var now = new Date();
            var delta = now - lastTick;
            // This plugin uses the built-in projection (provided by D3)
            // to rotate the globe each time we draw it.
            var rotation = planet.projection.rotate();
            rotation[0] += degPerSec * delta / 1000;
            if (rotation[0] >= 180) rotation[0] -= 360;
            planet.projection.rotate(rotation);
            lastTick = now;
        }})
    }};
    
    
    // The `zoom` and `drag` plugins enable
    // manipulating the globe with the mouse.
    globe.loadPlugin(planetaryjs.plugins.zoom({
    scaleExtent: [300, 500] // [min, max]
    }));
    
    globe.loadPlugin(planetaryjs.plugins.drag({
    // Dragging the globe should pause the
    // automatic rotation until we release the mouse.
    onDragStart: function() {
        this.plugins.autorotate.pause();
    },
    onDragEnd: function() {
        this.plugins.autorotate.resume();
    }
    }));
    
    // calling autorotate plugin built above.
    globe.loadPlugin(autorotate(1));
    globe.loadPlugin(planetaryjs.plugins.earth({
    oceans:   { fill:   '#000080' },
    land:     { fill:   '#339966' },
    borders:  { stroke: '#008000' }
    }));
    
    
    
    
    
    
    
    
    // Make the planet fit well in its canvas
    globe.projection
        .scale(canvas.width/2)
        .translate([canvas.width / 2, canvas.height/2]);
    
    globe.draw(canvas);