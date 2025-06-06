import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patheffects as path_effects # Import this
import matplotlib.patches as mpatches

def create_professional_visualization():
    # ... (your existing code for loading data, setting up fig, ax) ...
    # Load your existing data
    intersection_gdf = gpd.read_file("data/processed/hamilton_escarpment_boundary.shp")
    hamilton_gdf = gpd.read_file("data/raw/City_Boundary/City_Boundary.shp") # Ensure paths are correct

    # Ensure same CRS
    if hamilton_gdf.crs != intersection_gdf.crs:
        hamilton_gdf = hamilton_gdf.to_crs(intersection_gdf.crs)

    # Set up figure with Apple-style proportions
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#0f1419')

    # --- MODIFIED BACKGROUND APPROACH (Example using axhspan and imshow for sky) ---
    y_min_total, y_max_total = hamilton_gdf.total_bounds[1], hamilton_gdf.total_bounds[3]
    x_min_total, x_max_total = hamilton_gdf.total_bounds[0], hamilton_gdf.total_bounds[2]
    
    # Extend bounds slightly for visuals to bleed off if desired
    plot_x_min, plot_x_max = x_min_total - 2000, x_max_total + 2000
    plot_y_min, plot_y_max = y_min_total - 2000, y_max_total + 2000

    horizon_y_ratio = 0.45 # Horizon at 45% from bottom
    horizon_y_coord = plot_y_min + (plot_y_max - plot_y_min) * horizon_y_ratio
    
    # Darker bottom part
    ax.axhspan(plot_y_min, horizon_y_coord, facecolor='#0A182A', zorder=0, alpha=0.9) # Slightly different dark blue

    # Lighter gradient for the sky part
    sky_gradient_array = np.linspace(0.0, 1.0, 256).reshape(-1, 1) # Will be mapped by cmap
    sky_cmap = plt.cm.Blues_r # Light at 0.0, Dark at 1.0
    ax.imshow(sky_gradient_array, cmap=sky_cmap, aspect='auto', alpha=0.6,
              extent=[plot_x_min, plot_x_max, horizon_y_coord, plot_y_max], zorder=1)
    # --- END MODIFIED BACKGROUND ---

    # Plot faded Hamilton boundary
    hamilton_gdf.plot(ax=ax, facecolor='none', edgecolor='white',
                     linewidth=0.8, alpha=0.2, zorder=2) # Reduced alpha

    # Plot escarpment boundary with yellow highlight
    intersection_gdf.plot(ax=ax, facecolor='none', edgecolor='#FFD700', # Gold is good
                         linewidth=2.5, alpha=1.0, zorder=4) # Increased alpha, ensure on top of Hamilton boundary

    # Pick realistic viewpoint (southern edge of escarpment)
    bounds = intersection_gdf.bounds.iloc[0]
    viewpoint_x = (bounds['minx'] + bounds['maxx']) / 2
    viewpoint_y = bounds['miny'] + (bounds['maxy'] - bounds['miny']) * 0.3

    # Add viewpoint with impact
    viewpoint_radius = 900 # Slightly increased radius
    viewpoint_color = '#2ECC71' # A slightly softer green, or stick to #00FF7F
    viewpoint = Circle((viewpoint_x, viewpoint_y), radius=viewpoint_radius,
                      facecolor=viewpoint_color, edgecolor='white', # White edge for crispness
                      linewidth=1.5, alpha=1.0, zorder=10) # Ensure high zorder
    
    # Apply PathEffects to viewpoint for a glow
    viewpoint.set_path_effects([
        path_effects.Stroke(linewidth=viewpoint_radius*0.01 + 4, foreground='white', alpha=0.3), # Outer glow
        path_effects.Stroke(linewidth=viewpoint_radius*0.01 + 2, foreground=viewpoint_color, alpha=0.6), # Inner color reinforcement
        path_effects.Normal()
    ])
    ax.add_patch(viewpoint)

    # Calculate sight line direction (toward Toronto/CN Tower)
    cn_tower_approx_x = viewpoint_x + 25000 # Adjusted for potential new xlim/ylim
    cn_tower_approx_y = viewpoint_y + 12000

    # Add dashed sight line
    ax.plot([viewpoint_x, cn_tower_approx_x], [viewpoint_y, cn_tower_approx_y],
            color='white', linewidth=2.0, linestyle='--', alpha=0.7, zorder=5) # Reduced alpha slightly

    # Professional typography
    plt.rcParams['font.family'] = 'Arial' # Or another preferred sans-serif font

    # Add title and subtitle
    title_fx = [path_effects.Stroke(linewidth=1.5, foreground=ax.get_facecolor(), alpha=0.8), path_effects.Normal()]
    ax.text(0.5, 0.95, 'Hamilton Viewspot Finder',
            transform=ax.transAxes, fontsize=28, fontweight='bold',
            color='white', ha='center', va='top', path_effects=title_fx, zorder=11)

    ax.text(0.5, 0.90, 'Advanced Viewshed Analysis for Recreational Planning',
            transform=ax.transAxes, fontsize=16,
            color='#B0C4DE', ha='center', va='top', path_effects=title_fx, zorder=11) # Light Steel Blue

    ax.text(0.5, 0.06, 'Personal Portfolio Project • Interactive Spatial Analysis MVP',
            transform=ax.transAxes, fontsize=12,
            color='#87CEEB', ha='center', va='bottom', style='italic', path_effects=title_fx, zorder=11) # Sky Blue

    # Clean styling
    ax.set_xlim(plot_x_min, plot_x_max)
    ax.set_ylim(plot_y_min, plot_y_max)
    ax.set_aspect('equal')
    ax.axis('off')

    # Tight layout for clean presentation
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.08) # Adjust if text gets cut

    return fig, ax

# Test it
if __name__ == "__main__":
    # Make sure your shapefiles are in these relative paths or provide absolute paths
    # For example:
    # intersection_gdf = gpd.read_file("path/to/your/data/processed/hamilton_escarpment_boundary.shp")
    # hamilton_gdf = gpd.read_file("path/to/your/data/raw/City_Boundary/City_Boundary.shp")
    try:
        fig, ax = create_professional_visualization()
        plt.savefig("improved_visualization.png", dpi=300, bbox_inches='tight') # Save for review
        plt.show()
    except FileNotFoundError as e:
        print(f"Error: Shapefile not found. Please check paths. Details: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")