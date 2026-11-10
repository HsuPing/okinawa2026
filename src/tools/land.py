# Encode island outlines (lat/lng) as Google polylines for an offline coastline under the map tiles.
import json, glob, os, sys
def enc_val(v):
    v = ~(v << 1) if v < 0 else (v << 1)
    out = ""
    while v >= 0x20:
        out += chr((0x20 | (v & 0x1f)) + 63); v >>= 5
    return out + chr(v + 63)
def encode(pts):
    out, plat, plng = "", 0, 0
    for lat, lng in pts:
        ilat, ilng = round(lat * 1e5), round(lng * 1e5)
        out += enc_val(ilat - plat) + enc_val(ilng - plng); plat, plng = ilat, ilng
    return out
rings = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], "isl*.json"))):
    r = json.load(open(f))
    if not r: continue
    g = r[0]["geojson"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"] if g["type"] == "MultiPolygon" else []
    for poly in polys:
        ring = poly[0]
        if len(ring) >= 4: rings.append(encode([(c[1], c[0]) for c in ring]))
json.dump(rings, open(sys.argv[2], "w"))
print(len(rings), "rings", sum(map(len, rings)), "chars")
