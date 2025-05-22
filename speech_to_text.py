import azure.cognitiveservices.speech as speechsdk  # Azure Speech SDK
import simpleaudio as sa  # For audio playback
import threading  # To run audio playback in parallel
import time  # For delays

audio_done = False  # Flag to track when audio finishes playing

def play_audio():
    global audio_done
    try:
        wave_obj = sa.WaveObject.from_wave_file("audio.wav")  # Load audio file
        play_obj = wave_obj.play()  # Play audio
        play_obj.wait_done()  # Wait until done
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        audio_done = True  # Mark audio as done

def recognize_and_display_clean():
    # Azure subscription info
    speech_key = "7opGrVMoUxOueY9o2EpAdkhCwdWgwz87M8xRFLzhL2kZO6Vfq7d6JQQJ99BEACYeBjFXJ3w3AAAYACOGeWDb"
    service_region = "eastus"

    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_input = speechsdk.AudioConfig(filename="audio.wav")  # Input audio file

        # Auto detect English and Spanish languages
        auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=["en-US", "es-MX"]
        )

        # Create speech recognizer with auto language detection
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_input,
            auto_detect_source_language_config=auto_detect_config
        )

        recognition_done = False
        recognized_phrases = set()  # To avoid duplicates
        full_transcription = ""
        detected_language = None

        def stop_cb(evt):
            nonlocal recognition_done
            recognition_done = True  # Stop when recognition ends

        def recognizing_cb(evt):
            pass  # Can handle interim results here

        def recognized_cb(evt):
            nonlocal full_transcription, detected_language
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                if not detected_language:
                    # Get detected language first time
                    detected_language = evt.result.properties.get(
                        speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult)
                    print(f"Detected language: {detected_language}")

                new_text = evt.result.text.strip()
                if new_text and new_text not in recognized_phrases:
                    print(new_text)  # Print recognized text
                    recognized_phrases.add(new_text)
                    full_transcription += new_text + " "  # Append to full text

        # Connect callbacks
        recognizer.recognizing.connect(recognizing_cb)
        recognizer.recognized.connect(recognized_cb)
        recognizer.session_stopped.connect(stop_cb)
        recognizer.canceled.connect(stop_cb)

        # Start audio playback in background thread
        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()

        print("Detecting language and transcribing...\n")
        recognizer.start_continuous_recognition()  # Start recognition

        # Wait until both recognition and audio finish
        while not (recognition_done and audio_done):
            time.sleep(0.1)

        recognizer.stop_continuous_recognition()
        audio_thread.join()

        # Save full transcription to file
        with open("transcripcion.txt", "w", encoding="utf-8") as f:
            f.write(full_transcription.strip())

        print("\nTranscription saved to 'transcripcion.txt'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    recognize_and_display_clean()
