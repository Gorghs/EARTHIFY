# Waste Classification Web (Single-Page Edition)

This project is now a fully open, single-page waste classification web app.
It keeps only the AI classification backend and exposes one API endpoint for image prediction.

## What is included

- One-page frontend with drag/drop or click upload
- Instant visual AI result (label, category, icon, confidence, recycling tip)
- No login, signup, leaderboard, admin dashboard, or user history
- Backend API endpoint: `/api/classify`

## API

### `POST /api/classify`

Upload an image as multipart form-data using key `image`.

Example response:

```json
{
  "label": "plastic",
  "category": "Recyclable",
  "icon": "♻️",
  "confidence": 93.42,
  "tip": "Clean plastic before placing it in recycling bins.",
  "imageUrl": "/static/uploads/20260304113000_sample.jpg"
}
```

## Setup

1. Clone repository
2. Place `model.h5` in project root (same folder as `app.py`)
3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run app

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## Notes

- If TensorFlow is missing locally, the UI still loads, but classification API returns model-unavailable error until TensorFlow/model are present.
