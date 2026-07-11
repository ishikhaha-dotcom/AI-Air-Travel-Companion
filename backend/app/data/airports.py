"""Static reference data for the 35 airports in flights_data.csv.

Hand-embedded (no external API): IANA timezone for local-time/daypart/redeye
logic, lat/lon for the offline SVG route map, city aliases for the NLU
gazetteer, and region sets for open-ended trips ("multi-city Asia trip").
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Airport:
    iata: str
    city: str
    country: str
    lat: float
    lon: float
    tz: str


_A = Airport
AIRPORTS: dict[str, Airport] = {a.iata: a for a in [
    _A("AKL", "Auckland", "New Zealand", -37.01, 174.79, "Pacific/Auckland"),
    _A("AMS", "Amsterdam", "Netherlands", 52.31, 4.76, "Europe/Amsterdam"),
    _A("BCN", "Barcelona", "Spain", 41.30, 2.08, "Europe/Madrid"),
    _A("BKK", "Bangkok", "Thailand", 13.69, 100.75, "Asia/Bangkok"),
    _A("BOM", "Mumbai", "India", 19.09, 72.87, "Asia/Kolkata"),
    _A("CDG", "Paris", "France", 49.01, 2.55, "Europe/Paris"),
    _A("CPT", "Cape Town", "South Africa", -33.97, 18.60, "Africa/Johannesburg"),
    _A("DEL", "Delhi", "India", 28.57, 77.10, "Asia/Kolkata"),
    _A("DOH", "Doha", "Qatar", 25.27, 51.61, "Asia/Qatar"),
    _A("DPS", "Denpasar", "Indonesia", -8.75, 115.17, "Asia/Makassar"),
    _A("DXB", "Dubai", "UAE", 25.25, 55.36, "Asia/Dubai"),
    _A("FCO", "Rome", "Italy", 41.80, 12.24, "Europe/Rome"),
    _A("FRA", "Frankfurt", "Germany", 50.03, 8.56, "Europe/Berlin"),
    _A("GIG", "Rio de Janeiro", "Brazil", -22.81, -43.25, "America/Sao_Paulo"),
    _A("GRU", "Sao Paulo", "Brazil", -23.43, -46.47, "America/Sao_Paulo"),
    _A("HKG", "Hong Kong", "Hong Kong", 22.31, 113.91, "Asia/Hong_Kong"),
    _A("ICN", "Seoul", "South Korea", 37.46, 126.44, "Asia/Seoul"),
    _A("IST", "Istanbul", "Turkey", 41.28, 28.75, "Europe/Istanbul"),
    _A("JFK", "New York", "USA", 40.64, -73.78, "America/New_York"),
    _A("KUL", "Kuala Lumpur", "Malaysia", 2.75, 101.71, "Asia/Kuala_Lumpur"),
    _A("LAX", "Los Angeles", "USA", 33.94, -118.41, "America/Los_Angeles"),
    _A("LHR", "London", "UK", 51.47, -0.45, "Europe/London"),
    _A("LIS", "Lisbon", "Portugal", 38.77, -9.13, "Europe/Lisbon"),
    _A("MAA", "Chennai", "India", 12.99, 80.17, "Asia/Kolkata"),
    _A("MEL", "Melbourne", "Australia", -37.67, 144.84, "Australia/Melbourne"),
    _A("MEX", "Mexico City", "Mexico", 19.44, -99.07, "America/Mexico_City"),
    _A("NRT", "Tokyo", "Japan", 35.77, 140.39, "Asia/Tokyo"),
    _A("ORD", "Chicago", "USA", 41.97, -87.91, "America/Chicago"),
    _A("PEK", "Beijing", "China", 40.08, 116.58, "Asia/Shanghai"),
    _A("PVG", "Shanghai", "China", 31.14, 121.81, "Asia/Shanghai"),
    _A("SFO", "San Francisco", "USA", 37.62, -122.38, "America/Los_Angeles"),
    _A("SIN", "Singapore", "Singapore", 1.36, 103.99, "Asia/Singapore"),
    _A("SVO", "Moscow", "Russia", 55.97, 37.41, "Europe/Moscow"),
    _A("SYD", "Sydney", "Australia", -33.95, 151.18, "Australia/Sydney"),
    _A("YYZ", "Toronto", "Canada", 43.68, -79.61, "America/Toronto"),
]}


@lru_cache(maxsize=64)
def tzinfo(iata: str) -> ZoneInfo:
    return ZoneInfo(AIRPORTS[iata].tz)


# NLU gazetteer: lowercase alias -> IATA. Includes every dataset city name plus
# common traveler phrasings ("tokyo", "bali", "nyc", ...).
CITY_ALIASES: dict[str, str] = {a.city.lower(): a.iata for a in AIRPORTS.values()}
CITY_ALIASES.update({
    "tokyo": "NRT", "narita": "NRT",
    "bali": "DPS", "denpasar": "DPS",
    "new york": "JFK", "nyc": "JFK", "new york city": "JFK", "manhattan": "JFK",
    "london": "LHR", "heathrow": "LHR",
    "paris": "CDG", "rome": "FCO", "roma": "FCO",
    "bombay": "BOM", "madras": "MAA", "peking": "PEK",
    "sao paulo": "GRU", "são paulo": "GRU", "rio": "GIG",
    "la": "LAX", "san fran": "SFO", "frisco": "SFO",
    "moscow": "SVO", "seoul": "ICN", "incheon": "ICN",
    "kl": "KUL", "hongkong": "HKG", "hong kong": "HKG",
    "istanbul": "IST", "dubai": "DXB", "doha": "DOH",
    "chicago": "ORD", "toronto": "YYZ", "sydney": "SYD", "melbourne": "MEL",
    "auckland": "AKL", "cape town": "CPT", "capetown": "CPT",
    "amsterdam": "AMS", "frankfurt": "FRA", "barcelona": "BCN",
    "lisbon": "LIS", "singapore": "SIN", "bangkok": "BKK",
    "beijing": "PEK", "shanghai": "PVG", "delhi": "DEL", "mumbai": "BOM",
    "chennai": "MAA", "mexico city": "MEX", "mexico": "MEX",
})

REGIONS: dict[str, set[str]] = {
    "asia": {"NRT", "ICN", "PEK", "PVG", "HKG", "BKK", "SIN", "KUL", "DPS", "DEL", "BOM", "MAA"},
    "europe": {"LHR", "CDG", "FCO", "AMS", "FRA", "BCN", "LIS", "IST", "SVO"},
    "americas": {"JFK", "ORD", "LAX", "SFO", "YYZ", "MEX", "GRU", "GIG"},
    "middle east": {"DOH", "DXB"},
    "oceania": {"SYD", "MEL", "AKL"},
}

ALLIANCE_MEMBERS: dict[str, set[str]] = {
    # from the dataset's airline_code/alliance pairs (18 carriers)
    "star": {"NH", "LH", "SQ", "TG", "AI", "UA"},
    "oneworld": {"AA", "BA", "CX", "JL", "QF", "QR"},
    "skyteam": {"AF", "DL", "KE", "KL"},
    "none": {"EK", "TK"},
}


def alliance_of(airline_code: str) -> str:
    for name, members in ALLIANCE_MEMBERS.items():
        if airline_code in members:
            return name
    return "none"
