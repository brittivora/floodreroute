FloodReroute	—	Flood-Aware	Routing	System	for	Mumbai

A working, end-to-end flood-risk-aware routing system for Mumbai:
real road graph → SAR-enhanced risk scoring → risk-weighted A* routing → FastAPI backend → Leaflet map.

Everything used here is free — no API keys, no paid tiles, no paid hosting required.

## Features

- **Full Mumbai road network** (100k+ nodes) from OpenStreetMap via OSMnx
- **SAR-based flood detection** using Sentinel-1 change-detection via Google Earth Engine
- **Real elevation data** from SRTM (NASA, free)
- **Live rainfall** from Open-Meteo (free, no API key)
- **Risk scoring** blending SAR flood history (60%) + elevation (40%) × rainfall
- **Risk-weighted A* routing** that avoids flood-prone roads
- **Interactive Leaflet map** with color-coded risk overlay and address geocoding

## Run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open: http://127.0.0.1:8000/

- Search for any Mumbai address or select Origin/Destination and click the map.
- Choose a rainfall level and compare safest, fastest, and high-risk routes.

Local runs use the full Greater Mumbai graph by default. If the graph cache is
missing, OSMnx downloads it and saves it locally. Set `FLOOD_GRAPH_CACHE` to
choose a different cache path.

## Render demo

`render.yaml` defines a single free web service for both the API and map UI.
It packages `render_graph.graphml`, a prebuilt 4.5 km-radius OSM road graph
with about 6,600 nodes covering Juhu, Vile Parle, Bandra, BKC, and Kurla. The build
loads this cache instead of depending on Render's access to the Overpass API.
Picks too far from the included roads are rejected instead of being routed to
a misleading nearby node.

Deploy the Blueprint from a Git repository containing this project and its
Render files. Open the resulting service URL to use the same search-and-map UI.
The graph area can be adjusted in the Blueprint with `FLOOD_GRAPH_CENTER_LAT`,
`FLOOD_GRAPH_CENTER_LON`, and `FLOOD_GRAPH_RADIUS_M`.

## SAR Flood History (Google Earth Engine)

The risk model uses Sentinel-1 SAR change-detection to identify historically
flood-prone locations. This data is pre-computed and cached:

1. **One-time setup** (already done):
   ```bash
   pip install earthengine-api geemap
   earthengine authenticate
   ```

2. **Generate/refresh the SAR cache** (queries GEE for 5 flood events):
   ```bash
   python generate_sar_cache.py
   ```
   This produces `mumbai_sar_flood_history.json` (~3,880 flood-prone nodes).

3. **Automatic loading**: `main.py` loads the cache at startup. If the file
   doesn't exist, risk scoring falls back to elevation-only (still works).

## Files

- `main.py` — FastAPI backend (`/risk`, `/route`, `/geocode`, `/refresh-risk` endpoints)
- `graph_utils.py` — loads the road graph (real OSMnx or synthetic demo)
- `risk.py` — risk scoring: SAR flood history + elevation + rainfall
- `router.py` — risk-weighted A* routing
- `gee_sar.py` — Google Earth Engine Sentinel-1 SAR flood detection module
- `generate_sar_cache.py` — batch pre-computes SAR flood history for all road nodes
- `render_graph.graphml` — bounded road graph packaged for Render
- `mumbai_sar_flood_history.json` — cached SAR flood frequency data (3,880 nodes)
- `mumbai_graph_cache.graphml` — cached Mumbai road network (101,907 nodes)
- `static/index.html` — Leaflet frontend, free OpenStreetMap tiles

