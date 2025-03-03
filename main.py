from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
import requests
import base64
import os

app = FastAPI()

@app.post("/generate-audio")
async def generate_audio(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Text input is required")
    
    output_file = text_to_speech(text)
    if output_file:
        return FileResponse(output_file, media_type="audio/wav", filename="output_audio.wav")
    else:
        raise HTTPException(status_code=500, detail="Failed to generate audio")

def text_to_speech(text: str):
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {
        "API-Subscription-Key": os.getenv("SARVAM_API_KEY"),
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": [text],
        "target_language_code": "hi-IN",
        "speaker": "meera",
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        audio_base64 = response.json()["audios"][0]
        audio_bytes = base64.b64decode(audio_base64)
        output_filename = "output_audio.wav"
        with open(output_filename, "wb") as audio_file:
            audio_file.write(audio_bytes)
        return output_filename
    return None


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
