import azure.cognitiveservices.speech as speechsdk
import time

def recognize_from_microphone():
    # Azure subscription info
    speech_key = "7opGrVMoUxOueY9o2EpAdkhCwdWgwz87M8xRFLzhL2kZO6Vfq7d6JQQJ99BEACYeBjFXJ3w3AAAYACOGeWDb"
    service_region = "eastus"

    try:
        # Configuración de reconocimiento y micrófono
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_input = speechsdk.AudioConfig(use_default_microphone=True)

        # Autodetección de idioma: español e inglés
        auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=["en-US", "es-MX"]
        )

        # Reconocedor de voz
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_input,
            auto_detect_source_language_config=auto_detect_config
        )

        recognition_done = False
        detected_language = None
        recognized_text = ""

        def stop_cb(evt):
            nonlocal recognition_done
            recognition_done = True

        def recognized_cb(evt):
            nonlocal detected_language, recognized_text
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                if not detected_language:
                    detected_language = evt.result.properties.get(
                        speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult)
                    print(f"\n🗣 Detected language: {detected_language}")

                text = evt.result.text.strip()
                if text:
                    print(f"📝 {text}")
                    recognized_text += text + " "

        # Conectar eventos
        recognizer.recognized.connect(recognized_cb)
        recognizer.session_stopped.connect(stop_cb)
        recognizer.canceled.connect(stop_cb)

        print("🎙 Empieza a hablar... (presiona Ctrl+C para detener)\n")
        recognizer.start_continuous_recognition()

        try:
            while not recognition_done:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n⏹ Reconocimiento detenido por el usuario.")
            recognizer.stop_continuous_recognition()

        # Guardar transcripción
        output_path = "/Users/steef/Desktop/azure_speech_demo/transcripcion.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(recognized_text.strip())

        print(f"\n✅ Transcripción guardada en: {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    recognize_from_microphone()
