import azure.cognitiveservices.speech as speechsdk
import simpleaudio as sa
import threading
import time

audio_done = False

def play_audio():
    global audio_done
    try:
        wave_obj = sa.WaveObject.from_wave_file("audio.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print(f"Error al reproducir el audio: {e}")
    finally:
        audio_done = True

def recognize_and_display_clean():
    speech_key = "7opGrVMoUxOueY9o2EpAdkhCwdWgwz87M8xRFLzhL2kZO6Vfq7d6JQQJ99BEACYeBjFXJ3w3AAAYACOGeWDb"
    service_region = "eastus"

    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_input = speechsdk.AudioConfig(filename="audio.wav")

        # 🔍 Auto detección entre inglés y español
        auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=["en-US", "es-MX"]
        )

        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_input,
            auto_detect_source_language_config=auto_detect_config
        )

        recognition_done = False
        recognized_phrases = set()
        full_transcription = ""
        detected_language = None

        def stop_cb(evt):
            nonlocal recognition_done
            recognition_done = True

        def recognizing_cb(evt):
            pass

        def recognized_cb(evt):
            nonlocal full_transcription, detected_language
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                if not detected_language:
                    detected_language = evt.result.properties.get(
                        speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult)
                    print(f"Idioma detectado: {detected_language}")

                new_text = evt.result.text.strip()
                if new_text and new_text not in recognized_phrases:
                    print(new_text)
                    recognized_phrases.add(new_text)
                    full_transcription += new_text + " "

        recognizer.recognizing.connect(recognizing_cb)
        recognizer.recognized.connect(recognized_cb)
        recognizer.session_stopped.connect(stop_cb)
        recognizer.canceled.connect(stop_cb)

        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()

        print("Detectando idioma y transcribiendo...\n")
        recognizer.start_continuous_recognition()

        while not (recognition_done and audio_done):
            time.sleep(0.1)

        recognizer.stop_continuous_recognition()
        audio_thread.join()

        # Guardar resultado
        with open("transcripcion.txt", "w", encoding="utf-8") as f:
            f.write(full_transcription.strip())

        print("\nTranscripción guardada en 'transcripcion.txt'.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    recognize_and_display_clean()
