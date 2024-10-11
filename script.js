//https://leaflet-extras.github.io/leaflet-providers/preview/
var map = L.map('map').setView([-4.3,  -50.05], 8);
L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.{ext}', {
  attribution: '&copy; CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | &copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	ext: 'jpg'
}).addTo(map);


fetch('data/gdf_muni.geojson')
  .then(response => response.json())  // Parse do GeoJSON
  .then(data => {
    L.geoJSON(data, //adicionando características a minha layer
      {
        style: function(feature) {
          return {
            color: 'black',
            weight: 1,
            fillOpacity: 0.5
          };
        },
        onEachFeature: function(feature, layer) {
          // Tooltip content using the fields from GeoJSON properties
          var tooltipContent = 
            "<strong>Nome :</strong> " + feature.properties.nm_mun + "<br>" +
            "<strong>Grupo:</strong> " + feature.properties.cd_mun + "<br>";
          
          // Bind the tooltip to the layer
          layer.bindTooltip(tooltipContent);
        }
      }

    ).addTo(map);  // Add the GeoJSON layer to the map
  })
  .catch(error => {
    console.error('Error loading the GeoJSON file:', error);
  });
