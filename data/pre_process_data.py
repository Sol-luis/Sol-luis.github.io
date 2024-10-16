import os
import geopandas as gpd
import pandas as pd
import fnmatch as fn
import zipfile
import re

def process_files(vault_files, pattern, file_type, zipped=False):
    def process_vsizip(zip_path, file_ext):
        # Create the /vsizip/ path for GDAL to read directly from the zip
        with zipfile.ZipFile(zip_path, 'r') as z:
            list_files = [f for f in z.namelist() if f.endswith(file_ext) and fn.fnmatch(f, pattern)]
            if list_files:
                # Using /vsizip/ to read the file directly from the zip archive
                zip_vsi_path = f'/vsizip/{zip_path}/{list_files[0]}'
                if file_ext == '.shp':
                    gdf = gpd.read_file(zip_vsi_path)
                    print(f"Dimensões do arquivo {list_files[0]}: {gdf.shape}")
                    return gdf
                elif file_ext == '.kml':
                    kml = gpd.read_file(zip_vsi_path)
                    print(f"Dimensões do arquivo {list_files[0]}: {kml.shape}")
                    return kml
                elif file_ext == '.xlsx':
                    xlsx = pd.read_excel(zip_vsi_path)
                    print(f"Dimensões do arquivo {list_files[0]}: {xlsx.shape}")
                    return xlsx
            print("Nenhum arquivo correspondente encontrado no ZIP.")
            return None

    if zipped:
        zip_files = [x for x in os.listdir(vault_files) if x.endswith('.zip')]
        if zip_files:
            print(f"Arquivos ZIP encontrados: {zip_files}")
            for zip_file in zip_files:
                zip_path = os.path.join(vault_files, zip_file)
                if file_type == 'shp':
                    return process_vsizip(zip_path, '.shp')
                elif file_type == 'kml':
                    return process_vsizip(zip_path, '.kml')
                elif file_type == 'xlsx':
                    return process_vsizip(zip_path, '.xlsx')
                elif file_type == 'tif':
                    return process_vsizip(zip_path, '.tif')
        else:
            print("Nenhum arquivo ZIP encontrado.")
            return None
    else:
        # Process normal (unzipped) files
        if file_type == 'shp':
            list_files = [x for x in os.listdir(vault_files) if x.endswith('.shp') and fn.fnmatch(x, pattern)]
            if list_files:
                gdf_list = [gpd.read_file(os.path.join(vault_files, f)) for f in list_files]
                gdf = pd.concat(gdf_list, ignore_index=True) if len(gdf_list) > 1 else gdf_list[0]
                print(f"Dimensões do(s) arquivo(s) {list_files}: {gdf.shape}")
                return gdf
        elif file_type == 'kml':
            list_files = [x for x in os.listdir(vault_files) if x.endswith('.kml') and fn.fnmatch(x, pattern)]
            if list_files:
                kml = gpd.read_file(os.path.join(vault_files, list_files[0]))
                print(f"Dimensões do arquivo {list_files[0]}: {kml.shape}")
                return kml
        elif file_type == 'xlsx':
            list_files = [x for x in os.listdir(vault_files) if fn.fnmatch(x, pattern)]
            if list_files:
                xlsx = pd.read_excel(os.path.join(vault_files, list_files[0]))
                print(f"Dimensões do arquivo {list_files[0]}: {xlsx.shape}")
                return xlsx
        elif file_type == 'tif':
            list_files = [x for x in os.listdir(vault_files) if x.endswith('.tif')]
            print("Arquivos de imagem .tif:")
            for tif in list_files:
                print(tif)
            return list_files
        else:
            print("Tipo de arquivo não reconhecido.")
            return None

def clean_header(df):
    df.columns = [x.lower() for x in df.columns]
    df.columns = [x.strip() for x in df.columns]
    df.columns = [x.replace(' ', '_') for x in df.columns]
    return df

def add_area(df):
    df = df.to_crs(epsg=5880)
    df["area_hectares"] = df['geometry'].area/10000
    df["area_hectares"] = df["area_hectares"].round(4)
    #retornando ao crs original
    df = df.to_crs(epsg=4674)
    return df

def reclass_car(x):
    cl1 = re.compile("AT")
    cl2 = re.compile("CA")
    cl3 = re.compile("PE")
    if cl1.match(x):
        return "Ativo"
    elif cl2.match(x):
        return "Cancelado"
    elif cl3.match(x):
        return "Pendente"


### Abrindo arquivos xlsx e shapefile
vault_files = "/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data"
xlsx = process_files(vault_files, "*_produtores*","xlsx")
xlsx = clean_header(xlsx)
xlsx_car = xlsx[["car"]]
print(xlsx_car.info())
limite = process_files(vault_files, "*_IMOVEL_*", "shp", zipped = True)
print(limite.info())

### Coluna CAR dos dois bancos no mesmo tipo e formato

### encontrando correspondências
xlsx_car_lj_limite = xlsx_car.merge(limite, how='left',left_on="car", right_on="cod_imovel", indicator=True)
export_bd = xlsx_car_lj_limite.drop(columns=['_merge'], inplace=False)
export_bd = gpd.GeoDataFrame(export_bd, geometry='geometry')
export_bd = add_area(export_bd)
export_bd["status_car"] = export_bd["ind_status"].apply(reclass_car)
print(export_bd.ind_status.value_counts())
print(export_bd.status_car.value_counts())

### Exportando resultados para pasta correspondente
export_bd.to_file(os.path.join(vault_files,'pol_props_ES.geojson'), driver="GeoJSON", encoding='utf-8')