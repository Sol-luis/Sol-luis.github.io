import os
import geopandas as gpd
import pandas as pd
import fnmatch as fn
import zipfile
import re
from modules import abrindo_dados, reclassificando_vetores, adicionando_dados


### Abrindo arquivos xlsx e shapefile ###
vault_files = "/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data"
uso_solo =  abrindo_dados.process_files(vault_files, "*uso_do_solo*", 'geojson')
uso_solo = uso_solo[uso_solo['raster_val'] > 0]
print(uso_solo.raster_val.value_counts().reset_index().sort_values(by=['index']))
uso_solo_reclass =  reclassificando_vetores.reclassificando_classes_uso_solo_mapbiomas(uso_solo)
print(uso_solo_reclass.classe_uso_solo_mapbiomas.unique())
uso_solo_reclass.to_file(os.path.join(vault_files, 'es_uso_solo_vetor_reclassificado.geojson'), driver = 'GeoJSON')

