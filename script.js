//https://leaflet-extras.github.io/leaflet-providers/preview/
var map = L.map('map').setView([-4.3,  -50.05], 8);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
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
