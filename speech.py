from datetime import datetime
import io
import boto3
from pydub import AudioSegment


def text_to_speech(text, pause_duration="1s"):

    polly_client = boto3.Session(
        aws_access_key_id="AKIAUWIH62LHSMHLHX2X",
        aws_secret_access_key="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",
        region_name="eu-west-1"
    ).client("polly")

    # Insert a pause between each sentence
    sentences = text.split(". ")

    # filter out empty sentences or sentences with only spaces
    sentences = list(filter(lambda x: x.strip(), sentences))

    ssml_text = '<speak>' + \
        f'<break time="{pause_duration}"/>'.join(sentences) + '</speak>'

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
    file_lenght = (len(pcm_audio) / 1000)

    # Generate the output file name using the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = 'content/download/output_{}.wav'.format(timestamp)

    # Export the audio data to a WAV file using the export method
    pcm_audio.export(output_file, format='wav')
    return output_file, file_lenght
