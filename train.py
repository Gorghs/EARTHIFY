from ultralytics import YOLO

# Load pre-trained model
model = YOLO('yolov8n.pt')

# To train the model, provide the correct path to your data.yaml file
# Example: path = 'path/to/your/data.yaml'
# results = model.train(data=path, epochs=50)
# results = model.val()
# success = model.export(format='onnx')

