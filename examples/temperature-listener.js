const { spawn } = require('child_process');
// Storage for the readings.
const temperatures = [];

const sensor = spawn('spawn', ['sensor.py']);
sensor.stdout.on('data', function(data) {
    // Coerce Buffer object to Float
    temperatures.push(parseFloat(data));

    // Log to debug
    console.log(temperatures);
});