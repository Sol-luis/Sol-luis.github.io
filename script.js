//https://leaflet-extras.github.io/leaflet-providers/preview/
var map = L.map('map').setView([-20.28, -41.51], 8);

// Add a tile layer (Imagery from ArcGIS)
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
}).addTo(map);

// Fetch GeoJSON pol_props_ES (smaller polygons)
fetch('data/pol_props_ES.geojson')
  .then(response => response.json())  // Parse the GeoJSON file
  .then(data => {
    var polPropsLayer = L.geoJSON(data, {
      style: function(feature) {
        return {
          color: 'blue',
          weight: 1,
          fillOpacity: 0.3
        };
      },
      onEachFeature: function(feature, layer) {
        // Tooltip content for pol_props_ES
        var tooltipContent = 
          "<strong>Módulos Fiscais:</strong> " + feature.properties.mod_fiscal + "<br>" +
          "<strong>Tipo de propriedade:</strong> " + feature.properties.ind_tipo + "<br>"+
          "<strong>Municipio da propriedade:</strong> " + feature.properties.municipio + "<br>";
        
        // Bind tooltip to the layer
        layer.bindTooltip(tooltipContent);

        // Bring smaller polygons to front on mouseover
        layer.on('mouseover', function(e) {
          layer.bringToFront();
        });
      }
    }).addTo(map);

    // Make sure the smaller layer is brought to the front initially
    polPropsLayer.eachLayer(function(layer) {
      layer.bringToFront();
    });
  });

// Fetch GeoJSON gdf_muni_ES (larger polygons)
fetch('data/gdf_muni_ES.geojson')
  .then(response => response.json())  // Parse the GeoJSON file
  .then(data => {
    var geojsonLayer = L.geoJSON(data, {
      style: function(feature) {
        return {
          color: 'white',
          weight: 3,
          fillOpacity: 0
        };
      },
      interactive: false  // Disable interactions with the larger polygons
    }).addTo(map);  // Add the GeoJSON layer to the map

    // Add search control for municipalities
    var searchControl = new L.Control.Search({
      layer: geojsonLayer,
      propertyName: 'NM_MUN', // Field in GeoJSON to search
      zoom: 12,            // Zoom to the feature when found
      initial: false,      // Don't search automatically
      textPlaceholder: 'Digite aqui para procurar o município da propriedade',  // Placeholder text
      autoType: true, 
    });

    // Add the search control to the map
    map.addControl(searchControl);
  })
  .catch(error => console.error('Error loading GeoJSON:', error));  // Error handling