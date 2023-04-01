from dotenv import load_dotenv
from moviepy.editor import *
from generate import generate_prompt

from image import get_image
from speech import text_to_speech

# Load environment variables from .env file
load_dotenv()


def generate_audio(descriptions: list[str], duration: int = 5):

    silent_audio = AudioClip(
        lambda t: 0, duration=duration)

    lenghts_in_seconds = []
    files = []
    # loop through descriptions and generate audio
    for i in range(len(descriptions)):
        file, lenght_in_seconds = text_to_speech(descriptions[i])
        lenghts_in_seconds.append(lenght_in_seconds)
        files.append(file)

    # Join audio files, add silence between them
    # reverse the list so that the first audio file is at the end
    files.reverse()
    audioFiles = [AudioFileClip(f) for f in files]
    withSilence = [audioFiles[0]]
    for i in range(1, len(audioFiles)):
        withSilence.append(silent_audio)
        withSilence.append(audioFiles[i])

    transcript_sound_file = concatenate_audioclips(withSilence)

    background_sound_file = "content/static/background.wav"

    # Load background sound
    backgroundAudio = AudioFileClip(background_sound_file)
    # lower the volume of background sound
    backgroundAudio = backgroundAudio.volumex(0.2)

    # Concatenate background and transcript sounds
    # Mix background and transcript sounds
    finalAudio = CompositeAudioClip([backgroundAudio, transcript_sound_file])
    # generate audio
    return (finalAudio, lenghts_in_seconds)


def calculate_font_size(caption, max_width, min_font_size=20, max_font_size=50):
    font_size = max_font_size
    while TextClip(caption, fontsize=font_size, method='caption', print_cmd=True, size=(max_width, None)).size[0] > max_width and font_size > min_font_size:
        font_size -= 1
    return font_size


def generate_images(names):
    # generate images
    image_files = []
    for i in range(len(names)):
        image_url = get_image(names[i])
        if image_url:
            image_files.append(image_url)
        else:
            print("Error getting image url, exiting...")
            return
    return image_files


def main():
    # ask user to input a prompt
    prompt = input(
        "Enter what would you like to get video about (5 biggest cities in the world): ")

    if not prompt:
        print("You must enter a prompt!")
        prompt = "5 animals with biggest dicks"
        print(f"Using default prompt: {prompt}")

    # get content from openai api
    content = generate_prompt(prompt)
    # content = [('1. Blue whale', 'The blue whale has the largest penis of any animal. It is typically 12–16 metres long, but has been known to grow to lengths of 33 metres.'), ('2. Elephant', 'The elephant has the second largest penis of any land animal. The penis is typically 6–7 metres long and 1.5 metres in diameter.'), ('3. Giraffe',
   #                                                                                                                                                                                                                                                                                                                                   'The giraffe has the third largest penis of any land animal. The penis is typically 4–5 metres long and 0.5 metres in diameter.'), ('4. Rhinoceros', 'The rhinoceros has the fourth largest penis of any land animal. The penis is typically 3–4 metres long and 0.5 metres in diameter.'), ('5. Hippopotamus', 'The hippopotamus has the fifth largest penis of any land animal. The penis is typically 2–3 metres long and 0.5 metres in diameter.')]

    print(content)
    # ask user if they want to continue
    if input("Do you want to continue? (y/n): ") != "y":
        print("Exiting...")
        return

    names = list(map(lambda x: x[0].strip(), content))
    descriptions = list(map(lambda x: f"{x[0]} {x[1]}".strip(), content))

    # add intro text
    intro_text = f"Here we are, lets get blown by stuff!"
    descriptions.insert(0, intro_text)

    transition_time = 2

    # generate audio
    finalAudio, section_durations = generate_audio(
        descriptions, transition_time)

    # get images from unsplash api
    image_files = generate_images(names)
    if not image_files:
        return

    # create video
    # Process images and captions
    clips = []
    # Video settings
    image_size = (1920, 1080)  # width, height

    # Add start image
    start_image = ImageClip(
        "content/static/blown.jpeg").resize(image_size).set_duration(section_durations[0])

    # Add start text
    start_text = TextClip(f"Are you ready to get blown?", fontsize=50, color='white', bg_color='black', size=(
        image_size[0], 70)).set_duration(section_durations[0])
    start_text = start_text.set_position(("center", "center")).set_opacity(0.5)

    start_clip = CompositeVideoClip(
        [start_image, start_text])

    for index, (img, duration_per_image) in enumerate(zip(image_files, section_durations[1:]), start=1):

        # Load wait image
        wait_img = ImageClip("content/static/wait.jpg").resize(
            image_size).set_duration(transition_time)

        # Add consecutive number
        num_clip = TextClip(f"Number {index}!", fontsize=50, color='white', bg_color='black', size=(
            300, 80)).set_duration(transition_time+duration_per_image)
        num_clip = num_clip.set_position(("center", "center")).set_opacity(0.5)

        # Load image and resize
        img_clip = ImageClip(img).resize(image_size).set_duration(
            duration_per_image).set_start(transition_time)

        img_with_caption = CompositeVideoClip(
            [wait_img, img_clip, num_clip])

        clips.append(img_with_caption)

    clips.append(start_clip)
    clips.reverse()
    # Concatenate clips and set audio
    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_audio(
        finalAudio.set_duration(final_clip.duration))

    # Export the final video
    final_clip.write_videofile(
        "output_video.mp4", codec="libx264", audio_codec="aac", fps=5)


main()
