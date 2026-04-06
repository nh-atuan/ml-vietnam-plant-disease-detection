from fastapi import FastAPI, File, UploadFile
import torch
from PIL import Image
import io
from torchvision import transforms
from src.models.model_factory import AdvancedModel, load_model

app = FastAPI(title="Plant Disease Detection API")

# Load model globally
DEVICE = "cpu"
NUM_CLASSES = 10 # Example
model = AdvancedModel(num_classes=NUM_CLASSES)
# model = load_model(model, "models/best_model/model.pth", device=DEVICE)
model.eval()

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        confidence, class_idx = torch.max(probabilities, 0)
        
    return {
        "class_id": int(class_idx),
        "confidence": float(confidence),
        "disease": "Example Disease" # Map to actual name
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
