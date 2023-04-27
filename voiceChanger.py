import io
import logging
from pydub import AudioSegment
from telegram import Update
from telegram.ext import ContextTypes


async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Audio handler for voice messages received. """
    logging.info("Audio handler provoked.")
    # Download the audio file
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    audio_bytes = io.BytesIO(await voice_file.download_as_bytearray())

    # Pitch up the audio
    octaves = -0.7
    audio_file = AudioSegment.from_file(audio_bytes, format='ogg')
    new_sample_rate = int(audio_file.frame_rate * (2.0 ** octaves))
    hipitch_sound = audio_file._spawn(audio_file.raw_data, overrides={'frame_rate': new_sample_rate})
    hipitch_sound = hipitch_sound.set_frame_rate(44100)

    # Convert the audio to bytes and then to MP3
    output_bytes = io.BytesIO()
    hipitch_sound.export(output_bytes, format='mp3')
    output_bytes.seek(0)
    mp3_audio_bytes = io.BytesIO()
    AudioSegment.from_file(output_bytes).export(mp3_audio_bytes, format='mp3')

    # Send the MP3 audio file back to the user
    mp3_audio_bytes.seek(0)
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=mp3_audio_bytes, title='hipitched_audio.mp3')


###   Samples created with different octaves value ##
# for octaves in numpy.linspace(-1,1,21):
#     new_sample_rate = int(audio_file.frame_rate * (2.0 ** octaves))
#     hipitch_sound = audio_file._spawn(audio_file.raw_data, overrides={'frame_rate': new_sample_rate})
#     hipitch_sound = hipitch_sound.set_frame_rate(44100)
# #export / save pitch changed sound
#     hipitch_sound.export(f"sample-2.mp3_{octaves}.wav", format="wav")