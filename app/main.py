# app/main.py
import io
import pytesseract
# Import the concurrency tool from FastAPI
from fastapi.concurrency import run_in_threadpool
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
from pydantic import BaseModel
from .ai_services import restore_and_summarize_text # Keep this name

# --- App Configuration ---
app = FastAPI(
    title="StudySphere API",
    description="API for the AI-Powered Learning Hub, StudySphere.",
    version="0.1.0",
)

# --- Pydantic Models for Request Bodies ---
class SummarizeRequest(BaseModel):
    text: str

# ENDPOINT
@app.get("/")
def read_root():
    return {"message": "Welcome to the StudySphere API!"}


#OCR AN IMAGE
@app.post("/ocr/image/")
async def perform_ocr_on_image(image: UploadFile = File(...)):
    file_contents = await image.read()
    try:
        img = Image.open(io.BytesIO(file_contents))
        extracted_text = pytesseract.image_to_string(img)
        return {"filename": image.filename, "extracted_text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")

#SUMMARIZE A TEXT
@app.post("/summarize/")
async def get_summary(request: SummarizeRequest):
    summary = restore_and_summarize_text(request.text)
    return {"summary": summary}


#OCR TEXT RESTORER SUMMARY
@app.post("/process/image-to-summary/")
async def process_image_to_summary(image: UploadFile = File(...)):
    """
    takes in a image file to extract its text then feed it 
    to ai model to restore the messy words extracted by ocr 
    then use the model to make a concise and good summary of the 
    words extracted

    args:image
    returns:ai response text
    """
    
    
    
    
    # OCR EXTRACTOR
    file_contents = await image.read()
    try:
        img = Image.open(io.BytesIO(file_contents))
        extracted_text = pytesseract.image_to_string(img)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file provided: {e}")

    if len(extracted_text.strip()) < 20:
         raise HTTPException(
            status_code=400,
            detail="OCR failed to extract sufficient text from the image. Please use a clearer image."
        )

    #use the ai summary function and restore the ocr messy texts
    # in a separate thread to avoid blocking the main server.
    summary = await run_in_threadpool(restore_and_summarize_text, messy_text=extracted_text)

    #return
    return {
        "filename": image.filename,
        "extracted_text": extracted_text,
        "summary": summary
    }
    