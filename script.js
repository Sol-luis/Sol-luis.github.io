var map = L.map('map').setView([-19.46, -40.42], 8);

// Add a tile layer (Imagery from ArcGIS)
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  // attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
}).addTo(map);

// Add coordinates panel
var coordsPanel = L.control({ position: 'bottomleft' });
coordsPanel.onAdd = function (map) {
  var div = L.DomUtil.create('div', 'coords-panel');
  div.style.backgroundColor = 'white';
  div.style.padding = '5px';
  div.style.border = '1px solid #ccc';
  div.style.fontSize = '11px';
  div.innerHTML = 'Latitude: <span id="lat">-</span>, Longitude: <span id="lng">-</span>';
  return div;
};
coordsPanel.addTo(map);

map.on('mousemove', function (e) {
  document.getElementById('lat').innerText = e.latlng.lat.toFixed(6);
  document.getElementById('lng').innerText = e.latlng.lng.toFixed(6);
});

// Fetch GeoJSON for rural properties
fetch('data/pol_props_ES.geojson')
  .then(response => response.json())
  .then(data => {
    var polPropsLayer = L.geoJSON(data, {
      style: function (feature) {
        var fillColor;
        if (feature.properties.status_car === 'Ativo') {
          fillColor = 'yellow';
        } else if (feature.properties.status_car === 'Cancelado') {
          fillColor = 'red';
        } else {
          fillColor = 'grey';
        }
        return {
          color: fillColor,
          weight: 3,
          fillOpacity: 0.1
        };
      },
      onEachFeature: function (feature, layer) {
        var tooltipContent =
          "<strong>Área da propriedade:</strong> " + feature.properties.area_hectares + "<br>" +
          "<strong>CAR:</strong> " + feature.properties.car + "<br>" +
          "<strong>Nome do produtor:</strong> " + feature.properties.produtor + "<br>" +
          "<strong>Municipio:</strong> " + feature.properties.municipio + "<br>" +
          "<strong>Status da propriedade:</strong> " + feature.properties.status_car + "<br>";
        layer.bindTooltip(tooltipContent);

        layer.on('mouseover', function (e) {
          layer.bringToFront();
        });
      }
    }).addTo(map);
  });

// Fetch GeoJSON for municipalities
fetch('data/gdf_muni_ES.geojson')
  .then(response => response.json())
  .then(data => {
    var geojsonLayer = L.geoJSON(data, {
      style: function (feature) {
        return {
          color: '#C5C5C5',
          weight: 3,
          dashArray: '5, 10',
          fillOpacity: 0
        };
      },
      interactive: false
    }).addTo(map);

    geojsonLayer.eachLayer(function (layer) {
      var tooltip = layer.bindTooltip(layer.feature.properties.NM_MUN, {
        permanent: true,
        direction: 'center',
        className: 'municipality-label',
        opacity: 0
      });
      layer._tooltip = tooltip.getTooltip(); // Correctly assign tooltip instance
    });

    function toggleLabels() {
      var zoom = map.getZoom();
      geojsonLayer.eachLayer(function (layer) {
        if (zoom > 8.5) {
          layer._tooltip.setOpacity(1);
        } else {
          layer._tooltip.setOpacity(0);
        }
      });
    }

    map.on('zoomend', toggleLabels);
    toggleLabels();

    // Add search control for municipalities
    var searchControl = new L.Control.Search({
      layer: geojsonLayer,
      propertyName: 'NM_MUN',
      zoom: 11,
      textPlaceholder: 'Digite aqui para procurar o município da propriedade'
    });
    map.addControl(searchControl);
  });

// Add legend
var legend = L.control({ position: 'bottomright' });
legend.onAdd = function (map) {
  var div = L.DomUtil.create('div', 'info legend');
  var labels = ['<strong>Legenda</strong>'];
  var categories = ['Limites municipais', 'Propriedades Ativas', 'Propriedades Canceladas'];
  var colors = ['#C5C5C5', 'yellow', 'red'];

  for (var i = 0; i < categories.length; i++) {
    labels.push('<i style="background:' + colors[i] + '"></i> ' + categories[i]);
  }

  div.innerHTML = labels.join('<br>');
  return div;
};
legend.addTo(map);
