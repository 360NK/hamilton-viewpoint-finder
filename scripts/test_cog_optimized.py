import os
import rasterio
from rasterio.env import Env

# Optimize for COG access
os.environ['GDAL_DISABLE_READDIR_ON_OPEN'] = 'EMPTY_DIR'
os.environ['CPL_VSIL_CURL_ALLOWED_EXTENSIONS'] = '.tif'
os.environ['GDAL_HTTP_TIMEOUT'] = '30'
os.environ['GDAL_HTTP_CONNECTTIMEOUT'] = '10'

def test_optimized_cog():
    print("Testing COG with optimized settings...")
    
    tile_url = "https://datacube-prod-data-public.s3.amazonaws.com/store/elevation/hrdem/hrdem-mosaic-2m/8_2-mosaic-2m-dsm.tif"
    
    try:
        with Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',
                 CPL_VSIL_CURL_ALLOWED_EXTENSIONS='.tif',
                 GDAL_HTTP_TIMEOUT='30'):
            
            with rasterio.open(tile_url) as src:
                print("✅ COG opened!")
                print(f"Shape: {src.shape}")
                
                # Try reading a small window instead of index
                # Read a 10x10 pixel window from the middle
                window = rasterio.windows.Window(100000, 100000, 10, 10)
                data = src.read(1, window=window)
                print(f"✅ Read sample data: {data[0,0]}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_optimized_cog()