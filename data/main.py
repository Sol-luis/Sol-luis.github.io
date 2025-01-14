from modules import caixa_de_ferramentas_raster

def main():
    #Paths
    raster_path = '/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data/mapbiomas-brazil-collection-90-es-2023.tif'
    shapefile_path = '/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data/pol_props_ES.geojson' 
    output_path = '/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data/mapbiomas-brazil-collection-90-es-2023_clipped.tif'
    input_raster_recortado = '/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data/mapbiomas-brazil-collection-90-es-2023_clipped.tif'
    output_path_vector = '/home/luisthethormes/01_sol/geo-dev/Sol-luis.github.io/data/'
    vector_file_name = 'es_uso_do_solo_vetor'


    # Processes
    raster = caixa_de_ferramentas_raster.clip_raster_by_shapefile(raster_path, shapefile_path, output_path)
    vetorizado = caixa_de_ferramentas_raster.polygonize_raster(input_raster_recortado, output_path_vector, vector_file_name)




if __name__ == "__main__":
    main()
