import rasterio
from rasterio.mask import mask
import geopandas as gpd
from rasterio.features import shapes
import pandas as pd
import os
import fnmatch as fn
import zipfile
import re
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
                    if file_ext == '.geojson':
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
                    elif file_type =='geojson':
                        return process_vsizip(zip_path, '.geojson')
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
            elif file_type == 'geojson':
                list_files = [x for x in os.listdir(vault_files) if x.endswith('.geojson') and fn.fnmatch(x, pattern)]
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
        Objetivo: 
            Função para reclassificar as classes de uso do solo fora da influencia do PRODES a partir do campo "raster_val"

        Parâmetros:
            Geodataframe gerado a partir do Mapbiomas

        Versão mapbiomas:
            Coleção 09 - classificação de uso do solo no Espírito Santo
        """
        #Onde a coluna DN for igual a 0, adicionar uma nova coluna chamada 'classe_uso_solo' e atribuir o valor 'NO_DATA'
        df.loc[df['raster_val'] == 0, 'classe_uso_solo_mapbiomas'] = 'OUTROS'

        df.loc[df['raster_val'] == 3, 'classe_uso_solo_mapbiomas'] = 'Vegetação Nativa'
        #Forest formation
        df.loc[df['raster_val'] == 9, 'classe_uso_solo_mapbiomas'] = 'Formação Florestal'
        #Wetland
        df.loc[df['raster_val'] == 11, 'classe_uso_solo_mapbiomas'] = ' Floresta Alagável'
        #Pasture
        df.loc[df['raster_val'] == 15, 'classe_uso_solo_mapbiomas'] = 'Pastagem'
        #Outros usos
        df.loc[df['raster_val'] == 21, 'classe_uso_solo_mapbiomas'] = 'Outros usos agrícolas'
        #Outros usos
        df.loc[df['raster_val'] == 25, 'classe_uso_solo_mapbiomas'] = 'Outros usos agrícolas'
        #Urban Area
        df.loc[df['raster_val'] == 29, 'classe_uso_solo_mapbiomas'] = 'Afloramento Rochoso'
        #Rocky Outcrop
        df.loc[df['raster_val'] == 33, 'classe_uso_solo_mapbiomas'] = 'Corpo dágua'
        #Lavoura
        df.loc[df['raster_val'] == 41, 'classe_uso_solo_mapbiomas'] = 'Lavouras temporárias'
        #Café
        df.loc[df['raster_val'] == 46, 'classe_uso_solo_mapbiomas'] = 'Café'
        #Outras lavouras perenes
        df.loc[df['raster_val'] == 48, 'classe_uso_solo_mapbiomas'] = 'Lavouras perenes'

        return df
    
    @staticmethod
    def reclass_car(x):
        """
        Reclassifica os códigos de status do CAR em três categorias: "Ativo", "Cancelado" e "Pendente",
        com base nos prefixos dos códigos.

        Parâmetros:
        - x (str): Código CAR a ser reclassificado.

        Retorna:
        - str: String indicando o status do CAR: "Ativo" se o código começar com "AT", 
            "Cancelado" se começar com "CA", e "Pendente" se começar com "PE".
        """
        cl1 = re.compile("AT")
        cl2 = re.compile("CA")
        cl3 = re.compile("PE")
        if cl1.match(x):
            return "Ativo"
        elif cl2.match(x):
            return "Cancelado"
        elif cl3.match(x):
            return "Pendente"

class limpeza_de_dados:
    @staticmethod
    def clean_header(df):
        """
        Limpa e padroniza os nomes das colunas de um DataFrame, convertendo todos os caracteres para minúsculas,
        removendo espaços em branco nas extremidades e substituindo espaços por underscores.

        Parâmetros:
        - df (pd.DataFrame): DataFrame cujas colunas precisam ser padronizadas.

        Retorna:
        - pd.DataFrame: DataFrame com os nomes das colunas padronizados.
        """
        df.columns = [x.lower() for x in df.columns]
        df.columns = [x.strip() for x in df.columns]
        df.columns = [x.replace(' ', '_') for x in df.columns]
        return df
    
class adicionando_dados:
    @staticmethod
    def add_area(df):
        """
        Adiciona uma coluna 'area_hectares' a um GeoDataFrame contendo a área de cada geometria em hectares.
        A função muda temporariamente o sistema de coordenadas para EPSG 5880 (Albers Equal Area) para calcular a área corretamente
        e depois retorna ao sistema original EPSG 4674 (SIRGAS 2000).

        Parâmetros:
        - df (gpd.GeoDataFrame): GeoDataFrame com uma coluna de geometria.

        Retorna:
        - gpd.GeoDataFrame: GeoDataFrame com a coluna 'area_hectares', contendo a área de cada geometria em hectares, arredondada para quatro casas decimais.
        """

        df = df.to_crs(epsg=5880)
        df["area_hectares"] = df['geometry'].area/10000
        df["area_hectares"] = df["area_hectares"].round(4)
        #retornando ao crs original
        df = df.to_crs(epsg=4674)
        return df

