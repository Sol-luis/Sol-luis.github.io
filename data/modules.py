import rasterio
from rasterio.mask import mask
import geopandas as gpd
from rasterio.features import shapes
import pandas as pd
import os
import fnmatch as fn
import zipfile

class abrindo_dados:
    @staticmethod
    def process_files(vault_files, pattern, file_type, zipped=False):
        """
        Esta função abre arquivos de diferentes tipos (Shapefile, KML, XLSX, TIF) a partir de um diretório. 
        Ela também pode lidar com arquivos compactados (.zip) e ler arquivos dentro desses ZIPs diretamente sem a necessidade de extraí-los. 

        Parâmetros:
        - vault_files (str): Caminho para o diretório onde os arquivos estão localizados.
        - pattern (str): Padrão do nome do arquivo para identificar quais arquivos devem ser abertos.
                        Usa expressões de padrão, por exemplo, `arquivo_*` para arquivos que começam com 'arquivo_'.
        - file_type (str): Tipo do arquivo a ser processado. Pode ser 'shp', 'kml', 'xlsx' ou 'tif'.
        - zipped (bool): Indica se os arquivos estão compactados em formato ZIP. Se True, procura por arquivos dentro dos ZIPs.

        Retorna:
        - gpd.GeoDataFrame ou pd.DataFrame: Um GeoDataFrame ou DataFrame contendo os dados dos arquivos processados, 
                                            dependendo do tipo de arquivo (Shapefile e KML retornam GeoDataFrame; XLSX retorna DataFrame).
        - list: Uma lista dos arquivos TIF encontrados (se file_type for 'tif' e não estiver em ZIP).
        - None: Se nenhum arquivo correspondente for encontrado ou se o tipo de arquivo não for suportado.

        Funcionalidades:
        - Lê arquivos de vários formatos diretamente de um diretório ou dentro de arquivos ZIP, usando um padrão de nome.
        - Lida com os seguintes tipos de arquivos:
        - `shp` (Shapefile): Lê arquivos de shapefiles e retorna um GeoDataFrame com os dados.
        - `kml` (KML): Lê arquivos KML e retorna um GeoDataFrame com os dados.
        - `xlsx` (Excel): Lê arquivos Excel e retorna um DataFrame com os dados.
        - `tif` (Imagem): Lista arquivos TIF disponíveis no diretório ou dentro do ZIP, mas não carrega os dados.
        """
    
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
            # Processando sem .zip
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

class caixa_de_ferramentas_raster:
    @staticmethod
    def clip_raster_by_shapefile(raster_path, shapefile_path, output_path):
        with rasterio.open(raster_path) as src:
            shapefile = gpd.read_file(shapefile_path) #lendo vetor
            shapefile = shapefile.to_crs(src.crs) #transformando coordenada do vetor para coordenada do raster
            out_image, out_transform = mask(src,
                                            shapefile.geometry,
                                            crop=True)
            out_meta = src.meta.copy()
            # Update metadata
            out_meta.update({"driver": "GTiff",
                            "height": out_image.shape[1],
                            "width": out_image.shape[2],
                            "transform": out_transform})
            # Write raster
            with rasterio.open(output_path, "w", **out_meta) as dest:
                dest.write(out_image)

        print("Raster recortado salvo -> {}".format(output_path))
        return out_image, out_meta
    @staticmethod
    def polygonize_raster(input_raster, output_shapefile_path, file_name):
        with rasterio.Env():
            with rasterio.open(input_raster) as src:
                print("Checando dtype do Raster...")
                if src.dtypes[0] not in ['uint8', 'int16', 'int32', 'uint16', 'float32']:
                    image = src.read(1)# Convertendo raster p/ uint8
                    image = (image / image.max() * 255).astype('uint8')
                else:
                    image = src.read(1)
                results = (
                    {'properties': {'raster_val': v}, 'geometry': s}
                    for i, (s, v) 
                    in enumerate(
                        shapes(image, mask=None, transform=src.transform)))
                geoms = list(results)
                geoms = gpd.GeoDataFrame.from_features(geoms, crs=src.crs) #criando vetor
                print("Exportando vetor...")
                geoms.to_file(os.path.join(output_shapefile_path, file_name + '.geojson'), 
                            driver='GeoJSON', encoding='utf-8')
                print("Vetor exportado!")
        return geoms

class reclassificando_vetores:
    @staticmethod
    def reclassificando_classes_uso_solo_mapbiomas(df):
        """ 
        Objetivo: Função para reclassificar as classes de uso do solo fora da influencia do PRODES a partir do campo
        'DN'
        
        """
        #Onde a coluna DN for igual a 0, adicionar uma nova coluna chamada 'classe_uso_solo' e atribuir o valor 'NO_DATA'
        df.loc[df['raster_val'] == 3, 'classe_uso_solo_mapbiomas'] = 'VEGETACAO_NATIVA'
        df.loc[df['raster_val'] == 4, 'classe_uso_solo_mapbiomas'] = 'VEGETACAO_NATIVA'
        df.loc[df['raster_val'] == 15, 'classe_uso_solo_mapbiomas'] = 'PASTAGEM'

        df.loc[df['raster_val'] == 0, 'classe_uso_solo_mapbiomas'] = 'OUTROS'
        df.loc[df['raster_val'] == 39, 'classe_uso_solo_mapbiomas'] = 'OUTROS'
        df.loc[df['raster_val'] == 41, 'classe_uso_solo_mapbiomas'] = 'OUTROS'
        df.loc[df['raster_val'] == 12, 'classe_uso_solo_mapbiomas'] = 'OUTROS'
        df.loc[df['raster_val'] == 11, 'classe_uso_solo_mapbiomas'] = 'OUTROS'
        df.loc[df['raster_val'] == 33, 'classe_uso_solo_mapbiomas'] = 'OUTROS'

        return df