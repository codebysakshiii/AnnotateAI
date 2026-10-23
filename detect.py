
from ultralytics import YOLO

print("Loading AI model...")

# Load pretrained YOLO model
model = YOLO("yolo11n.pt")

print("AI model loaded successfully!")
print("Detecting objects in the sample image...")

# Download and analyze a sample image
results = model.predict(
    source="https://ultralytics.com/images/bus.jpg",
    save=True,
    conf=0.25
)

# Display detected objects
for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        name = result.names[class_id]
        confidence = float(box.conf[0])

        print(f"Object: {name} | Confidence: {confidence:.2%}")

print("\nDetection complete!")
print("Check the runs/detect folder for the output image.")