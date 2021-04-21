import azure.cognitiveservices.speech as speechsdk
import argparse
from translate import Translator

# Command line options
parser = argparse.ArgumentParser()
parser.add_argument('--audio_file', type=str, default="",
                    help='An audio file to extract text from.')
parser.add_argument('--target_lang', type=str, default="english",
                    help='Language to convert text to.')
args = parser.parse_args()

# In order for the code to run, you'll need to enter the key and region from your own Azure Cognitive Services resource
speech_key, service_region = "<your_key>", "your_region"
auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "es-ES", "fr-CA"])
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Either use microphone or audio file if specified
if args.audio_file == "":
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
else:
        audio_config = speechsdk.audio.AudioConfig(filename=args.audio_file)

speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        auto_detect_source_language_config=auto_detect_source_language_config,
        audio_config=audio_config)
result = speech_recognizer.recognize_once()


# Print out the results
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(result)
        detected_language = auto_detect_source_language_result.language
        lang_dict = {"en-US": "english", "es-ES": "spanish", "fr-CA": "french"}
        detected_language = lang_dict[detected_language]
        print('Detected Language: ', detected_language)
        translator = Translator(from_lang=detected_language, to_lang=args.target_lang)
        print("Translated Text: ", translator.translate(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

