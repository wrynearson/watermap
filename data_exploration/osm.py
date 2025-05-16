import marimo

__generated_with = "0.13.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import lonboard
    from lonboard import Map, viz, PathLayer
    from lonboard.colormap import apply_categorical_cmap
    import pandas as pd
    import geopandas as gpd
    import numpy as np
    import pyogrio
    import re
    return Map, PathLayer, apply_categorical_cmap, gpd, mo, pd, re, viz


@app.cell
def _(gpd):
    # From inspecting pbf files
    layers = ['points', 'lines', 'multilinestrings', 'multipolygons']

    gdf_list = []

    # Iterate through the layers and read each one
    for layer in layers:
        try:
            # Read the layer from the PBF file
            gdf = gpd.read_file("/Users/will/DevSeed/Personal/watermap/data/raw/output/europe_toilets.pbf", engine="pyogrio", layer=layer)

            # Add a new column to indicate the layer
            gdf['layer'] = layer

            # Append the GeoDataFrame to the list
            gdf_list.append(gdf)

            # Optionally print the first few rows of the GeoDataFrame
            print(f"Layer: {layer}, Number of features: {len(gdf)}")

            # Export the layer as a separate .geojson, to later add as tile layers in tippecanoe

            if len(gdf) > 0:
                export = gdf[["osm_id", "geometry"]]
                export.to_file(f"/Users/will/DevSeed/Personal/watermap/data/raw/geojsons/{layer}.geojson", driver="GeoJSON")
            else:
                print(f"Nothing to write to {layer}.geojson. Skipping...")
        except Exception as e:
            print(f"Failed to read layer {layer}: {e}")
    return (gdf_list,)


@app.cell
def _(gdf_list, gpd, pd):
    # Concatenate all GeoDataFrames in the list into a single GeoDataFrame
    combined_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
    return (combined_gdf,)


@app.cell
def _(combined_gdf):
    combined_gdf_min = combined_gdf[["osm_id", "geometry"]]
    return (combined_gdf_min,)


@app.cell
def _(combined_gdf_min):
    combined_gdf_min
    return


@app.cell
def _(combined_gdf_min, viz):
    viz(combined_gdf_min)
    return


@app.cell
def _(gpd):
    # Help for the engine: https://github.com/geopandas/geopandas/discussions/3015

    water = gpd.read_file("/Users/will/DevSeed/Personal/watermap/data/raw/output/europe_water.pbf", engine="pyogrio", layer = "points")
    toilets = gpd.read_file("/Users/will/DevSeed/Personal/watermap/data/raw/output/europe_toilets.pbf", engine="pyogrio", layer="points")
    benches = gpd.read_file("/Users/will/DevSeed/Personal/watermap/data/raw/output/europe_benches.pbf", engine="pyogrio", layer="points")
    return benches, toilets, water


@app.cell
def _(benches, toilets, water):
    print(len(water), "drinking water POIs,", len(toilets), "toilet POIs, and", len(benches), "bench/picnic table POIs")
    return


@app.cell
def _(toilets, water):
    water_1 = water[['osm_id', 'name', 'geometry', 'other_tags']]
    toilets_1 = toilets[['osm_id', 'name', 'geometry', 'other_tags']]
    return toilets_1, water_1


@app.cell
def _(toilets_1, viz, water_1):
    viz([toilets_1, water_1])
    return


@app.cell
def _(water_1):
    water_min = water_1[['osm_id', 'geometry']]
    return


@app.cell
def _(toilets_1):
    toilets_min = toilets_1[['osm_id', 'geometry']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---

    ## SAC Scale
    """
    )
    return


@app.cell
def _(pd):
    def _extract_sac_scale(other_tags):
        if pd.isna(other_tags) or 'sac_scale' not in other_tags:
            return None
        import re
        match = re.search('"sac_scale"=>\\"([^\\"]+)\\"', other_tags)
        return match.group(1) if match else None
    return


@app.cell
def _(gpd, pd, re):
    def _extract_sac_scale(other_tags):
        if pd.isna(other_tags) or 'sac_scale' not in other_tags:
            return None
        match = re.search('"sac_scale"=>\\"([^\\"]+)\\"', other_tags)
        return match.group(1) if match else None
    sac_gdf = gpd.read_file('/Users/will/DevSeed/Personal/watermap/data/raw/output/sac.pbf', engine='pyogrio', layer='lines')
    if 'other_tags' in sac_gdf.columns:
        sac_gdf['sac_scale'] = sac_gdf['other_tags'].apply(_extract_sac_scale)
        print('SAC Scale Distribution:')
        print(sac_gdf['sac_scale'].value_counts(dropna=True))
    return (sac_gdf,)


@app.cell
def _(sac_gdf):
    sac_gdf_1 = sac_gdf[['osm_id', 'name', 'geometry', 'sac_scale']]
    return (sac_gdf_1,)


@app.cell
def _(sac_gdf_1):
    sac_gdf_1.to_file(f'/Users/will/DevSeed/Personal/watermap/data/raw/geojsons/sac.geojson', driver='GeoJSON')
    return


@app.cell
def _(PathLayer, apply_categorical_cmap, sac_gdf_1):
    code_map = {'strolling': 0, 'hiking': 1, 'mountain_hiking': 2, 'demanding_mountain_hiking': 3, 'alpine_hiking': 4, 'demanding_alpine_hiking': 5, 'difficult_alpine_hiking': 6}
    mask = sac_gdf_1['sac_scale'].isin(code_map)
    sac_clean = sac_gdf_1[mask].copy()
    sac_clean['sac_code'] = sac_clean['sac_scale'].map(code_map)
    codes = sac_clean['sac_code'].to_numpy().astype(int)
    colors = [[255, 255, 0], [255, 255, 0], [255, 165, 0], [255, 0, 0], [0, 0, 255], [128, 0, 128], [255, 0, 255]]
    layer_1 = PathLayer.from_geopandas(gdf=sac_clean, get_color=apply_categorical_cmap(codes, colors), width_min_pixels=2)
    return (layer_1,)


@app.cell
def _():
    Voyager = 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json'
    return (Voyager,)


@app.cell
def _(Map, Voyager, layer_1):
    m = Map(layer_1, basemap_style=Voyager)
    m
    return


if __name__ == "__main__":
    app.run()
