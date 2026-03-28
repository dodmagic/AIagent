#!/usr/bin/env python3
"""Query local weather based on IP geolocation and print a readable summary."""

import json
import sys
import urllib.request
from datetime import datetime, timezone


def get_location():
    """Get approximate location from public IP using ip-api.com."""
    url = "http://ip-api.com/json/"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    if data.get("status") != "success":
        raise RuntimeError(f"Geolocation failed: {data}")
    return {
        "city": data.get("city", "Unknown"),
        "region": data.get("regionName", ""),
        "country": data.get("country", ""),
        "lat": data["lat"],
        "lon": data["lon"],
    }


def get_weather(lat, lon):
    """Fetch current weather from Open-Meteo (no API key required)."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&temperature_unit=celsius"
        f"&windspeed_unit=kmh"
    )
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    return data["current_weather"]


WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def main():
    try:
        loc = get_location()
    except Exception as e:
        print(f"Error determining location: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        weather = get_weather(loc["lat"], loc["lon"])
    except Exception as e:
        print(f"Error fetching weather: {e}", file=sys.stderr)
        sys.exit(1)

    condition = WMO_CODES.get(weather.get("weathercode"), "Unknown")
    location_str = ", ".join(
        part for part in [loc["city"], loc["region"], loc["country"]] if part
    )

    print(f"Location:    {location_str}")
    print(f"Temperature: {weather['temperature']} °C")
    print(f"Condition:   {condition}")
    print(f"Wind speed:  {weather['windspeed']} km/h")
    print(f"Timestamp:   {weather.get('time', 'N/A')}")
    print(f"Queried at:  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")


if __name__ == "__main__":
    main()
