import os
import geopandas as gpd
import pandas as pd
import fnmatch as fn
import zipfile
import re
from modules import abrindo_dados, reclassificando_vetores, adicionando_dados


### Abrindo arquivos xlsx e shapefile ###
vault_files = "/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data"
uso_solo =  abrindo_dados.process_files(vault_files, "es_uso_do_solo_vetor.geojson", 'geojson')
uso_solo = uso_solo[uso_solo['raster_val'] > 0]
print(uso_solo.raster_val.value_counts().reset_index().sort_values(by=['index']))

#English
uso_solo_reclass =  reclassificando_vetores.reclassificando_classes_uso_solo_mapbiomas_eng(uso_solo)
print(uso_solo_reclass.classe_uso_solo_mapbiomas.unique())
uso_solo_reclass.to_file(os.path.join(vault_files, 'es_uso_solo_vetor_reclassificado_eng.geojson'), driver = 'GeoJSON')

#Português
uso_solo_reclass =  reclassificando_vetores.reclassificando_classes_uso_solo_mapbiomas_pt(uso_solo)
print(uso_solo_reclass.classe_uso_solo_mapbiomas.unique())
uso_solo_reclass.to_file(os.path.join(vault_files, 'es_uso_solo_vetor_reclassificado_pt.geojson'), driver = 'GeoJSON')


