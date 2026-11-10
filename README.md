# 沖繩自駕四日遊

2026/11/13 – 11/16 沖繩本島行程，含地圖和天氣預報。

網頁：https://hsuping.github.io/okinawa2026/

## 修改行程

1. 編輯 `src/trip.html`（行程在 `DAYS`，航班在 `FLIGHTS`）
2. 執行 `node src/build.mjs`，產生根目錄的 `index.html`
3. commit 後 push，GitHub Pages 約一分鐘後更新

`index.html` 是建置結果，請不要直接修改。

## 其他檔案

- `src/vendor/leaflet-1.9.4.js`：地圖程式庫 Leaflet（BSD-2-Clause），建置時直接寫進網頁
- `src/tools/routes.py`：用 OSRM 重新計算各段路線並輸出 JSON（`python3 src/tools/routes.py src/data/routes.json`），結果要手動更新到 `trip.html` 的 `PIN` 和 `LEGS`
- `src/tools/land.py`：從 `src/data/geo/` 產生離線海岸線（`python3 src/tools/land.py src/data/geo src/data/land.json`），對應 `trip.html` 的 `LAND`

底圖：國土地理院 地理院タイル。路線：OSRM。道路與海岸線資料 © OpenStreetMap contributors。天氣：Open-Meteo。
