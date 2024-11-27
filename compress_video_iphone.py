import os
import subprocess
from tqdm import tqdm

def compress_video(input_file, output_file, resolution="640x360", video_bitrate="500k", audio_bitrate="128k"):
    """
    Compress a video file using FFmpeg with a specified resolution, video bitrate, and audio bitrate.
    Ensures the output is compatible with iPhones by using H.264 video codec and AAC audio codec.
    """
    try:
        # Build the FFmpeg command for compression
        command = [
            "ffmpeg", "-i", input_file,  # Input file
            "-vf", f"scale={resolution}",  # Scale resolution
            "-b:v", video_bitrate,  # Set video bitrate
            "-b:a", audio_bitrate,  # Set audio bitrate
            "-acodec", "aac",  # Audio codec set to AAC (iPhone compatible)
            "-vcodec", "libx264",  # Video codec set to H.264 (iPhone compatible)
            "-preset", "ultrafast",  # Set encoding speed (ultrafast = fastest, least compression)
            "-movflags", "+faststart",  # Optimize the file for streaming (important for iPhone)
            "-y",  # Overwrite output file if it exists
            output_file  # Output file
        ]
        
        # Run the command
        subprocess.run(command, check=True)
        print(f"Video successfully compressed and saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during video compression: {e}")

def process_directory(video_folder, output_folder, resolution="640x360", video_bitrate="500k", audio_bitrate="128k"):
    """
    Process all video files in the specified folder, compressing each and saving the result to the output folder.
    The output files will be iPhone-compatible (MP4 with H.264 and AAC).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all video files in the folder (filter for common video formats)
    video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".mkv", ".avi", ".mov"))]

    # Use tqdm for progress bar
    for filename in tqdm(video_files, desc="Compressing videos", unit="file"):
        # Define full input and output file paths
        input_file = os.path.join(video_folder, filename)
        output_file = os.path.join(output_folder, f"compressed_{filename}.mp4")

        # Compress the video
        compress_video(input_file, output_file, resolution, video_bitrate, audio_bitrate)

# Example usage
video_folder = "Videos"  # Folder where video files are stored
output_folder = "Compressed_Videos"  # Folder where compressed videos will be saved
process_directory(video_folder, output_folder)
