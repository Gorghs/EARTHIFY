import json
import sys
from pathlib import Path
import cv2
from ultralytics import YOLO
import settings

def load_model():
    model_path = Path(settings.DETECTION_MODEL)
    model = YOLO(model_path)
    return model

def map_to_detailed_category(detected_class):
    """
    Map detected waste class to detailed environmental categories
    """
    category_mapping = {
        # Recyclable
        'cardboard_box': {
            'primary_category': 'Paper / Cardboard',
            'is_recyclable': 'Yes',
            'is_biodegradable': 'Yes (compostable)',
            'reasoning': 'Cardboard is made from paper pulp and can be recycled into new paper products. It is also biodegradable in composting facilities.'
        },
        'can': {
            'primary_category': 'Metal',
            'is_recyclable': 'Yes',
            'is_biodegradable': 'No',
            'reasoning': 'Aluminum or steel cans are highly recyclable metals that can be melted down and reused indefinitely.'
        },
        'plastic_bottle_cap': {
            'primary_category': 'Plastic',
            'is_recyclable': 'Yes (check local recycling)',
            'is_biodegradable': 'No',
            'reasoning': 'Plastic bottle caps are typically recyclable but may need to be separated from bottles in some systems. They are made from various plastic resins.'
        },
        'plastic_bottle': {
            'primary_category': 'Plastic',
            'is_recyclable': 'Yes',
            'is_biodegradable': 'No',
            'reasoning': 'PET plastic bottles are widely recyclable and can be turned into new bottles or other plastic products.'
        },
        'reuseable_paper': {
            'primary_category': 'Paper / Cardboard',
            'is_recyclable': 'Yes',
            'is_biodegradable': 'Yes (compostable)',
            'reasoning': 'Paper products are recyclable and biodegradable, helping reduce deforestation and landfill waste.'
        },

        # Non-Recyclable
        'plastic_bag': {
            'primary_category': 'Plastic',
            'is_recyclable': 'No (single-use)',
            'is_biodegradable': 'No',
            'reasoning': 'Thin plastic bags are difficult to recycle due to their light weight and contamination issues. They contribute to environmental pollution.'
        },
        'scrap_paper': {
            'primary_category': 'Paper / Cardboard',
            'is_recyclable': 'Yes',
            'is_biodegradable': 'Yes (compostable)',
            'reasoning': 'Most paper scraps are recyclable unless heavily contaminated with food or chemicals.'
        },
        'stick': {
            'primary_category': 'Biodegradable / Organic',
            'is_recyclable': 'No',
            'is_biodegradable': 'Yes',
            'reasoning': 'Wooden sticks are organic material that will naturally decompose in composting or landfill conditions.'
        },
        'plastic_cup': {
            'primary_category': 'Plastic',
            'is_recyclable': 'Sometimes (check resin code)',
            'is_biodegradable': 'No',
            'reasoning': 'Depends on plastic type - some coated paper cups may not be recyclable. Single-use plastics contribute to pollution.'
        },
        'snack_bag': {
            'primary_category': 'Plastic',
            'is_recyclable': 'No',
            'is_biodegradable': 'No',
            'reasoning': 'Multi-layered snack bags are difficult to recycle due to mixed materials and food contamination.'
        },
        'plastic_box': {
            'primary_category': 'Plastic',
            'is_recyclable': 'Yes',
            'is_biodegradable': 'No',
            'reasoning': 'Rigid plastic containers are generally recyclable if clean and of appropriate plastic type.'
        },
        'straw': {
            'primary_category': 'Plastic',
            'is_recyclable': 'No (single-use)',
            'is_biodegradable': 'No',
            'reasoning': 'Plastic straws are single-use plastics that contribute to ocean pollution and are hard to recycle.'
        },
        'plastic_cup_lid': {
            'primary_category': 'Plastic',
            'is_recyclable': 'Sometimes',
            'is_biodegradable': 'No',
            'reasoning': 'Depends on material - some plastic lids are recyclable, others are mixed materials.'
        },
        'scrap_plastic': {
            'primary_category': 'Plastic',
            'is_recyclable': 'Possibly',
            'is_biodegradable': 'No',
            'reasoning': 'Depends on plastic type and condition - many plastics are recyclable but require sorting.'
        },
        'cardboard_bowl': {
            'primary_category': 'Paper / Cardboard',
            'is_recyclable': 'Yes',
            'is_biodegradable': 'Yes (compostable)',
            'reasoning': 'Cardboard bowls are recyclable and biodegradable, though may have wax coating that affects composting.'
        },
        'plastic_cutlery': {
            'primary_category': 'Plastic',
            'is_recyclable': 'No (single-use)',
            'is_biodegradable': 'No',
            'reasoning': 'Single-use plastic cutlery contributes to environmental pollution and is difficult to recycle.'
        },

        # Hazardous
        'battery': {
            'primary_category': 'E-waste',
            'is_recyclable': 'Yes (special handling)',
            'is_biodegradable': 'No',
            'reasoning': 'Batteries contain toxic chemicals and heavy metals. They require special recycling facilities to safely extract valuable materials.'
        },
        'chemical_spray_can': {
            'primary_category': 'Hazardous waste',
            'is_recyclable': 'No',
            'is_biodegradable': 'No',
            'reasoning': 'Aerosol cans contain pressurized chemicals and may be hazardous waste requiring special disposal.'
        },
        'chemical_plastic_bottle': {
            'primary_category': 'Hazardous waste',
            'is_recyclable': 'No',
            'is_biodegradable': 'No',
            'reasoning': 'Chemical containers may contain residues and require hazardous waste disposal procedures.'
        },
        'chemical_plastic_gallon': {
            'primary_category': 'Hazardous waste',
            'is_recyclable': 'No',
            'is_biodegradable': 'No',
            'reasoning': 'Large chemical containers are hazardous waste and must be disposed of through proper channels.'
        },
        'light_bulb': {
            'primary_category': 'E-waste',
            'is_recyclable': 'Yes (special handling)',
            'is_biodegradable': 'No',
            'reasoning': 'Light bulbs, especially fluorescent ones, contain mercury and require special recycling to prevent environmental contamination.'
        },
        'paint_bucket': {
            'primary_category': 'Hazardous waste',
            'is_recyclable': 'Possibly (if empty and clean)',
            'is_biodegradable': 'No',
            'reasoning': 'Paint buckets may contain toxic chemicals. Empty, clean metal buckets can sometimes be recycled.'
        }
    }

    return category_mapping.get(detected_class, {
        'primary_category': 'Mixed waste',
        'is_recyclable': 'Unknown',
        'is_biodegradable': 'Unknown',
        'reasoning': 'Unable to classify this waste type with certainty.'
    })

def classify_image(image_path, model):
    """
    Analyze image and return classification in specified JSON format
    """
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            return {
                "identified_object": "Unknown",
                "primary_category": "Unknown",
                "is_recyclable": "Unknown",
                "is_biodegradable": "Unknown",
                "confidence_score": "0.0",
                "reasoning": "Image could not be loaded or processed.",
                "alternative_possibility": {
                    "category": "",
                    "confidence": ""
                }
            }

        # Run detection
        results = model.predict(image, conf=0.5)

        if len(results) == 0 or results[0].boxes is None or len(results[0].boxes) == 0:
            return {
                "identified_object": "No objects detected",
                "primary_category": "Unknown",
                "is_recyclable": "Unknown",
                "is_biodegradable": "Unknown",
                "confidence_score": "0.0",
                "reasoning": "No waste objects detected in the image.",
                "alternative_possibility": {
                    "category": "",
                    "confidence": ""
                }
            }

        # Get the highest confidence detection
        boxes = results[0].boxes
        confidences = boxes.conf.cpu().numpy()
        classes = boxes.cls.cpu().numpy().astype(int)

        max_conf_idx = confidences.argmax()
        max_conf = confidences[max_conf_idx]
        detected_class = model.names[classes[max_conf_idx]]

        # Get detailed classification
        details = map_to_detailed_category(detected_class)

        # Check for alternative if confidence is low
        alternative = {"category": "", "confidence": ""}
        if max_conf < 0.8 and len(confidences) > 1:
            # Get second highest
            sorted_indices = confidences.argsort()[::-1]
            if len(sorted_indices) > 1:
                second_idx = sorted_indices[1]
                second_class = model.names[classes[second_idx]]
                second_details = map_to_detailed_category(second_class)
                alternative = {
                    "category": second_details['primary_category'],
                    "confidence": f"{confidences[second_idx]:.2f}"
                }

        return {
            "identified_object": detected_class.replace('_', ' '),
            "primary_category": details['primary_category'],
            "is_recyclable": details['is_recyclable'],
            "is_biodegradable": details['is_biodegradable'],
            "confidence_score": f"{max_conf:.2f}",
            "reasoning": details['reasoning'],
            "alternative_possibility": alternative
        }

    except Exception as e:
        return {
            "identified_object": "Error",
            "primary_category": "Unknown",
            "is_recyclable": "Unknown",
            "is_biodegradable": "Unknown",
            "confidence_score": "0.0",
            "reasoning": f"Processing error: {str(e)}",
            "alternative_possibility": {
                "category": "",
                "confidence": ""
            }
        }

def main():
    if len(sys.argv) != 2:
        print("Usage: python classify_waste.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    if not Path(image_path).exists():
        print(f"Error: Image file '{image_path}' not found.")
        sys.exit(1)

    # Load model
    model = load_model()

    # Classify image
    result = classify_image(image_path, model)

    # Output JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()