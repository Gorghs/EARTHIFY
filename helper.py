from ultralytics import YOLO
import time
import streamlit as st
import cv2
import settings
import threading
import gamification

def sleep_and_clear_success():
    time.sleep(3)
    if 'recyclable_placeholder' in st.session_state:
        st.session_state['recyclable_placeholder'].empty()
    if 'non_recyclable_placeholder' in st.session_state:
        st.session_state['non_recyclable_placeholder'].empty()
    if 'hazardous_placeholder' in st.session_state:
        st.session_state['hazardous_placeholder'].empty()

def load_model(model_path):
    model = YOLO(model_path)
    return model

def classify_waste_type(detected_items):
    recyclable_items = set(detected_items) & set(settings.RECYCLABLE)
    non_recyclable_items = set(detected_items) & set(settings.NON_RECYCLABLE)
    hazardous_items = set(detected_items) & set(settings.HAZARDOUS)
    
    return recyclable_items, non_recyclable_items, hazardous_items

def remove_dash_from_class_name(class_name):
    return class_name.replace("_", " ")

def _display_detected_frames(model, st_frame, image):
    image = cv2.resize(image, (640, int(640*(9/16))))
    
    if 'unique_classes' not in st.session_state:
        st.session_state['unique_classes'] = set()

    if 'recyclable_placeholder' not in st.session_state:
        st.session_state['recyclable_placeholder'] = st.sidebar.empty()
    if 'non_recyclable_placeholder' not in st.session_state:
        st.session_state['non_recyclable_placeholder'] = st.sidebar.empty()
    if 'hazardous_placeholder' not in st.session_state:
        st.session_state['hazardous_placeholder'] = st.sidebar.empty()

    if 'last_detection_time' not in st.session_state:
        st.session_state['last_detection_time'] = 0

    try:
        res = model.predict(image, conf=0.6)
        names = model.names
        detected_items = set()

        for result in res:
            if result.boxes is not None and len(result.boxes) > 0:
                new_classes = set([names[int(c)] for c in result.boxes.cls])
                if new_classes != st.session_state['unique_classes']:
                    st.session_state['unique_classes'] = new_classes
                    st.session_state['recyclable_placeholder'].markdown('')
                    st.session_state['non_recyclable_placeholder'].markdown('')
                    st.session_state['hazardous_placeholder'].markdown('')
                    detected_items.update(st.session_state['unique_classes'])

                    recyclable_items, non_recyclable_items, hazardous_items = classify_waste_type(detected_items)

                    # Add gamification points for detections
                    game = gamification.Gamification()
                    for item in recyclable_items:
                        game.add_detection('recyclable', item)
                    for item in non_recyclable_items:
                        game.add_detection('non_recyclable', item)
                    for item in hazardous_items:
                        game.add_detection('hazardous', item)

                    if recyclable_items:
                        detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in recyclable_items)
                        st.session_state['recyclable_placeholder'].markdown(
                            f"<div class='stRecyclable'>♻️ Recyclable items:\n\n- {detected_items_str}</div>",
                            unsafe_allow_html=True
                        )
                    if non_recyclable_items:
                        detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in non_recyclable_items)
                        st.session_state['non_recyclable_placeholder'].markdown(
                            f"<div class='stNonRecyclable'>🗑️ Non-Recyclable items:\n\n- {detected_items_str}</div>",
                            unsafe_allow_html=True
                        )
                    if hazardous_items:
                        detected_items_str = "\n- ".join(remove_dash_from_class_name(item) for item in hazardous_items)
                        st.session_state['hazardous_placeholder'].markdown(
                            f"<div class='stHazardous'>⚠️ Hazardous items:\n\n- {detected_items_str}</div>",
                            unsafe_allow_html=True
                        )

                    threading.Thread(target=sleep_and_clear_success, daemon=True).start()
                    st.session_state['last_detection_time'] = time.time()

        # Plot results
        if len(res) > 0 and res[0].boxes is not None and len(res[0].boxes) > 0:
            res_plotted = res[0].plot()
            st_frame.image(res_plotted, channels="BGR")
        else:
            st_frame.image(image, channels="BGR")
    except Exception as e:
        st.sidebar.error(f"Detection error: {str(e)}")


def play_webcam(model):
    source_webcam = settings.WEBCAM_PATH
    
    # Initialize session state
    if 'detecting' not in st.session_state:
        st.session_state['detecting'] = False
    
    # Create columns for buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button('🎬 Start Detection', use_container_width=True):
            st.session_state['detecting'] = True
    
    with col2:
        if st.button('⏹️ Stop Detection', use_container_width=True):
            st.session_state['detecting'] = False
    
    with col3:
        st.write("")  # spacer
    
    # Container for status and frames
    status_container = st.container()
    frame_container = st.container()
    
    if st.session_state['detecting']:
        status_container.info("🟢 Detection is running... Initializing webcam...")
        
        try:
            # Open webcam
            vid_cap = cv2.VideoCapture(source_webcam)
            
            # Check if webcam is available
            if not vid_cap.isOpened():
                status_container.error("❌ Cannot access webcam. Please:")
                st.error("• Check if webcam is connected")
                st.error("• Check if webcam is not in use by another application")  
                st.error("• Refresh the page and try again")
                st.session_state['detecting'] = False
                vid_cap.release()
                return
            
            # Set webcam properties
            vid_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            vid_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            vid_cap.set(cv2.CAP_PROP_FPS, 30)
            
            st_frame = frame_container.empty()
            frame_count = 0
            max_frames = 1000  # Increased limit
            
            status_container.success("✅ Webcam connected! Processing frames...")
            
            while st.session_state['detecting'] and frame_count < max_frames:
                success, image = vid_cap.read()
                
                if success:
                    # Flip for mirror effect
                    image = cv2.flip(image, 1)
                    _display_detected_frames(model, st_frame, image)
                    frame_count += 1
                    
                    # Update status every 30 frames
                    if frame_count % 30 == 0:
                        status_container.metric("Frames Processed", frame_count)
                else:
                    status_container.warning("⚠️ Failed to read frame from webcam")
                    break
            
            vid_cap.release()
            
            if st.session_state['detecting']:
                st.session_state['detecting'] = False
            
            if frame_count > 0:
                status_container.success(f"✅ Detection completed! Processed {frame_count} frames")
            
        except Exception as e:
            status_container.error(f"❌ Error during detection: {str(e)}")
            st.session_state['detecting'] = False
    else:
        status_container.info("👉 Click 'Start Detection' to begin analyzing waste")
        frame_container.empty()
