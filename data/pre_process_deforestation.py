import geopandas as gpd
import pandas as pd
from modules import abrindo_dados, limpeza_de_dados, reclassificando_vetores, adicionando_dados, caixa_de_ferramentas_vetores
import os


# 1) Download Mapbiomas Alerta (2020-2024)tudo que tiver + & PRODES (2008-2024) 

# 2) Recortar por propriedade e deletar arquivos originais
vault_files = "/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data/"
limite_produtor = abrindo_dados.process_files(vault_files, "pol_props*", "geojson", zipped = False)
limite_produtor
mapbiomas_deforestation_alert = abrindo_dados.process_files(vault_files,
                                                             "*dashboard_*",
                                                             "shp",
                                                               zipped = True)
prodes_deforestation =  abrindo_dados.process_files(vault_files,
                                                     "yearly_*",
                                                     "shp",
                                                       zipped = True)
#clip por propriedade
clip_mapbiomas_deforestation = caixa_de_ferramentas_vetores.clip_vector_by_vector(mapbiomas_deforestation_alert, limite_produtor)
clip_mapbiomas_deforestation.to_file(os.path.join(vault_files, 'mapbiomas_deforestation_alert_clip.geojson'),
                                      driver = 'GeoJSON')
print(clip_mapbiomas_deforestation.shape)
print(clip_mapbiomas_deforestation.head(10))
#clip por propriedade
clip_prodes_deforestation = caixa_de_ferramentas_vetores.clip_vector_by_vector(prodes_deforestation, limite_produtor)
print(clip_prodes_deforestation.shape)
print(clip_prodes_deforestation.head(10))
clip_prodes_deforestation.to_file(os.path.join(vault_files, 'prodes_deforestation_clip.geojson'), driver = 'GeoJSON')

# 3) Pivotar desmates por propriedade e ano


# 3) Pivotar uso do solo para o ano de 2023




# 4)Se der tempo baixar de 2013 também para comparar área de café com 2023

# Perguntar pro Caio como faço para rodar códigos no Vscode & lidar com pouca memória local
