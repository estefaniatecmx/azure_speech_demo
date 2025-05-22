import azure.cognitiveservices.speech as speechsdk

def text_to_speech():
     # Azure key and region
    speech_key = "7opGrVMoUxOueY9o2EpAdkhCwdWgwz87M8xRFLzhL2kZO6Vfq7d6JQQJ99BEACYeBjFXJ3w3AAAYACOGeWDb"
    service_region = "eastus"
    # Setup speech config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Select Mexican Spanish voice
    speech_config.speech_synthesis_voice_name = "es-MX-DaliaNeural"

    # Audio output config (default voice)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
    # Text to speak
    text = "Hola Instagram buenas noches este es un demo de NLP como mi primer extraccion de texto a voz, ADIOS LOS AMO BYEEE"
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(" Voz generada con éxito.")
      # Handle errors   
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f" Error: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Detalles: {cancellation_details.error_details}")

if __name__ == "__main__":
    text_to_speech()
