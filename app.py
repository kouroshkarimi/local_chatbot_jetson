import sys
import requests
import argparse
import riva.client
import riva.client.audio_io


class ArgsASR():
    def __init__(self) -> None:
        self.input_device = 25
        self.list_devices = False
        self.profanity_filter = False
        self.automatic_punctuation = False
        self.no_verbatim_transcripts = False
        self.language_code = "en-US"
        self.boosted_lm_words = None
        self.boosted_lm_score = 4.0
        self.speaker_diarization = False
        self.server = "localhost:50051"
        self.ssl_cert = None
        self.use_ssl = False
        self.metadata = None
        self.sample_rate_hz = 16000
        self.file_streaming_chunk = 1600


class ArgsTTS():
    def __init__(self) -> None:
        self.language_code = 'en-US'
        self.sample_rate_hz = 48000
        self.stream = True
        self.output_device = 30


class ChatBot():
    def __init__(self, args) -> None:

        if args.list_input_devices:
            riva.client.audio_io.list_input_devices()
            sys.exit()
        if args.list_output_devices:
            riva.client.audio_io.list_output_devices()
            sys.exit()

        self.args_asr = ArgsASR()
        self.args_tts = ArgsTTS()
        self.args_asr.input_device = args.input_device
        self.args_tts.output_device = args.output_device

        auth = riva.client.Auth(uri=self.args_asr.server)
        self.asr_service = riva.client.ASRService(auth)
        self.tts_service = riva.client.SpeechSynthesisService(auth)

        self.config_asr = riva.client.StreamingRecognitionConfig(
            config=riva.client.RecognitionConfig(
                encoding=riva.client.AudioEncoding.LINEAR_PCM,
                language_code=self.args_asr.language_code,
                max_alternatives=1,
                profanity_filter=self.args_asr.profanity_filter,
                enable_automatic_punctuation=self.args_asr.automatic_punctuation,
                verbatim_transcripts=not self.args_asr.no_verbatim_transcripts,
                sample_rate_hertz=self.args_asr.sample_rate_hz,
                audio_channel_count=1,
            ),
            interim_results=True,
        )

        riva.client.add_word_boosting_to_config(
            self.config_asr, 
            self.args_asr.boosted_lm_words, 
            self.args_asr.boosted_lm_score
            )

        self.flag_wakeup = False

    def output_audio(self, answer):
        sound_stream = None
        try:
            if self.args_tts.output_device is not None:
                # For playing audio during synthesis you will need to pass audio chunks to riva.
                # client.audio_io.SoundCallBack as they arrive.
                sound_stream = riva.client.audio_io.SoundCallBack(
                    self.args_tts.output_device, nchannels=1, sampwidth=2,
                    framerate=self.args_tts.sample_rate_hz
                )
            if self.args_tts.stream:
                responses1 = self.tts_service.synthesize_online(
                    answer, None, self.args_tts.language_code, 
                    sample_rate_hz=self.args_tts.sample_rate_hz
                )
                for resp in responses1:    
                    if sound_stream is not None:
                        sound_stream(resp.audio)
        finally:
            if sound_stream is not None:
                sound_stream.close()
    
    def run(self):
        output_asr = ""
        while True:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            with riva.client.audio_io.MicrophoneStream(
                    self.args_asr.sample_rate_hz,
                    self.args_asr.file_streaming_chunk,
                    device=self.args_asr.input_device,
                ) as stream_mic:
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                try:
                    for response in self.asr_service.streaming_response_generator(
                            audio_chunks=stream_mic,
                            streaming_config=self.config_asr,
                    ):  # Here is a continuous listening loop
                        for result in response.results:
                            if result.is_final:
                                transcripts = result.alternatives[0].transcript
                                output_asr = transcripts
                            if output_asr != "":
                                if "hello" in output_asr:
                                    self.flag_wakeup = True
                                    self.output_audio('Here!')
                                    output_asr = ""
                                    stream_mic.close()
                                if "stop" in output_asr and self.flag_wakeup:
                                    self.flag_wakeup = False
                                    self.output_audio('Bye! Have a great day!')
                                    output_asr = ""
                                    stream_mic.close()
                                if self.flag_wakeup and self.isinstance(output_asr):
                                    print(f'User Input: >>>>>\n {output_asr} \n')
                                    stream_mic.close()

                                    headers = {"Content-Type": "application/json",}
                                    data = {
                                        'inputs': output_asr,
                                        'parameters': {
                                            'max_new_tokens': 50,
                                        },
                                    }
                                    response = requests.post(
                                        'http://192.168.49.74:8899/generate', headers=headers, json=data
                                        )
                                    result = response.json()['generated_text']
                                    print(f'ChatBot Output: >>>>>\n {result} \n')
                                    self.output_audio(result)
                                    output_asr = ""
                finally:
                    pass

    @staticmethod
    def isinstance(text, min_length=5, min_unique_words=1):
        text = text.strip()

        if len(text) < min_length:
            return False

        words = text.split()
        unique_words = set(words)
        if len(unique_words) < min_unique_words:
            return False

        return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="",)
    parser.add_argument("--list-input-devices", action="store_true", help="List input audio device indices.")
    parser.add_argument("--list-output-devices", action="store_true", help="List input audio device indices.")
    parser.add_argument("--input-device", type=int, default=25, help="Set input audio device.")
    parser.add_argument("--output-device", type=int, default=30, help="Set output audio device.")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    chatbot = ChatBot(args)
    chatbot.run()