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
        // Check the status_car property to set the color dynamically
        var fillColor;
        if (feature.properties.status_car === 'Ativo') {
          fillColor = 'yellow';
        } else if (feature.properties.status_car === 'Cancelado') {
          fillColor = 'red';
        } else {
          fillColor = 'grey';  // Default color for other statuses, if any
        }
        
        return {
          color: fillColor,
          weight: 3,
          fillOpacity: 0.1
        };
      },
      onEachFeature: function(feature, layer) {
        // Tooltip content for pol_props_ES
        var tooltipContent = 
          "<strong>Área da propriedade:</strong> " + feature.properties.area_hectares + "<br>" +
          "<strong>CAR:</strong> " + feature.properties.car + "<br>" +
          "<strong>Status da propriedade:</strong> " + feature.properties.status_car + "<br>";
        
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
          color: '#C5C5C5',
          weight: 3,
          dashArray: '5, 10',
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

// Add legend control
var legend = L.control({ position: 'bottomright' });
legend.onAdd = function (map) {
  var div = L.DomUtil.create('div', 'info legend'),
      labels = ['<strong>Legenda</strong>'],
      categories = ['Limites municipais',
                     'Limite propriedades rurais Ativas',
                      'Limite propriedades rurais Canceladas'],
      colors = ['grey', 'yellow', 'red'];  // Colors corresponding to each layer

  // Loop through the categories and colors to generate the legend
  for (var i = 0; i < categories.length; i++) {
    labels.push(
      '<i style="background:' + colors[i] + '"></i> ' + categories[i]);
  }

  div.innerHTML = labels.join('<br>');
  return div;
};

// Add the legend to the map
legend.addTo(map);

// var layerControl = L.control.layers(baseMaps, overlayMaps).addTo(map);
