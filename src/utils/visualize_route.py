import folium
import pandas as pd
import networkx as nx

def render_route_map(route_coordinates, start_node, end_node,
                     predicted_duration=None, predicted_fare=None,
                     output_path="outputs/route_map.html"):
    lats= [c[0] for c in route_coordinates]
    lons= [c[1] for c in route_coordinates]
    center= [sum(lats) / len(lats), sum(lons) / len(lons)]

    m= folium.Map(location=center, zoom_start=12, tiles="cartodbpositron")

    folium.PolyLine(
        locations=route_coordinates,
        color="#2E7D32",
        weight=5,
        opacity=0.8,
        tooltip="Optimized Route"
    ).add_to(m)

    folium.Marker(
        location=route_coordinates[0],
        popup=f"Start (Node {start_node})",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)

    folium.Marker(
        location=route_coordinates[-1],
        popup=f"End (Node {end_node})",
        icon=folium.Icon(color="red", icon="stop")
    ).add_to(m)

    for i, coord in enumerate(route_coordinates[1:-1], start=1):
        folium.CircleMarker(
            location=coord,
            radius=4,
            color="#1B5E20",
            fill=True,
            fill_opacity=0.9,
            popup=f"Stop {i}"
        ).add_to(m)

    if predicted_duration and predicted_fare:
        info_html = f"""
        <div style="position: fixed; top: 10px; right: 10px; z-index: 1000;
                    background: white; padding: 12px; border-radius: 8px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.3); font-family: sans-serif;">
            <b>Predicted Duration:</b> {predicted_duration:.1f} min<br>
            <b>Predicted Fare:</b> ${predicted_fare:.2f}
        </div>
        """
        m.get_root().html.add_child(folium.Element(info_html))

    m.save(output_path)
    print(f"Map saved to {output_path}")
    return m

def render_comparison_map(graph, ga_path, start_node, end_node, output_path="outputs/comparison_map.html"):
    try:
        shortest= nx.shortest_path(graph, start_node, end_node, weight="distance")
    except nx.NetworkXNoPath:
        shortest= None

    zone_coords = pd.read_parquet("data/processed/zone_coords.parquet").set_index("LocationID")

    def to_coords(path):
        return [[zone_coords.loc[n, "lat"], zone_coords[n, "lon"]] for n in path]
    
    ga_coords= to_coords(ga_path)
    lats= [c[0] for c in ga_coords]
    lons= [c[1] for c in ga_coords]
    m= folium.Map(location=[sum(lats)/len(lats), sum(lons)/len(lons)], zoom_start=12, tiles="cartodbpositron")
    
    folium.PolyLine(ga_coords, color="#2E7D32", weight=5, tooltip="GA Optimized Route").add_to(m)

    if shortest:
        shortest_coords= to_coords(shortest)
        folium.PolyLine(shortest_coords, color="#C62828", weight=4, dash_array="8", tooltip="Shortest Path (baseline)").add_to(m)

    folium.Marker(ga_coords[0], popup="Start", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(ga_coords[-1], popup="End", icon=folium.Icon(color="red")).add_to(m)

    legend_html = """
    <div style="position: fixed; bottom: 20px; left: 20px; z-index: 1000;
                background: white; padding: 10px; border-radius: 8px; font-family: sans-serif;">
        <span style="color:#2E7D32;">■</span> GA Optimized Route<br>
        <span style="color:#C62828;">■</span> Shortest Path (baseline)
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    m.save(output_path)
    return m
if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    sample_coords = [
        [40.7128, -74.0060],
        [40.7300, -73.9950],
        [40.7484, -73.9857]
    ]
    render_route_map(sample_coords, start_node=1, end_node=3, 
                     predicted_duration=18.5, predicted_fare=14.20)