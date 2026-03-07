# education.py
# This module provides environmental facts, waste statistics, and educational content
# related to waste management and environmental impact.

environmental_facts = [
    {
        "title": "Global Waste Generation Trends",
        "fact": "In 2020, the world generated 2.24 billion tonnes of solid waste, amounting to 0.79 kilograms per person per day. With rapid population growth and urbanization, annual waste generation is expected to increase by 73% from 2020 levels to 3.88 billion tonnes in 2050.",
        "source": "World Bank - Solid Waste Management"
    },
    {
        "title": "Impact of Poor Waste Management",
        "fact": "In low-income countries, over 90% of waste is often disposed in unregulated dumps or openly burned. These practices create serious health, safety, and environmental consequences, including breeding grounds for disease vectors, contributions to global climate change through methane generation, and promotion of urban violence.",
        "source": "World Bank - Solid Waste Management"
    },
    {
        "title": "Waste Management Costs",
        "fact": "Effective waste management is expensive, often comprising 20%–50% of municipal budgets. Operating this essential municipal service requires integrated systems that are efficient, sustainable, and socially supported.",
        "source": "World Bank - Solid Waste Management"
    },
    {
        "title": "US Waste Statistics",
        "fact": "In the United States in 2018, 292.4 million tons of trash were generated, with 146.1 million tons ending up in landfills.",
        "source": "EPA - Facts and Figures about Materials, Waste and Recycling"
    },
    {
        "title": "Recycling and Energy Savings",
        "fact": "Recycling reduces the need for extracting new raw materials, saves energy, and reduces greenhouse gas emissions. For example, recycling one ton of plastic saves 5,774 kWh of energy.",
        "source": "EPA - Facts and Figures about Materials, Waste and Recycling"
    }
]

waste_statistics = [
    {
        "statistic": "Global solid waste generation in 2020: 2.24 billion tonnes",
        "detail": "This equates to 0.79 kg per person per day.",
        "source": "World Bank"
    },
    {
        "statistic": "Projected global waste in 2050: 3.88 billion tonnes",
        "detail": "A 73% increase from 2020 levels due to population growth and urbanization.",
        "source": "World Bank"
    },
    {
        "statistic": "Waste disposal in low-income countries: Over 90% in unregulated dumps or burned",
        "detail": "Leading to health, safety, and environmental issues.",
        "source": "World Bank"
    },
    {
        "statistic": "US trash generation in 2018: 292.4 million tons",
        "detail": "With 146.1 million tons landfilled.",
        "source": "EPA"
    },
    {
        "statistic": "Recycling rate impact",
        "detail": "Increasing recycling rates can significantly reduce landfill use and environmental impact.",
        "source": "EPA"
    }
]

educational_content = [
    {
        "topic": "Importance of Proper Waste Management",
        "content": "Proper waste management is crucial for building sustainable and livable cities. It helps prevent health issues, reduces environmental pollution, and mitigates climate change by capturing methane from landfills and promoting recycling.",
        "tips": [
            "Separate recyclables from trash at home.",
            "Compost organic waste to reduce landfill contributions.",
            "Support local waste management initiatives."
        ],
        "source": "World Bank and EPA"
    },
    {
        "topic": "Reducing Plastic Pollution",
        "content": "Plastic pollution affects oceans, wildlife, and human health. Microplastics enter the food chain, and large plastics harm marine life. Reducing single-use plastics and improving recycling can help.",
        "tips": [
            "Use reusable bags, bottles, and containers.",
            "Avoid plastic straws and cutlery.",
            "Participate in beach cleanups and recycling programs."
        ],
        "source": "General Environmental Knowledge"
    },
    {
        "topic": "Benefits of Recycling",
        "content": "Recycling conserves natural resources, saves energy, reduces pollution, and creates jobs. It also decreases the amount of waste sent to landfills and incinerators.",
        "tips": [
            "Know what materials are recyclable in your area.",
            "Clean recyclables before sorting.",
            "Educate others about recycling benefits."
        ],
        "source": "EPA"
    },
    {
        "topic": "Composting for Environmental Impact",
        "content": "Composting organic waste reduces methane emissions from landfills, enriches soil, and decreases the need for chemical fertilizers. It's a simple way to manage food scraps and yard waste.",
        "tips": [
            "Start a home compost bin.",
            "Include fruit and vegetable scraps, coffee grounds, and yard trimmings.",
            "Avoid adding meat, dairy, or oils to prevent pests."
        ],
        "source": "EPA"
    },
    {
        "topic": "Waste Reduction Strategies",
        "content": "Reducing waste at the source is the most effective way to minimize environmental impact. This includes buying products with less packaging, repairing items instead of discarding them, and choosing durable goods.",
        "tips": [
            "Plan meals to reduce food waste.",
            "Buy in bulk to minimize packaging.",
            "Donate or repurpose items instead of throwing them away."
        ],
        "source": "World Bank and EPA"
    }
]

def get_random_fact():
    """Returns a random environmental fact."""
    import random
    return random.choice(environmental_facts)

def get_random_statistic():
    """Returns a random waste statistic."""
    import random
    return random.choice(waste_statistics)

def get_educational_topic(topic_name):
    """Returns educational content for a specific topic."""
    for item in educational_content:
        if item["topic"].lower() == topic_name.lower():
            return item
    return None

# Example usage:
# fact = get_random_fact()
# print(fact["title"] + ": " + fact["fact"])