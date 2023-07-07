import logging
import os
from pytube import YouTube
from pathlib import Path


async def download_youtube_video(update, context):
    """Youtube video download handler."""
    logging.info("download_youtube_video provoked.")
    try:
        # Download the YouTube video
        video_url = update.message.text
        video = YouTube(video_url)
        stream = video.streams.get_highest_resolution()

        # Create the directory to save the video
        data_path = "/data/youtube_downloads/"
        os.makedirs(data_path, exist_ok=True)

        output_filename = video.title + ".mp4"

        stream.download(output_path=data_path, filename=output_filename, timeout=700)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Downloading video...")
        logging.info(f"video {video.title} saved in file path:{data_path}")
        video_path = os.path.join(data_path, output_filename)
        chat_id = update.effective_chat.id
        await context.bot.send_video(chat_id=chat_id, video=open(video_path, 'rb'))
        Path(video_path).unlink()
        logging.info(f"video path {video_path} unlinked!")
        return
    except Exception as e:
        logging.exception(f"Error downloading YouTube video: {str(e)}")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"An error occurred while downloading the YouTube video. Please ensure that the provided link is correct and try again.")
        return None


async def youtube_command(update, context):
    """YouTube command. """
    logging.info("YouTube command provoked.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send the youtube link and i will send you the video.")
