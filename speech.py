from datetime import datetime
import io
import random
import boto3
import os
from pydub import AudioSegment


def text_to_speech(text, pause_duration="1s"):

    polly_client = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name="eu-west-1"
    ).client("polly")

    text = text.strip()

    ssml_text = f'<speak><break time="{pause_duration}"/>{text}</speak>'

    response = polly_client.synthesize_speech(
        Text=ssml_text,
        TextType="ssml",
        OutputFormat='pcm',
        VoiceId="Joanna"
    )

    audio_stream = response['AudioStream'].read()

    # Load the audio data into Pydub using the AudioSegment.from_file method
    pcm_audio = AudioSegment.from_file(io.BytesIO(audio_stream), format='raw', sample_width=2,
                                       channels=1, frame_rate=16000)

    # get length of audio file in seconds
    file_lenght = round(len(pcm_audio) / 1000)

    # random index for file name
    idx = random.randint(0, 1000)

    # Generate the output file name using the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = 'content/download/output_{}_{}.wav'.format(timestamp, idx)

    # Export the audio data to a WAV file using the export method
    pcm_audio.export(output_file, format='wav')
    return output_file, file_lenght
