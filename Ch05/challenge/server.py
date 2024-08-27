"""Make this server production ready:
- Plug security holes
- Add some logging
- Add some metrics
"""

import csv
import math
from datetime import datetime
from io import StringIO

from fastapi import FastAPI, Request

app = FastAPI()

lat_km = 92
lng_km = 111


def distance(lat1, lng1, lat2, lng2):
    """Return euclidean distance (in kilometers) between two coordinates.

    >>> distance(0, 0, 1, 1)
    144.1700384962146
    """
    delta_lat = (lat1 - lat2) * lat_km
    delta_lng = (lng1 - lng2) * lng_km
    return math.hypot(delta_lat, delta_lng)


def parse_csv(fp):
    """Parse CSV, returns tuple of:
    - number of samples
    - total distance
    - average speed in km/h
    """
    reader = csv.DictReader(fp)
    start_time = end_time = None
    prev_lat = prev_lng = None
    count = total_distance = 0

    for row in reader:
        count += 1
        time = datetime.fromisoformat(row['time'])
        # Rows are in chronological order
        if start_time is None:
            start_time = time
        else:
            end_time = time

        lat, lng = float(row['lat']), float(row['lng'])
        if prev_lat:
            total_distance += distance(lat, lng, prev_lat, prev_lng)
        prev_lat, prev_lng = lat, lng

    duration_hours = (end_time - start_time).total_seconds() / (60 * 60)
    speed = total_distance / duration_hours

    return count, total_distance, speed


@app.post('/run')
async def run_stats(request: Request):
    data = await request.body()
    fp = StringIO(data.decode())
    count, distance, speed = parse_csv(fp)
    out = {
        'count': count,
        'distance': distance,
        'speed': speed,
    }
    return out
