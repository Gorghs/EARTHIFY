// ==================== DOM ELEMENTS ====================
// Navigation
const homeLink = document.getElementById("homeLink");
const featuresLink = document.getElementById("featuresLink");
const aboutLink = document.getElementById("aboutLink");

// Sections
const homeSection = document.getElementById("homeSection");
const featuresSection = document.getElementById("featuresSection");
const aboutSection = document.getElementById("aboutSection");

// Mode buttons
const uploadModeBtn = document.getElementById("uploadModeBtn");
const liveModeBtn = document.getElementById("liveModeBtn");

// Mode containers
const uploadMode = document.getElementById("uploadMode");
const liveMode = document.getElementById("liveMode");

// Upload elements
const fileInput = document.getElementById("fileInput");
const dropZone = document.getElementById("dropZone");
const previewWrap = document.getElementById("previewWrap");
const previewImage = document.getElementById("previewImage");
const classifyBtn = document.getElementById("classifyBtn");

// Camera elements
const cameraFeed = document.getElementById("cameraFeed");
const captureCanvas = document.getElementById("captureCanvas");
const startCameraBtn = document.getElementById("startCameraBtn");
const stopCameraBtn = document.getElementById("stopCameraBtn");

// Result elements
const resultCard = document.getElementById("resultCard");
const resultIcon = document.getElementById("resultIcon");
const resultLabel = document.getElementById("resultLabel");
const resultCategory = document.getElementById("resultCategory");
const resultConfidence = document.getElementById("resultConfidence");
const resultTip = document.getElementById("resultTip");

// Status elements
const loading = document.getElementById("loading");
const errorText = document.getElementById("errorText");
const deviceInfo = document.getElementById("deviceInfo");

// ==================== STATE ====================
let selectedFile = null;
let isCameraRunning = false;
let cameraStream = null;
let classificationInterval = null;

// ==================== UTILITY FUNCTIONS ====================
const showError = (message) => {
  errorText.textContent = message;
  errorText.classList.remove("hidden");
};

const clearError = () => {
  errorText.textContent = "";
  errorText.classList.add("hidden");
};

const log = (prefix, message) => {
  console.log(`[${prefix}] ${message}`);
};

// ==================== MODE SWITCHING ====================
const switchSection = (section) => {
  homeSection.classList.add("hidden");
  featuresSection.classList.add("hidden");
  aboutSection.classList.add("hidden");
  
  homeLink.classList.remove("active");
  featuresLink.classList.remove("active");
  aboutLink.classList.remove("active");
  
  if (section === "home") {
    homeSection.classList.remove("hidden");
    homeLink.classList.add("active");
  } else if (section === "features") {
    featuresSection.classList.remove("hidden");
    featuresLink.classList.add("active");
  } else if (section === "about") {
    aboutSection.classList.remove("hidden");
    aboutLink.classList.add("active");
  }
};

homeLink.addEventListener("click", (e) => {
  e.preventDefault();
  switchSection("home");
});

featuresLink.addEventListener("click", (e) => {
  e.preventDefault();
  switchSection("features");
});

aboutLink.addEventListener("click", (e) => {
  e.preventDefault();
  switchSection("about");
});

// ==================== MODE SWITCHING ====================
uploadModeBtn.addEventListener("click", () => {
  uploadModeBtn.classList.add("active");
  liveModeBtn.classList.remove("active");
  uploadMode.classList.add("active");
  liveMode.classList.remove("active");
  clearError();
  
  // Stop camera if running
  if (isCameraRunning) {
    stopCameraFeed();
  }
});

liveModeBtn.addEventListener("click", () => {
  liveModeBtn.classList.add("active");
  uploadModeBtn.classList.remove("active");
  liveMode.classList.add("active");
  uploadMode.classList.remove("active");
  clearError();
});

// ==================== UPLOAD MODE FUNCTIONALITY ====================
const handleFile = (file) => {
  if (!file || !file.type.startsWith("image/")) {
    showError("Please upload a valid image file.");
    return;
  }

  clearError();
  selectedFile = file;

  const reader = new FileReader();
  reader.onload = (event) => {
    previewImage.src = event.target.result;
    previewWrap.classList.remove("hidden");
    resultCard.classList.add("hidden");
  };
  reader.readAsDataURL(file);
};

fileInput.addEventListener("change", (event) => {
  handleFile(event.target.files[0]);
});

dropZone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropZone.classList.remove("drag-over");
  handleFile(event.dataTransfer.files[0]);
});

classifyBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    showError("Please upload an image first.");
    return;
  }

  clearError();
  loading.classList.remove("hidden");
  resultCard.classList.add("hidden");

  try {
    const formData = new FormData();
    formData.append("image", selectedFile);

    const response = await fetch("/api/classify", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Classification failed");
    }

    resultIcon.textContent = "[R]";
    resultLabel.textContent = (data.label || "unknown").replace(/-/g, " ");
    resultCategory.textContent = data.category || "Unknown";
    resultConfidence.textContent = `${data.confidence}%`;
    resultTip.textContent = data.tip || "Sort correctly and follow local rules.";

    resultCard.classList.remove("hidden");
    log("UPLOAD", "Classification successful");
  } catch (error) {
    showError(error.message || "Something went wrong.");
    log("UPLOAD", `Error: ${error.message}`);
  } finally {
    loading.classList.add("hidden");
  }
});

// ==================== CAMERA MODE FUNCTIONALITY ====================
async function startCameraFeed() {
  try {
    log("CAMERA", "Requesting camera access...");
    
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 1280, max: 1920 },
        height: { ideal: 720, max: 1080 }
      },
      audio: false
    });

    log("CAMERA", "Stream obtained");
    cameraFeed.srcObject = cameraStream;

    // Check device name
    const tracks = cameraStream.getVideoTracks();
    if (tracks.length > 0) {
      const deviceLabel = tracks[0].label.toLowerCase();
      log("CAMERA", `Device: ${tracks[0].label}`);
      
      // Check if it's a remote device
      const remoteKeywords = ['phonelink', 'chromecast', 'cast', 'nest', 'remote', 'screencast'];
      const isRemote = remoteKeywords.some(keyword => deviceLabel.includes(keyword));
      
      if (isRemote) {
        log("CAMERA", "Remote device detected, switching to local camera");
        stopCameraFeed();
        
        // Enumerate and find local camera
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoCameras = devices.filter(d => d.kind === 'videoinput');
        
        if (videoCameras.length > 0) {
          // Try to find a local camera (skip the first if it's remote)
          let localCamera = videoCameras[0];
          for (let cam of videoCameras) {
            const label = cam.label.toLowerCase();
            if (!remoteKeywords.some(keyword => label.includes(keyword))) {
              localCamera = cam;
              break;
            }
          }
          
          cameraStream = await navigator.mediaDevices.getUserMedia({
            video: { deviceId: localCamera.deviceId },
            audio: false
          });
          cameraFeed.srcObject = cameraStream;
          log("CAMERA", `Using local device: ${localCamera.label}`);
        }
      }
    }

    isCameraRunning = true;
    startCameraBtn.classList.add("hidden");
    stopCameraBtn.classList.remove("hidden");
    resultCard.classList.add("hidden");
    
    // Start classification after video plays
    cameraFeed.onloadedmetadata = () => {
      log("CAMERA", "Video loaded and playing");
      setTimeout(startClassification, 500);
    };
    
  } catch (error) {
    if (error.name === "NotAllowedError") {
      showError("Camera permission denied. Please allow access.");
    } else if (error.name === "NotFoundError") {
      showError("No camera device found.");
    } else if (error.name === "NotReadableError") {
      showError("Camera is already in use or not accessible.");
    } else {
      showError(`Camera error: ${error.message}`);
    }
    log("CAMERA", `Error: ${error.message}`);
  }
}

function stopCameraFeed() {
  log("CAMERA", "Stopping camera");
  
  if (classificationInterval) {
    clearInterval(classificationInterval);
    classificationInterval = null;
  }
  
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }
  
  cameraFeed.srcObject = null;
  isCameraRunning = false;
  
  startCameraBtn.classList.remove("hidden");
  stopCameraBtn.classList.add("hidden");
  resultCard.classList.add("hidden");
}

function startClassification() {
  if (classificationInterval) {
    clearInterval(classificationInterval);
  }
  
  log("CAMERA", "Starting frame classification (1.5s interval)");
  classificationInterval = setInterval(classifyFrame, 1500);
}

async function classifyFrame() {
  if (!isCameraRunning || !cameraStream || cameraFeed.readyState !== cameraFeed.HAVE_ENOUGH_DATA) {
    return;
  }

  try {
    const ctx = captureCanvas.getContext("2d");
    captureCanvas.width = cameraFeed.videoWidth;
    captureCanvas.height = cameraFeed.videoHeight;
    
    ctx.drawImage(cameraFeed, 0, 0);
    
    const imageData = captureCanvas.toDataURL("image/jpeg", 0.7);
    
    const response = await fetch("/api/classify-frame", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageData })
    });

    const data = await response.json();
    
    if (response.ok) {
      resultIcon.textContent = "[R]";
      resultLabel.textContent = (data.label || "unknown").replace(/-/g, " ");
      resultCategory.textContent = data.category || "Unknown";
      resultConfidence.textContent = `${data.confidence}%`;
      resultTip.textContent = data.tip || "Sort correctly and follow local rules.";
      resultCard.classList.remove("hidden");
      
      log("CLASSIFICATION", `${data.label} (${data.confidence}%)`);
    } else {
      log("CLASSIFICATION", `Error: ${data.error}`);
    }
  } catch (error) {
    log("CLASSIFICATION", `Error: ${error.message}`);
  }
}

startCameraBtn.addEventListener("click", startCameraFeed);
stopCameraBtn.addEventListener("click", stopCameraFeed);

// ==================== INITIALIZATION ====================
document.addEventListener("DOMContentLoaded", () => {
  log("APP", "Initializing Earthify");
  
  // Detect device
  const userAgent = navigator.userAgent.toLowerCase();
  if (userAgent.includes("iphone") || userAgent.includes("ipad")) {
    deviceInfo.textContent = "iOS Device";
  } else if (userAgent.includes("android")) {
    deviceInfo.textContent = "Android Device";
  } else if (userAgent.includes("windows")) {
    deviceInfo.textContent = "Windows PC";
  } else if (userAgent.includes("mac")) {
    deviceInfo.textContent = "Mac OS";
  } else {
    deviceInfo.textContent = "Unknown Device";
  }
  
  log("APP", "Ready");
});
