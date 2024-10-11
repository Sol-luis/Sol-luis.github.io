//https://leaflet-extras.github.io/leaflet-providers/preview/
var map = L.map('map').setView([-4.3,  -50.05], 8);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data © OpenStreetMap contributors'
}).addTo(map);


fetch('data/gdf_muni.geojson')
  .then(response => response.json())  // Parse the GeoJSON file
  .then(data => {
    L.geoJSON(data).addTo(map);  // Add the GeoJSON layer to the map
  })
  .catch(error => {
    console.error('Error loading the GeoJSON file:', error);
  });
