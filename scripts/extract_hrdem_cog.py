import rasterio
from rasterio.mask import mask
import geopandas as gpd

def main():
    cog_urls = [
        "https://datacube-prod-data-public.s3.amazonaws.com/store/elevation/hrdem/hrdem-mosaic-2m/8_1-mosaic-2m-dsm.tif",
        "https://datacube-prod-data-public.s3.amazonaws.com/store/elevation/hrdem/hrdem-mosaic-2m/8_2-mosaic-2m-dsm.tif"
    ]

    hamilton_boundary_path = "data/raw/City_Boundary/City_Boundary.shp"
    buffer_distance = 0.05
    output_dir = "data/processed"

    hamilton_gdf = gpd.read_file(hamilton_boundary_path)
    buffered_boundary = hamilton_gdf.buffer(buffer_distance)

    for i, cog_url in enumerate(cog_urls):
        quick_cog_test(cog_url)
        

def quick_cog_test(cog_url):
    with rasterio.open(cog_url) as src:
        print(f"✅ {cog_url.split('/')[-1]} - accessible")
        return True


if __name__ == "__main__":
    main()