//https://leaflet-extras.github.io/leaflet-providers/preview/
var map = L.map('map').setView([-4.3,  -50.05], 8);
L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.{ext}', {
  attribution: '&copy; CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | &copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	ext: 'jpg'
}).addTo(map);


fetch('data/gdf_muni.geojson')
  .then(response => response.json())  // Parse the GeoJSON file
  .then(data => {
    L.geoJSON(data).addTo(map);  // Add the GeoJSON layer to the map
  })
  .catch(error => {
    console.error('Error loading the GeoJSON file:', error);
  });
