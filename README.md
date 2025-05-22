Azure Speech Demo (Bilingual)

🎤 Overview | Descripción

This project is a bilingual (English/Spanish) demo using Azure Cognitive Services to:

🔊 Convert speech to text from a .wav audio file

🎧 Automatically detect whether the audio is in English or Spanish

🎙️ Play the audio while transcribing

♻️ No time limit on audio playback

Features | Características

✅ Real-time transcription with language detection

✅ Unlimited playback duration

✅ Clean transcript output with duplicates removed

✅ Multithreading for simultaneous audio playback and transcription

🚫 Files Ignored | Archivos Ignorados

Included in .gitignore:

.venv/
__pycache__/
*.pyc
audio.wav
transcripcion.txt
*.env

🚧 Requirements | Requisitos

Install dependencies:

pip install -r requirements.txt

🔐 Azure Setup | Configuración de Azure

Create an account at: https://portal.azure.com

Create a Speech resource

Copy your Subscription Key and Region

(Optional) Store them in a .env file:

▶️ How to Use | Cómo Usar

python speech_to_text.py

The audio will play while it is being transcribed. Once complete, the transcript is saved in transcripcion.txt.

👤 Author | Autor

Created by [Estefania Rosas] in 2025.
