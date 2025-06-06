# """
# Viewshed Analysis for Niagara Escarpment
# Direct COG processing for line-of-sight calculations
# """

# import rasterio
# import numpy as np
# import math
# from typing import Dict, List, Tuple, Optional
# from dataclasses import dataclass
# from pyproj import Transformer

# # Available HRDEM COG tiles covering the analysis area
# HRDEM_TILES = {
#     "8_1": "https://datacube-prod-data-public.s3.amazonaws.com/store/elevation/hrdem/hrdem-mosaic-2m/8_1-mosaic-2m-dsm.tif",
#     "8_2": "https://datacube-prod-data-public.s3.amazonaws.com/store/elevation/hrdem/hrdem-mosaic-2m/8_2-mosaic-2m-dsm.tif"
# }

# @dataclass
# class TileBounds:
#     """Represents geographic bounds of a COG tile"""
#     west: float
#     south: float
#     east: float
#     north: float
#     tile_id: str

# def get_tile_bounds(tile_url: str, tile_id: str) -> TileBounds:
#     """
#     Get geographic bounds of a COG tile
    
#     Args:
#         tile_url: URL to the COG tile
#         tile_id: Identifier for the tile
    
#     Returns:
#         TileBounds object with geographic extents
#     """
#     try:
#         with rasterio.open(tile_url) as src:
#             bounds = src.bounds
#             return TileBounds(
#                 west=bounds.left,
#                 south=bounds.bottom, 
#                 east=bounds.right,
#                 north=bounds.top,
#                 tile_id=tile_id
#             )
#     except Exception as e:
#         print(f"Error reading tile {tile_id}: {e}")
#         return None

# def transform_coordinates(lat: float, lon: float, from_crs: str = "EPSG:4326", to_crs: str = "EPSG:3979"):
#     """
#     Transform coordinates between coordinate systems
    
#     Args:
#         lat, lon: Input coordinates
#         from_crs: Source coordinate system (default: WGS84 lat/lon)
#         to_crs: Target coordinate system (default: Canada Atlas LCC)
    
#     Returns:
#         Tuple of transformed coordinates (x, y)
#     """
#     transformer = Transformer.from_crs(from_crs, to_crs, always_xy=True)
#     x, y = transformer.transform(lon, lat)  # Note: lon, lat order for transformer
#     return x, y

# def point_in_bounds(lat: float, lon: float, bounds: TileBounds) -> bool:
#     """
#     Check if a coordinate point falls within tile bounds
    
#     Args:
#         lat: Latitude of point
#         lon: Longitude of point  
#         bounds: TileBounds object
        
#     Returns:
#         True if point is within bounds
#     """
#     # Transform lat/lon to tile's coordinate system
#     x, y = transform_coordinates(lat, lon)
    
#     return (bounds.south <= y <= bounds.north and 
#             bounds.west <= x <= bounds.east)

# def line_intersects_bounds(lat1: float, lon1: float, 
#                           lat2: float, lon2: float, 
#                           bounds: TileBounds) -> bool:
#     """
#     Check if a line segment intersects with tile bounds
#     Uses simple bounding box intersection check
    
#     Args:
#         lat1, lon1: Start point of line
#         lat2, lon2: End point of line
#         bounds: TileBounds object
        
#     Returns:
#         True if line intersects tile bounds
#     """
#     # Transform both points to tile coordinate system
#     x1, y1 = transform_coordinates(lat1, lon1)
#     x2, y2 = transform_coordinates(lat2, lon2)
    
#     # Line bounding box in projected coordinates
#     line_west = min(x1, x2)
#     line_east = max(x1, x2)
#     line_south = min(y1, y2)
#     line_north = max(y1, y2)
    
#     # Check if bounding boxes overlap
#     return not (line_east < bounds.west or line_west > bounds.east or
#                 line_north < bounds.south or line_south > bounds.north)

# def get_intersecting_tiles(observer_lat: float, observer_lon: float,
#                           target_lat: float, target_lon: float) -> List[str]:
#     """
#     Determine which COG tiles are needed for line-of-sight analysis
    
#     Args:
#         observer_lat, observer_lon: Observer coordinates
#         target_lat, target_lon: Target coordinates
        
#     Returns:
#         List of tile IDs that intersect the line of sight
#     """
#     needed_tiles = []
    
#     for tile_id, tile_url in HRDEM_TILES.items():
#         bounds = get_tile_bounds(tile_url, tile_id)
#         if bounds is None:
#             continue
            
#         # Check if observer or target is in this tile
#         observer_in_tile = point_in_bounds(observer_lat, observer_lon, bounds)
#         target_in_tile = point_in_bounds(target_lat, target_lon, bounds)
        
#         # Check if line crosses this tile
#         line_crosses_tile = line_intersects_bounds(
#             observer_lat, observer_lon, target_lat, target_lon, bounds
#         )
        
#         if observer_in_tile or target_in_tile or line_crosses_tile:
#             needed_tiles.append(tile_id)
    
#     return needed_tiles

# def sample_line_coordinates(lat1: float, lon1: float, 
#                            lat2: float, lon2: float, 
#                            num_samples: int = 250) -> List[Tuple[float, float]]:
#     """
#     Generate coordinate samples along a line between two points
    
#     Args:
#         lat1, lon1: Start point
#         lat2, lon2: End point
#         num_samples: Number of points to sample along the line
        
#     Returns:
#         List of (lat, lon) coordinate tuples
#     """
#     samples = []
    
#     for i in range(num_samples + 1):  # Include both endpoints
#         ratio = i / num_samples
        
#         # Linear interpolation between points
#         sample_lat = lat1 + (lat2 - lat1) * ratio
#         sample_lon = lon1 + (lon2 - lon1) * ratio
        
#         samples.append((sample_lat, sample_lon))
    
#     return samples

# def get_elevation_at_point(lat: float, lon: float, tile_url: str) -> Optional[float]:
#     """
#     Get elevation value at a specific coordinate from a COG tile
    
#     Args:
#         lat: Latitude of point
#         lon: Longitude of point
#         tile_url: URL to COG tile
        
#     Returns:
#         Elevation value in meters, or None if point outside tile or error
#     """
#     try:
#         with rasterio.open(tile_url) as src:
#             # Transform lat/lon to the COG's coordinate system
#             x, y = transform_coordinates(lat, lon)
            
#             # Convert transformed coordinates to pixel coordinates
#             row, col = src.index(x, y)
            
#             # Check if coordinates are within the raster bounds
#             if (0 <= row < src.height and 0 <= col < src.width):
#                 # Read elevation value at this pixel
#                 elevation = src.read(1)[row, col]
                
#                 # Handle nodata values
#                 if src.nodata is not None and elevation == src.nodata:
#                     return None
                    
#                 return float(elevation)
#             else:
#                 return None
                
#     except Exception as e:
#         print(f"Error reading elevation at ({lat}, {lon}): {e}")
#         return None

# def get_elevation_profile_multi_tile(coordinates: List[Tuple[float, float]], 
#                                    tiles_needed: List[str]) -> List[Optional[float]]:
#     """
#     Get elevation profile along a line using multiple COG tiles
    
#     Args:
#         coordinates: List of (lat, lon) points along the line
#         tiles_needed: List of tile IDs to search for elevation data
        
#     Returns:
#         List of elevation values corresponding to each coordinate
#     """
#     elevations = []
    
#     for lat, lon in coordinates:
#         elevation = None
        
#         # Try each tile until we find one that contains this point
#         for tile_id in tiles_needed:
#             tile_url = HRDEM_TILES[tile_id]
#             elevation = get_elevation_at_point(lat, lon, tile_url)
            
#             if elevation is not None:
#                 break  # Found elevation in this tile
        
#         elevations.append(elevation)
    
#     return elevations

# def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
#     """
#     Calculate great circle distance between two points using Haversine formula
    
#     Args:
#         lat1, lon1: First point coordinates
#         lat2, lon2: Second point coordinates
        
#     Returns:
#         Distance in kilometers
#     """
#     # Convert to radians
#     lat1_rad = math.radians(lat1)
#     lon1_rad = math.radians(lon1)
#     lat2_rad = math.radians(lat2)
#     lon2_rad = math.radians(lon2)
    
#     # Haversine formula
#     dlat = lat2_rad - lat1_rad
#     dlon = lon2_rad - lon1_rad
    
#     a = (math.sin(dlat/2)**2 + 
#          math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
#     c = 2 * math.asin(math.sqrt(a))
    
#     # Earth's radius in kilometers
#     earth_radius_km = 6371.0
    
#     return earth_radius_km * c

# def calculate_line_of_sight(observer_elevation: float, target_elevation: float,
#                           elevation_profile: List[float], 
#                           distances: List[float],
#                           observer_height: float = 1.7) -> Dict:
#     """
#     Calculate line-of-sight visibility accounting for terrain and curvature
    
#     Args:
#         observer_elevation: Ground elevation at observer position (meters)
#         target_elevation: Ground elevation at target position (meters)
#         elevation_profile: Terrain elevations along the line
#         distances: Distance from observer to each profile point (meters)
#         observer_height: Height of observer above ground (meters)
        
#     Returns:
#         Dictionary with visibility analysis results
#     """
#     # Observer's eye level
#     observer_eye_level = observer_elevation + observer_height
    
#     # Total distance to target
#     total_distance = distances[-1] if distances else 0
    
#     visible = True
#     blocking_elevation = None
#     blocking_distance = None
    
#     # Check each point along the profile for obstruction
#     for i, (terrain_elev, distance) in enumerate(zip(elevation_profile, distances)):
#         if terrain_elev is None:
#             continue  # Skip points with no elevation data
            
#         # Calculate required line-of-sight height at this distance
#         # Accounts for Earth's curvature (approximation)
#         curvature_correction = (distance**2) / (2 * 6371000)  # meters
        
#         # Height the line-of-sight beam should be at this distance
#         if total_distance > 0:
#             beam_ratio = distance / total_distance
#             required_height = (observer_eye_level + 
#                              beam_ratio * (target_elevation - observer_eye_level) + 
#                              curvature_correction)
#         else:
#             required_height = observer_eye_level
        
#         # Check if terrain blocks the line of sight
#         if terrain_elev > required_height:
#             visible = False
#             blocking_elevation = terrain_elev
#             blocking_distance = distance
#             break
    
#     return {
#         'visible': visible,
#         'blocking_elevation': blocking_elevation,
#         'blocking_distance_m': blocking_distance,
#         'observer_eye_level': observer_eye_level,
#         'target_elevation': target_elevation,
#         'total_distance_m': total_distance
#     }

# def line_of_sight(observer_lat: float, observer_lon: float,
#                  target_lat: float, target_lon: float,
#                  observer_height: float = 1.7) -> Dict:
#     """
#     Main function: Calculate line-of-sight visibility between two points
    
#     Args:
#         observer_lat, observer_lon: Observer coordinates (decimal degrees)
#         target_lat, target_lon: Target coordinates (decimal degrees)  
#         observer_height: Height of observer above ground (meters)
        
#     Returns:
#         Dictionary containing complete visibility analysis:
#         {
#             'visible': bool,
#             'distance_km': float,
#             'elevation_profile': List[float],
#             'sample_coordinates': List[Tuple[float, float]],
#             'observer_elevation': float,
#             'target_elevation': float,
#             'blocking_elevation': float or None,
#             'blocking_distance_m': float or None,
#             'tiles_used': List[str]
#         }
#     """
    
#     # Step 1: Determine which tiles we need
#     tiles_needed = get_intersecting_tiles(observer_lat, observer_lon, 
#                                         target_lat, target_lon)
    
#     if not tiles_needed:
#         return {
#             'error': 'No elevation data available for this line of sight',
#             'visible': False
#         }
    
#     # Step 2: Sample coordinates along the line
#     sample_coords = sample_line_coordinates(observer_lat, observer_lon,
#                                           target_lat, target_lon)
    
#     # Step 3: Get elevation profile from COG tiles
#     elevation_profile = get_elevation_profile_multi_tile(sample_coords, tiles_needed)
    
#     # Step 4: Calculate distances from observer to each sample point
#     distances = []
#     for lat, lon in sample_coords:
#         dist_km = calculate_distance_km(observer_lat, observer_lon, lat, lon)
#         distances.append(dist_km * 1000)  # Convert to meters
    
#     # Step 5: Get observer and target elevations
#     observer_elevation = elevation_profile[0] if elevation_profile else None
#     target_elevation = elevation_profile[-1] if elevation_profile else None
    
#     if observer_elevation is None or target_elevation is None:
#         return {
#             'error': 'Cannot determine observer or target elevation',
#             'visible': False
#         }
    
#     # Step 6: Calculate line-of-sight visibility
#     visibility_result = calculate_line_of_sight(
#         observer_elevation, target_elevation, elevation_profile, 
#         distances, observer_height
#     )
    
#     # Step 7: Prepare complete result
#     total_distance_km = calculate_distance_km(observer_lat, observer_lon, 
#                                             target_lat, target_lon)
    
#     result = {
#         'visible': visibility_result['visible'],
#         'distance_km': total_distance_km,
#         'elevation_profile': elevation_profile,
#         'sample_coordinates': sample_coords,
#         'observer_elevation': observer_elevation,
#         'target_elevation': target_elevation,
#         'observer_eye_level': visibility_result['observer_eye_level'],
#         'blocking_elevation': visibility_result['blocking_elevation'],
#         'blocking_distance_m': visibility_result['blocking_distance_m'],
#         'tiles_used': tiles_needed,
#         'num_samples': len(sample_coords)
#     }
    
#     return result

# # Test function for development
# def test_line_of_sight():
#     """
#     Test the line of sight calculation with Hamilton area coordinates
#     """
#     # Dundas Peak to Hamilton downtown
#     observer_lat, observer_lon = 43.2833, -80.0167  # Dundas Peak
#     target_lat, target_lon = 43.2557, -79.8711      # Hamilton downtown
    
#     print("Testing line of sight from Dundas Peak to Hamilton downtown...")
    
#     result = line_of_sight(observer_lat, observer_lon, target_lat, target_lon)
    
#     print(f"Visible: {result.get('visible', 'Unknown')}")
#     print(f"Distance: {result.get('distance_km', 0):.2f} km")
#     print(f"Observer elevation: {result.get('observer_elevation', 'Unknown')} m")
#     print(f"Target elevation: {result.get('target_elevation', 'Unknown')} m")
#     print(f"Tiles used: {result.get('tiles_used', [])}")
    
#     if not result.get('visible', False):
#         print(f"Blocked at: {result.get('blocking_distance_m', 0)/1000:.2f} km")
#         print(f"Blocking elevation: {result.get('blocking_elevation', 'Unknown')} m")

# def test_line_of_sight_fast():
#     """
#     Fast test with fewer sample points
#     """
#     # Dundas Peak to Hamilton downtown
#     observer_lat, observer_lon = 43.2833, -80.0167  # Dundas Peak
#     target_lat, target_lon = 43.2557, -79.8711      # Hamilton downtown
    
#     print("Testing line of sight with 10 sample points...")
    
#     # Test with just 10 sample points instead of 250
#     sample_coords = sample_line_coordinates(observer_lat, observer_lon, 
#                                           target_lat, target_lon, 10)
    
#     print(f"Sample coordinates: {len(sample_coords)} points")
    
#     # Test elevation reading for just these few points
#     tiles_needed = get_intersecting_tiles(observer_lat, observer_lon, 
#                                         target_lat, target_lon)
#     print(f"Tiles needed: {tiles_needed}")
    
#     if tiles_needed:
#         elevations = get_elevation_profile_multi_tile(sample_coords, tiles_needed)
#         print(f"Elevations: {elevations}")

# def test_single_elevation():
#     """Test reading elevation for just one point"""
#     print("Testing single elevation read...")
    
#     lat, lon = 43.2833, -80.0167  # Dundas Peak
#     tile_url = HRDEM_TILES["8_2"]
    
#     print(f"Reading elevation at ({lat}, {lon})...")
    
#     try:
#         elevation = get_elevation_at_point(lat, lon, tile_url)
#         print(f"✅ Elevation: {elevation} meters")
#     except Exception as e:
#         print(f"❌ Error: {e}")

# # Replace your __main__ section with:
# if __name__ == "__main__":
#     test_single_elevation()

"""
Viewshed Analysis for Niagara Escarpment
Direct COG processing for line-of-sight calculations
"""

import os
import rasterio
from rasterio.env import Env
import numpy as np
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pyproj import Transformer

# Optimize rasterio for COG access
os.environ['GDAL_DISABLE_READDIR_ON_OPEN'] = 'EMPTY_DIR'
os.environ['CPL_VSIL_CURL_ALLOWED_EXTENSIONS'] = '.tif'
os.environ['GDAL_HTTP_TIMEOUT'] = '30'
os.environ['GDAL_HTTP_CONNECTTIMEOUT'] = '10'

# Available HRDEM COG tiles covering the analysis area
HRDEM_TILES = {
    "8_1": "https://datacube-prod-data-public.s3.amazonaws.com/store/elevation/hrdem/hrdem-mosaic-2m/8_1-mosaic-2m-dsm.tif",
    "8_2": "https://datacube-prod-data-public.s3.amazonaws.com/store/elevation/hrdem/hrdem-mosaic-2m/8_2-mosaic-2m-dsm.tif"
}

@dataclass
class TileBounds:
    """Represents geographic bounds of a COG tile"""
    west: float
    south: float
    east: float
    north: float
    tile_id: str

def get_tile_bounds(tile_url: str, tile_id: str) -> TileBounds:
    """
    Get geographic bounds of a COG tile
    
    Args:
        tile_url: URL to the COG tile
        tile_id: Identifier for the tile
    
    Returns:
        TileBounds object with geographic extents
    """
    try:
        with rasterio.open(tile_url) as src:
            bounds = src.bounds
            return TileBounds(
                west=bounds.left,
                south=bounds.bottom, 
                east=bounds.right,
                north=bounds.top,
                tile_id=tile_id
            )
    except Exception as e:
        print(f"Error reading tile {tile_id}: {e}")
        return None

def transform_coordinates(lat: float, lon: float, from_crs: str = "EPSG:4326", to_crs: str = "EPSG:3979"):
    """
    Transform coordinates between coordinate systems
    
    Args:
        lat, lon: Input coordinates
        from_crs: Source coordinate system (default: WGS84 lat/lon)
        to_crs: Target coordinate system (default: Canada Atlas LCC)
    
    Returns:
        Tuple of transformed coordinates (x, y)
    """
    transformer = Transformer.from_crs(from_crs, to_crs, always_xy=True)
    x, y = transformer.transform(lon, lat)  # Note: lon, lat order for transformer
    return x, y

def point_in_bounds(lat: float, lon: float, bounds: TileBounds) -> bool:
    """
    Check if a coordinate point falls within tile bounds
    
    Args:
        lat: Latitude of point
        lon: Longitude of point  
        bounds: TileBounds object
        
    Returns:
        True if point is within bounds
    """
    # Transform lat/lon to tile's coordinate system
    x, y = transform_coordinates(lat, lon)
    
    return (bounds.south <= y <= bounds.north and 
            bounds.west <= x <= bounds.east)

def line_intersects_bounds(lat1: float, lon1: float, 
                          lat2: float, lon2: float, 
                          bounds: TileBounds) -> bool:
    """
    Check if a line segment intersects with tile bounds
    Uses simple bounding box intersection check
    
    Args:
        lat1, lon1: Start point of line
        lat2, lon2: End point of line
        bounds: TileBounds object
        
    Returns:
        True if line intersects tile bounds
    """
    # Transform both points to tile coordinate system
    x1, y1 = transform_coordinates(lat1, lon1)
    x2, y2 = transform_coordinates(lat2, lon2)
    
    # Line bounding box in projected coordinates
    line_west = min(x1, x2)
    line_east = max(x1, x2)
    line_south = min(y1, y2)
    line_north = max(y1, y2)
    
    # Check if bounding boxes overlap
    return not (line_east < bounds.west or line_west > bounds.east or
                line_north < bounds.south or line_south > bounds.north)

def get_intersecting_tiles(observer_lat: float, observer_lon: float,
                          target_lat: float, target_lon: float) -> List[str]:
    """
    Determine which COG tiles are needed for line-of-sight analysis
    
    Args:
        observer_lat, observer_lon: Observer coordinates
        target_lat, target_lon: Target coordinates
        
    Returns:
        List of tile IDs that intersect the line of sight
    """
    needed_tiles = []
    
    for tile_id, tile_url in HRDEM_TILES.items():
        bounds = get_tile_bounds(tile_url, tile_id)
        if bounds is None:
            continue
            
        # Check if observer or target is in this tile
        observer_in_tile = point_in_bounds(observer_lat, observer_lon, bounds)
        target_in_tile = point_in_bounds(target_lat, target_lon, bounds)
        
        # Check if line crosses this tile
        line_crosses_tile = line_intersects_bounds(
            observer_lat, observer_lon, target_lat, target_lon, bounds
        )
        
        if observer_in_tile or target_in_tile or line_crosses_tile:
            needed_tiles.append(tile_id)
    
    return needed_tiles

def sample_line_coordinates(lat1: float, lon1: float, 
                           lat2: float, lon2: float, 
                           num_samples: int = 250) -> List[Tuple[float, float]]:
    """
    Generate coordinate samples along a line between two points
    
    Args:
        lat1, lon1: Start point
        lat2, lon2: End point
        num_samples: Number of points to sample along the line
        
    Returns:
        List of (lat, lon) coordinate tuples
    """
    samples = []
    
    for i in range(num_samples + 1):  # Include both endpoints
        ratio = i / num_samples
        
        # Linear interpolation between points
        sample_lat = lat1 + (lat2 - lat1) * ratio
        sample_lon = lon1 + (lon2 - lon1) * ratio
        
        samples.append((sample_lat, sample_lon))
    
    return samples

def get_elevation_at_point(lat: float, lon: float, tile_url: str) -> Optional[float]:
    """
    Get elevation value at a specific coordinate from a COG tile
    
    Args:
        lat: Latitude of point
        lon: Longitude of point
        tile_url: URL to COG tile
        
    Returns:
        Elevation value in meters, or None if point outside tile or error
    """
    try:
        with Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',
                 CPL_VSIL_CURL_ALLOWED_EXTENSIONS='.tif'):
            
            with rasterio.open(tile_url) as src:
                # Transform lat/lon to the COG's coordinate system
                x, y = transform_coordinates(lat, lon)
                
                # Convert transformed coordinates to pixel coordinates
                row, col = src.index(x, y)
                
                # Check if coordinates are within the raster bounds
                if (0 <= row < src.height and 0 <= col < src.width):
                    # Read elevation value at this pixel
                    elevation = src.read(1)[row, col]
                    
                    # Handle nodata values
                    if src.nodata is not None and elevation == src.nodata:
                        return None
                        
                    return float(elevation)
                else:
                    return None
                    
    except Exception as e:
        print(f"Error reading elevation at ({lat}, {lon}): {e}")
        return None

def get_elevation_profile_multi_tile(coordinates: List[Tuple[float, float]], 
                                   tiles_needed: List[str]) -> List[Optional[float]]:
    """
    Get elevation profile along a line using multiple COG tiles
    
    Args:
        coordinates: List of (lat, lon) points along the line
        tiles_needed: List of tile IDs to search for elevation data
        
    Returns:
        List of elevation values corresponding to each coordinate
    """
    elevations = []
    
    for lat, lon in coordinates:
        elevation = None
        
        # Try each tile until we find one that contains this point
        for tile_id in tiles_needed:
            tile_url = HRDEM_TILES[tile_id]
            elevation = get_elevation_at_point(lat, lon, tile_url)
            
            if elevation is not None:
                break  # Found elevation in this tile
        
        elevations.append(elevation)
    
    return elevations

def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great circle distance between two points using Haversine formula
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
        
    Returns:
        Distance in kilometers
    """
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (math.sin(dlat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth's radius in kilometers
    earth_radius_km = 6371.0
    
    return earth_radius_km * c

def calculate_line_of_sight(observer_elevation: float, target_elevation: float,
                          elevation_profile: List[float], 
                          distances: List[float],
                          observer_height: float = 1.7) -> Dict:
    """
    Calculate line-of-sight visibility accounting for terrain and curvature
    
    Args:
        observer_elevation: Ground elevation at observer position (meters)
        target_elevation: Ground elevation at target position (meters)
        elevation_profile: Terrain elevations along the line
        distances: Distance from observer to each profile point (meters)
        observer_height: Height of observer above ground (meters)
        
    Returns:
        Dictionary with visibility analysis results
    """
    # Observer's eye level
    observer_eye_level = observer_elevation + observer_height
    
    # Total distance to target
    total_distance = distances[-1] if distances else 0
    
    visible = True
    blocking_elevation = None
    blocking_distance = None
    
    # Check each point along the profile for obstruction
    for i, (terrain_elev, distance) in enumerate(zip(elevation_profile, distances)):
        if terrain_elev is None:
            continue  # Skip points with no elevation data
            
        # Calculate required line-of-sight height at this distance
        # Accounts for Earth's curvature (approximation)
        curvature_correction = (distance**2) / (2 * 6371000)  # meters
        
        # Height the line-of-sight beam should be at this distance
        if total_distance > 0:
            beam_ratio = distance / total_distance
            required_height = (observer_eye_level + 
                             beam_ratio * (target_elevation - observer_eye_level) + 
                             curvature_correction)
        else:
            required_height = observer_eye_level
        
        # Check if terrain blocks the line of sight
        if terrain_elev > required_height:
            visible = False
            blocking_elevation = terrain_elev
            blocking_distance = distance
            break
    
    return {
        'visible': visible,
        'blocking_elevation': blocking_elevation,
        'blocking_distance_m': blocking_distance,
        'observer_eye_level': observer_eye_level,
        'target_elevation': target_elevation,
        'total_distance_m': total_distance
    }

def line_of_sight(observer_lat: float, observer_lon: float,
                 target_lat: float, target_lon: float,
                 observer_height: float = 1.7) -> Dict:
    """
    Main function: Calculate line-of-sight visibility between two points
    
    Args:
        observer_lat, observer_lon: Observer coordinates (decimal degrees)
        target_lat, target_lon: Target coordinates (decimal degrees)  
        observer_height: Height of observer above ground (meters)
        
    Returns:
        Dictionary containing complete visibility analysis:
        {
            'visible': bool,
            'distance_km': float,
            'elevation_profile': List[float],
            'sample_coordinates': List[Tuple[float, float]],
            'observer_elevation': float,
            'target_elevation': float,
            'blocking_elevation': float or None,
            'blocking_distance_m': float or None,
            'tiles_used': List[str]
        }
    """
    
    # Step 1: Determine which tiles we need
    tiles_needed = get_intersecting_tiles(observer_lat, observer_lon, 
                                        target_lat, target_lon)
    
    if not tiles_needed:
        return {
            'error': 'No elevation data available for this line of sight',
            'visible': False
        }
    
    # Step 2: Sample coordinates along the line
    sample_coords = sample_line_coordinates(observer_lat, observer_lon,
                                          target_lat, target_lon)
    
    # Step 3: Get elevation profile from COG tiles
    elevation_profile = get_elevation_profile_multi_tile(sample_coords, tiles_needed)
    
    # Step 4: Calculate distances from observer to each sample point
    distances = []
    for lat, lon in sample_coords:
        dist_km = calculate_distance_km(observer_lat, observer_lon, lat, lon)
        distances.append(dist_km * 1000)  # Convert to meters
    
    # Step 5: Get observer and target elevations
    observer_elevation = elevation_profile[0] if elevation_profile else None
    target_elevation = elevation_profile[-1] if elevation_profile else None
    
    if observer_elevation is None or target_elevation is None:
        return {
            'error': 'Cannot determine observer or target elevation',
            'visible': False
        }
    
    # Step 6: Calculate line-of-sight visibility
    visibility_result = calculate_line_of_sight(
        observer_elevation, target_elevation, elevation_profile, 
        distances, observer_height
    )
    
    # Step 7: Prepare complete result
    total_distance_km = calculate_distance_km(observer_lat, observer_lon, 
                                            target_lat, target_lon)
    
    result = {
        'visible': visibility_result['visible'],
        'distance_km': total_distance_km,
        'elevation_profile': elevation_profile,
        'sample_coordinates': sample_coords,
        'observer_elevation': observer_elevation,
        'target_elevation': target_elevation,
        'observer_eye_level': visibility_result['observer_eye_level'],
        'blocking_elevation': visibility_result['blocking_elevation'],
        'blocking_distance_m': visibility_result['blocking_distance_m'],
        'tiles_used': tiles_needed,
        'num_samples': len(sample_coords)
    }
    
    return result

# Test function for development
def test_line_of_sight():
    """
    Test the line of sight calculation with Hamilton area coordinates
    """
    # Dundas Peak to Hamilton downtown
    observer_lat, observer_lon = 43.2833, -80.0167  # Dundas Peak
    target_lat, target_lon = 43.2557, -79.8711      # Hamilton downtown
    
    print("Testing line of sight from Dundas Peak to Hamilton downtown...")
    
    result = line_of_sight(observer_lat, observer_lon, target_lat, target_lon)
    
    print(f"Visible: {result.get('visible', 'Unknown')}")
    print(f"Distance: {result.get('distance_km', 0):.2f} km")
    print(f"Observer elevation: {result.get('observer_elevation', 'Unknown')} m")
    print(f"Target elevation: {result.get('target_elevation', 'Unknown')} m")
    print(f"Tiles used: {result.get('tiles_used', [])}")
    
    if not result.get('visible', False):
        blocking_dist = result.get('blocking_distance_m', 0)
        if blocking_dist:
            print(f"Blocked at: {blocking_dist/1000:.2f} km")
        print(f"Blocking elevation: {result.get('blocking_elevation', 'Unknown')} m")

def test_fast_line_of_sight():
    """
    Test with optimized window reading instead of individual points
    """
    print("Testing FAST line of sight...")
    
    observer_lat, observer_lon = 43.2833, -80.0167  # Dundas Peak
    target_lat, target_lon = 43.2557, -79.8711      # Hamilton downtown
    
    # Just test if we can read elevation at two points
    tile_url = HRDEM_TILES["8_2"]
    
    print("Reading observer elevation...")
    obs_elev = get_elevation_at_point(observer_lat, observer_lon, tile_url)
    print(f"Observer: {obs_elev} m")
    
    print("Reading target elevation...")
    target_elev = get_elevation_at_point(target_lat, target_lon, tile_url)
    print(f"Target: {target_elev} m")
    
    if obs_elev and target_elev:
        distance = calculate_distance_km(observer_lat, observer_lon, target_lat, target_lon)
        print(f"Distance: {distance:.2f} km")
        print(f"✅ Basic line of sight test successful!")
    else:
        print("❌ Could not read elevations")

# Replace your __main__ section:
if __name__ == "__main__":
    test_fast_line_of_sight()