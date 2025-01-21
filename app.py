from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import os

app = Flask(__name__)
CORS(app)
load_dotenv()
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process-audio", methods=["POST"])
def process_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files["audio"]
    file_path = f"temp_audio.wav"
    audio_file.save(file_path)

    # Optional: Convert audio to WAV format if needed
    sound = AudioSegment.from_file(file_path)
    sound.export(file_path, format="wav")

    # Use OpenAI's Whisper API to transcribe the audio
    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    os.remove(file_path)

    # Translate transcription to fun "cat language"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a fun translator for cat sounds."},
            {"role": "user", "content": f"What does this cat say? {transcription.text}"}
        ]
    )
    translation = response.choices[0].message.content
    print(translation)
    return jsonify({"translation": translation})

if __name__ == "__main__":
    app.run(host="0.0.0.1", debug=True)
