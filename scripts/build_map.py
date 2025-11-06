import sys
from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Usage:
#   python scripts/build_map.py countries.txt places.csv visited-map.png

def main():
    if len(sys.argv) < 4:
        print("Usage: python scripts/build_map.py countries.txt places.csv visited-map.png")
        sys.exit(1)

    countries_path = Path(sys.argv[1])
    places_path = Path(sys.argv[2])
    out_path = Path(sys.argv[3])

    # Read ISO3 codes
    iso3 = [line.strip().upper() for line in countries_path.read_text().splitlines() if line.strip()]


    # Path to shapefile (relative to project root)
    shapefile_path = Path("./data/ne_110m_admin_0_countries.shp")
    if not shapefile_path.exists():
        print("Error: Shapefile './data/ne_110m_admin_0_countries.shp' not found.\n" 
              "Download it from https://www.naturalearthdata.com/downloads/110m-cultural-vectors/ and extract all files into the 'data' folder at the project root.")
        sys.exit(1)
    world = gpd.read_file(str(shapefile_path))

    # Match by ISO_A3 (column is uppercase in the shapefile)
    if "ISO_A3" not in world.columns:
        print("Error: 'ISO_A3' column not found in the shapefile. Available columns are:")
        print(list(world.columns))
        sys.exit(1)
    visited = world[world["ISO_A3"].isin(iso3)]

    # Read places
    places = pd.read_csv(places_path)
    gdf_points = gpd.GeoDataFrame(
        places,
        geometry=gpd.points_from_xy(places["lon"], places["lat"]),
        crs="EPSG:4326"
    )

    # Plot
    fig, ax = plt.subplots(figsize=(14, 7), dpi=200)
    world.plot(ax=ax, color="#f2f2f2", edgecolor="#c9c9c9", linewidth=0.4, alpha=0.5)
    visited.plot(ax=ax, color="#b3d8ff", edgecolor="#7cb5ec", linewidth=0.6, alpha=0.7)
    gdf_points.plot(ax=ax, markersize=28, color="#333333", alpha=0.8)

    # Labels
    for _, row in gdf_points.iterrows():
        ax.text(row.geometry.x + 2.0, row.geometry.y + 1.0, row["name"], fontsize=8)

    ax.set_axis_off()
    ax.set_title("Places I've Been", fontsize=14, pad=12)
    plt.tight_layout()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.6)
    ax.set_facecolor('none')


    fig.savefig(out_path, bbox_inches="tight")
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
