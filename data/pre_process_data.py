import os
import geopandas as gpd
import pandas as pd
import fnmatch as fn

def process_files(vault_files, pattern, file_type):
    # Define the file extension and function to open files based on type
    if file_type == 'shp':
        list_files = [x for x in os.listdir(vault_files) if x.endswith('.shp') and fn.fnmatch(x, pattern)]
        if list_files:
            gdf_list = [gpd.read_file(os.path.join(vault_files, f)) for f in list_files]
            gdf = pd.concat(gdf_list, ignore_index=True) if len(gdf_list) > 1 else gdf_list[0]
            print(f"Dimensões do(s) arquivo(s) {list_files}: {gdf.shape}")
            return gdf
    if file_type =='kml':
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
    df.columns = [x.replace(' ', '_') for x in df.columns]
    return df

def clean_string(column):
    return column.astype("string").str.replace("-", "", regex=False)\
                                 .str.replace(".", "", regex=False)\
                                 .str.replace(" ", "", regex=False)

def car_to_limit(): # pega uma lista com n de códigos do car e encontra shapefiles correspondentes
    return

def limit_to_data_folder():
    return

### Abrindo arquivos xlsx e shapefile
xslx = pd.read()

### Coluna CAR dos dois bancos no mesmo tipo e formato


### encontrando correspondências


### Exportando resultados para pasta correspondente