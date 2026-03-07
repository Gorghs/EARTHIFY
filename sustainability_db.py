# sustainability_db.py

# This module contains a database of sustainable alternatives and environmental tips
# for various waste categories, aimed at promoting eco-friendly practices.

sustainability_db = {
    "plastic_bottle": {
        "alternatives": [
            "Use a reusable stainless steel or glass water bottle.",
            "Opt for biodegradable or compostable alternatives if available."
        ],
        "tips": [
            "Recycle plastic bottles at designated centers.",
            "Avoid single-use plastics to reduce ocean pollution.",
            "Participate in plastic-free challenges."
        ]
    },
    "paper": {
        "alternatives": [
            "Switch to digital documents and receipts.",
            "Use recycled paper products."
        ],
        "tips": [
            "Recycle paper to save trees and energy.",
            "Print double-sided to reduce paper usage.",
            "Choose FSC-certified paper products."
        ]
    },
    "glass": {
        "alternatives": [
            "Use glass jars for storage instead of disposable containers.",
            "Opt for reusable glassware."
        ],
        "tips": [
            "Recycle glass infinitely without loss of quality.",
            "Avoid breaking glass to prevent contamination in recycling bins.",
            "Support local glass recycling programs."
        ]
    },
    "metal_can": {
        "alternatives": [
            "Choose canned goods with recyclable packaging.",
            "Use bulk buying to reduce packaging."
        ],
        "tips": [
            "Recycle aluminum and steel cans to conserve resources.",
            "Rinse cans before recycling.",
            "Buy products in recyclable metal containers."
        ]
    },
    "organic_waste": {
        "alternatives": [
            "Compost food scraps at home.",
            "Use biodegradable bags for composting."
        ],
        "tips": [
            "Compost to reduce methane emissions from landfills.",
            "Avoid food waste by planning meals.",
            "Start a community composting program."
        ]
    },
    "electronic_waste": {
        "alternatives": [
            "Repair and refurbish electronics instead of discarding.",
            "Buy durable, long-lasting devices."
        ],
        "tips": [
            "Recycle e-waste at certified facilities to recover valuable materials.",
            "Donate old electronics for reuse.",
            "Avoid frequent upgrades to reduce e-waste."
        ]
    },
    "cardboard": {
        "alternatives": [
            "Use cardboard boxes for storage or crafts.",
            "Opt for minimal packaging products."
        ],
        "tips": [
            "Recycle cardboard to make new paper products.",
            "Flatten boxes to save space in recycling bins.",
            "Support businesses with sustainable packaging."
        ]
    },
    "textile": {
        "alternatives": [
            "Buy second-hand clothing.",
            "Choose natural fiber fabrics like cotton or wool."
        ],
        "tips": [
            "Donate unwanted clothes to charities.",
            "Recycle textiles into new products.",
            "Wash clothes in cold water to save energy."
        ]
    }
}

def get_sustainability_info(waste_category):
    """
    Retrieve sustainable alternatives and environmental tips for a given waste category.

    Args:
        waste_category (str): The category of waste (e.g., 'plastic_bottle').

    Returns:
        dict: A dictionary with 'alternatives' and 'tips' lists, or None if not found.
    """
    return sustainability_db.get(waste_category.lower().replace(" ", "_"), None)

# Example usage:
# info = get_sustainability_info("plastic bottle")
# if info:
#     print("Alternatives:", info["alternatives"])
#     print("Tips:", info["tips"])