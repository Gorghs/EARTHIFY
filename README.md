# EARTHIFY - Intelligent Waste Classification System

A modern web application for real-time waste classification using YOLO object detection. Identify recyclable, non-recyclable, and hazardous waste items through image upload or live camera feed.

## Features

✨ **AI Detection** - Real-time YOLO-based waste classification  
📱 **Real-time Processing** - Instant results with confidence scores  
📸 **Image Upload** - Upload photos for quick classification  
📹 **Live Camera** - Use your webcam for live detection  
💡 **Eco Tips** - Get sustainability recommendations for each waste type  
🌍 **Sustainable Impact** - Learn about waste reduction and recycling

## Demo

Visit: https://earthify-waste-classifier.onrender.com

## Quick Start

### Local Setup

```bash
cd Waste-Classification-Web
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` in your browser.

### Using Docker

```bash
docker build -t earthify .
docker run -p 5000:5000 earthify
```

## Project Structure

```
Waste-Classification-Web/
├── app.py                 # Flask application
├── static/
│   ├── app.js            # Client-side functionality
│   ├── style.css         # UI styling (black & white theme)
│   └── uploads/          # User uploaded images
├── templates/
│   └── index.html        # Main web interface
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version (3.12.7)
├── Procfile              # Render deployment config
└── Dockerfile            # Docker configuration

../weights/
├── best.onnx             # YOLO model (ONNX format)
├── best.pt               # YOLO model (PyTorch)
└── last.pt               # Training checkpoint
```

## Waste Categories

The model classifies waste into 12 categories:
- Battery
- Biological
- Brown Glass
- Cardboard
- Clothes
- Green Glass
- Metal
- Paper
- Plastic
- Shoes
- Trash
- White Glass

## Technology Stack

- **Backend**: Flask 3.0.3
- **ML Framework**: ONNX Runtime (YOLOv8)
- **Image Processing**: Pillow, NumPy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Render, Docker
- **Production Server**: Gunicorn

## Author

**Karthick V**
- GitHub: [@Gorghs](https://github.com/Gorghs)
- LinkedIn: [karthickv4](https://linkedin.com/in/karthickv4/)
- Email: karthick.venkatachalem@gmail.com
- Portfolio: [karthick-rnen.onrender.com](https://karthick-rnen.onrender.com)

## License

MIT License - Feel free to use this project for educational and commercial purposes.

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [YOLO Documentation](https://github.com/ultralytics/yolov5)

