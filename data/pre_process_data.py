import os
import geopandas as gpd
import pandas as pd
import fnmatch as fn
import zipfile
import re
from modules import abrindo_dados, limpeza_de_dados, reclassificando_vetores, adicionando_dados


### Abrindo arquivos xlsx e shapefile ###
vault_files = "/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data"

xlsx = abrindo_dados.process_files(vault_files, "*_produtores*","xlsx")
limite = abrindo_dados.process_files(vault_files, "*_IMOVEL_*", "shp", zipped = True)
uso_solo =  abrindo_dados.process_files(vault_files, "*uso_do_solo*", 'geojson')

#Limpando dados
xlsx = limpeza_de_dados.clean_header(xlsx) #homogeneizando cabeçalho
xlsx_car = xlsx[["car", "produtor"]]

### encontrando correspondências para Espacializar os dados a partir do CAR ###
xlsx_car_lj_limite = xlsx_car.merge(limite, how='left',left_on="car", right_on="cod_imovel", indicator=True)
export_bd = xlsx_car_lj_limite.drop(columns=['_merge'], inplace=False) #retirando coluna _merge
export_bd = gpd.GeoDataFrame(export_bd, geometry='geometry') #criando Geodataframe
export_bd = adicionando_dados.add_area(export_bd) #Calculando área em hectares
export_bd["status_car"] = export_bd["ind_status"].apply(reclassificando_vetores.reclass_car)

### Exportando resultados para pasta correspondente ###
# export_bd.to_file(os.path.join(vault_files,'pol_props_ES.geojson'), driver="GeoJSON", encoding='utf-8')
