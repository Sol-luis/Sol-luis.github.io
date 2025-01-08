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
          "<strong>Area(ha):</strong> " + feature.properties.area_hectares + "<br>" +
          "<strong>CAR:</strong> " + feature.properties.car + "<br>" +
          "<strong>Farmers name:</strong> " + feature.properties.produtor + "<br>" +
          "<strong>Municipality:</strong> " + feature.properties.municipio + "<br>" +
          "<strong>Farm status:</strong> " + feature.properties.status_car + "<br>";
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
      textPlaceholder: 'Search by municipality'
    });
    map.addControl(searchControl);
  });


// Variável para armazenar a camada de uso do solo
var usoSoloLayer;
var usoSoloLegend;

// Função para obter a cor baseada na classe de uso do solo
function getUsoSoloColor(classe) {
  const colors = {
    "Café": "#8B4513",
    "Formação Florestal" :'#1F8D49',     // Marrom escuro
    "Pastagem": "#F0FF00",               // Verde brilhante
    "Outros usos agrícolas": "#FFD700",  // Dourado
    "Corpo d'água": "#1E90FF",           // Azul forte
    "Afloramento Rochoso": "#808080",    // Cinza médio
    "Lavouras perenes": "#6B8E23",       // Verde oliva escuro
    "Lavouras temporárias": "#FFA500",   // Laranja
    "Vegetação Nativa": "#006400",       // Verde escuro
    "Floresta Alagável": "#4682B4"       // Azul acinzentado
  };
  return colors[classe] || "#000000"; // Preto como padrão para classes desconhecidas
}

// Função para adicionar GeoJSON das classes de uso do solo
fetch('data/es_uso_solo_vetor_reclassificado.geojson')
  .then(response => response.json())
  .then(data => {
    usoSoloLayer = L.geoJSON(data, {
      style: function (feature) {
        return {
          color: getUsoSoloColor(feature.properties.classe_uso_solo_mapbiomas),
          weight: 1,
          fillOpacity: 0.7
        };
      },
      onEachFeature: function (feature, layer) {
        var tooltipContent = 
          "<strong>Land uses:</strong> " + feature.properties.classe_uso_solo_mapbiomas + "<br>"
        layer.bindTooltip(tooltipContent);

        layer.on('mouseover', function () {
          layer.bringToFront();
        });
      }
    });
  });

// Função para criar e adicionar a legenda das classes de uso do solo
function createUsoSoloLegend() {
  usoSoloLegend = L.control({ position: 'bottomright' });
  usoSoloLegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');
    var labels = ['<strong>Land use</strong>'];
    var classes = {
      "Coffee": "#8B4513",
      "Forest Formation" :'#1F8D49',     // Marrom escuro
      "Pasture": "#F0FF00",               // Verde brilhante
      "Other Agricultural land uses": "#FFD700",  // Dourado
      "Water": "#1E90FF",           // Azul forte
      "Rocky Outcrop": "#808080",    // Cinza médio
      "Parennial Crop": "#6B8E23",       // Verde oliva escuro
      "Temporary Crop": "#FFA500",   // Laranja
      "Native Forest": "#006400",       // Verde escuro
      "Floodable Forest": "#4682B4"       // Azul acinzentado
  };
    for (var classe in classes) {
      labels.push('<i style="background:' + classes[classe] + '"></i> ' + classe);
    }

    div.innerHTML = labels.join('<br>');
    return div;
  };
}

// Criar a legenda (mas não adicionar ainda)
createUsoSoloLegend();

// Função para alternar entre a legenda e a camada de uso do solo
function toggleUsoSoloLayer() {
  var button = document.querySelector('.toggle-button');
  
  if (map.hasLayer(usoSoloLayer)) {
    // Remover camada de uso do solo e restaurar a legenda original
    map.removeLayer(usoSoloLayer);
    map.removeControl(usoSoloLegend); // Remover legenda de uso do solo
    legend.addTo(map); // Reativar a legenda original
    button.innerHTML = 'Switch to land use view';
    
  } else {
    // Adicionar camada de uso do solo e substituir a legenda
    usoSoloLayer.addTo(map);
    map.removeControl(legend); // Remover a legenda original
    usoSoloLegend.addTo(map); // Adicionar legenda de uso do solo
    button.innerHTML = 'Switch to property limits';
    
  }
}

// Adicionar um botão para alternar a camada
var toggleButton = L.control({ position: 'bottomright' });
toggleButton.onAdd = function (map) {
  var button = L.DomUtil.create('button', 'toggle-button');
  button.innerHTML = 'Switch to land use mode';

  button.onclick = function () {
    toggleUsoSoloLayer();
  };

  return button;
};
toggleButton.addTo(map);


// Add legend
var legend = L.control({ position: 'bottomright' });
legend.onAdd = function (map) {
  var div = L.DomUtil.create('div', 'info legend');
  var labels = ['<strong>Legend</strong>'];
  var categories = ['Municipal limits', 'Active property', 'Cancelled property'];
  var colors = ['#C5C5C5', 'yellow', 'red'];

  for (var i = 0; i < categories.length; i++) {
    labels.push('<i style="background:' + colors[i] + '"></i> ' + categories[i]);
  }
  div.innerHTML = labels.join('<br>');
  return div;
};
legend.addTo(map);
