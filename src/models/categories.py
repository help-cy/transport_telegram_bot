from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Category:
    name: str
    subcategories: List[str]


CATEGORIES: Dict[str, List[str]] = {
    "Damage": [
        "Road",
        "Pavement, footpath",
        "Cycle path",
        "Pedestrian crossing",
        "Traffic sign",
        "Lighting",
        "Sewer, drainage, manhole",
        "Traffic lights",
        "Bridge, tunnel",
        "Bus stop",
        "Road equipment (e.g. poles, bins, benches)",
        "Traffic barrier, safety rail",
        "Exposed wire",
        "Water pipe",
        "Retaining wall",
        "Other"
    ],
    "Obstacle": [
        "Road",
        "Pavement, footpath",
        "Cycle path",
        "Pedestrian crossing",
        "Traffic sign",
        "Traffic lights",
        "Bridge, tunnel",
        "Bus stop",
        "Road equipment (e.g. poles, bins, benches)",
        "Other"
    ],
    "Vandalism": [
        "Road",
        "Pavement, footpath",
        "Cycle path",
        "Traffic sign",
        "Lighting",
        "Traffic lights",
        "Bridge, tunnel",
        "Bus stop",
        "Road equipment (e.g. poles, bins, benches)",
        "Traffic barrier, safety rail",
        "Water pipe",
        "Retaining wall",
        "Other"
    ],
    "Vegetation, tree (fall / pruning)": [
        "Road",
        "Pavement, footpath",
        "Cycle path",
        "Traffic sign",
        "Lighting",
        "Traffic lights",
        "Bus stop",
        "Other"
    ],
    "Animals": [
        "Road",
        "Pavement, footpath",
        "Cycle path",
        "Pedestrian crossing",
        "Other"
    ],
    "Landslide": [
        "Road",
        "Pavement, footpath",
        "Cycle path",
        "Pedestrian crossing",
        "Retaining wall",
        "Other"
    ],
    "Blockage": [
        "Sewer, drainage, manhole",
        "Water pipe",
        "Other"
    ],
    "Flood": [
        "Road",
        "Pavement, footpath",
        "Cycle path",
        "Sewer, drainage, manhole",
        "Bridge, tunnel",
        "Other"
    ],
    "Other": [
        "Road",
        "Pavement, footpath",
        "Cycle path",
        "Pedestrian crossing",
        "Traffic sign",
        "Lighting",
        "Sewer, drainage, manhole",
        "Traffic lights",
        "Bridge, tunnel",
        "Bus stop",
        "Road equipment (e.g. poles, bins, benches)",
        "Traffic barrier, safety rail",
        "Exposed wire",
        "Water pipe",
        "Retaining wall",
        "Other"
    ]
}


def get_all_categories() -> List[str]:
    return list(CATEGORIES.keys())


def get_subcategories_for_category(
    category: str
) -> List[str]:
    return CATEGORIES.get(
        category,
        CATEGORIES["Other"]
    )
