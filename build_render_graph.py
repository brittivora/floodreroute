"""Build the bounded road graph packaged with the Render service."""

import os

from graph_utils import get_graph


os.environ.setdefault("FLOOD_GRAPH_MODE", "small")
os.environ.setdefault("FLOOD_GRAPH_CENTER_LAT", "19.065")
os.environ.setdefault("FLOOD_GRAPH_CENTER_LON", "72.850")
os.environ.setdefault("FLOOD_GRAPH_RADIUS_M", "4500")
os.environ.setdefault("FLOOD_GRAPH_CACHE", "render_graph.graphml")

if os.environ["FLOOD_GRAPH_MODE"].lower() != "small":
    raise SystemExit("Render graph build requires FLOOD_GRAPH_MODE=small")

graph = get_graph(
    mode="small",
    center_lat=float(os.environ["FLOOD_GRAPH_CENTER_LAT"]),
    center_lon=float(os.environ["FLOOD_GRAPH_CENTER_LON"]),
    radius_m=int(os.environ["FLOOD_GRAPH_RADIUS_M"]),
)

if graph.number_of_nodes() == 0:
    raise SystemExit("OSM returned an empty bounded road graph")

print(
    f"Built Render road graph: {graph.number_of_nodes()} nodes, "
    f"{graph.number_of_edges()} edges"
)