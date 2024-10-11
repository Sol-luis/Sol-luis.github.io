//https://leaflet-extras.github.io/leaflet-providers/preview/
var map = L.map('map').setView([-4.3,  -50.05], 8);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
}).addTo(map);


fetch('data/gdf_muni.geojson')
  .then(response => response.json())  // Parse do GeoJSON
  .then(data => {
    var geojsonLayer = L.geoJSON(data, //adicionando características a minha layer
      {
        style: function(feature) {
          return {
            color: 'grey',
            weight: 1,
            fillOpacity: 0.3
          };
        },
        onEachFeature: function(feature, layer) {
          // Tooltip content using the fields from GeoJSON properties
          var tooltipContent = 
            "<strong>Nome :</strong> " + feature.properties.nm_mun + "<br>" +
            "<strong>Código do município:</strong> " + feature.properties.cd_mun + "<br>";
          
          // Bind the tooltip to the layer
          layer.bindTooltip(tooltipContent);
        }
      }

    ).addTo(map);  // Add the GeoJSON layer to the map
  // Add search control
    var searchControl = new L.Control.Search({
      layer: geojsonLayer,
      propertyName: 'nm_mun', // The property to search in your GeoJSON data
      zoom: 12, // Zoom to the found feature
      initial: false, // Don't search automatically
      textPlaceholder: 'Digite aqui para procurar o municipio' // Placeholder for the search box
    });

    // Add the search control to the map
    map.addControl(searchControl);
  })
  .catch(error => {
    console.error('Error loading the GeoJSON file:', error);
  });
