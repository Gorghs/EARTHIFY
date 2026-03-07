import streamlit as st
import cv2
from pathlib import Path
from ultralytics import YOLO
import settings

st.set_page_config(page_title="Simple Object Detection", layout="centered")

st.title("🔍 Simple Object Detection")

# Load the model
model_path = Path(settings.DETECTION_MODEL)

@st.cache_resource
def load_model(path):
    return YOLO(path)

with st.spinner("Loading AI model..."):
    try:
        model = load_model(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Camera Feed")
    frame_placeholder = st.empty()

with col2:
    st.markdown("### Detected")
    text_placeholder = st.empty()

# Camera Controls
st.sidebar.title("Controls")
start_btn = st.sidebar.button('🎬 Start Camera')
stop_btn = st.sidebar.button('⏹️ Stop Camera')

if 'running' not in st.session_state:
    st.session_state['running'] = False

if start_btn:
    st.session_state['running'] = True
if stop_btn:
    st.session_state['running'] = False

if st.session_state['running']:
    cap = cv2.VideoCapture(settings.WEBCAM_PATH)
    
    if not cap.isOpened():
        st.error("Cannot access the camera. Please check your camera connection.")
        st.session_state['running'] = False
    
    while st.session_state['running']:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to read from camera.")
            break
            
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Predict
        results = model.predict(frame, conf=0.5, verbose=False)
        
        detected_names = set()
        
        if len(results) > 0:
            # Draw bounding boxes
            frame = results[0].plot()
            
            # Extract just the object names
            if results[0].boxes is not None:
                for cls in results[0].boxes.cls:
                    name = model.names[int(cls)].replace('_', ' ').title()
                    detected_names.add(name)
        
        # Convert BGR to RGB for Streamlit display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, use_container_width=True)
        
        # Display the text of what was found
        if detected_names:
            items_list = "\n".join([f"- **{name}**" for name in detected_names])
            text_placeholder.markdown(items_list)
        else:
            text_placeholder.info("Nothing detected...")
            
    if cap.isOpened():
        cap.release()
else:
    frame_placeholder.info("Click 'Start Camera' in the sidebar to begin detection.")
    text_placeholder.empty()

