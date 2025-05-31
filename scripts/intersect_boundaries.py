import geopandas as gpd
import os

def main():
    hamilton_path = "data/raw/City_Boundary/City_Boundary.shp"
    escarpment_path = "data/raw/Niagara_Escarpment_Plan_Boundary/Niagara_Escarpment_Plan_Boundary.shp"
    output_path = "data/processed/hamilton_escarpment_boundary.shp"

    print("Loading Hamilton boundary...")
    hamilton_gdf = gpd.read_file(hamilton_path)

    print("Loading Niagara Escarpment boundary...")
    escarpment_gdf = gpd.read_file(escarpment_path)

    print(f"Hamilton boundary loaded: {len(hamilton_gdf)} features")
    print(f"Escarpment boundary loaded: {len(escarpment_gdf)} features")

    # Prints and checks what eachother coordinate systems are.
    print(f"Hamilton CRS: {hamilton_gdf.crs}")
    print(f"Escarpment CRS: {escarpment_gdf.crs}")

    if hamilton_gdf.crs != escarpment_gdf.crs:
        print("Warning: Coordinate systems don't match!")
        print("Reprojecting escarpment to match Hamilton...")
        escarpment_gdf = escarpment_gdf.to_crs(hamilton_gdf.crs)
        print("Reprojection complete.")
    else:
        print("Coordinate systems match - ready for intersection.")

    print("Performing intersection...")
    intersection_gdf = gpd.overlay(hamilton_gdf, escarpment_gdf, how='intersection')

    print(f"Intersection complete: {len(intersection_gdf)} features created")
    print(f"Total area: {intersection_gdf.geometry.area.sum():.2f} square units")
    quick_plot(hamilton_gdf, escarpment_gdf, intersection_gdf)

    print(f"Saving intersection to {output_path}...")
    intersection_gdf.to_file(output_path)
    print("Intersection saved successfully!")

    print("\nSummary:")
    print(f"Output file: {output_path}")
    print(f"Features in result: {len(intersection_gdf)}")
    print(f"Coordinate system: {intersection_gdf.crs}")

def quick_plot(hamilton_gdf, escarpment_gdf, intersection_gdf):
    """Quick visualization of the intersection"""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot all layers
    hamilton_gdf.plot(ax=ax, color='lightblue', alpha=0.5, label='Hamilton')
    escarpment_gdf.plot(ax=ax, color='lightgreen', alpha=0.5, label='Escarpment')
    intersection_gdf.plot(ax=ax, color='red', alpha=0.8, label='Intersection')
    
    ax.legend()
    ax.set_title('Boundary Intersection Result')
    plt.show()


if __name__ == '__main__':
    main()

