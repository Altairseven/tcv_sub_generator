"""Script para generar subtítulos de clips para Tira con Ventaja"""
import os
import sys
import subprocess
import shutil
import whisper

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
MODEL_DOWNLOAD_PATH = os.path.join(SCRIPT_FOLDER, "model_data")
TEMP_FOLDER = os.path.join(SCRIPT_FOLDER, "temp")

def list_mp4_files(input_folder: str) -> list:
    """Lists all .mp4 files in the input folder."""
    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        return []

    file_list = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]
    if not file_list:
        print(f"No .mp4 files found in the input folder: {input_folder}")
    return file_list


def extract_audio(input_folder: str, file_name: str) -> str:
    """Extracts audio from an .mp4 file and saves it as a .wav file in the temp folder."""
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    input_path = os.path.join(input_folder, file_name)
    temp_file_name = os.path.splitext(file_name)[0] + ".wav"
    temp_file_path = os.path.join(TEMP_FOLDER, temp_file_name)

    print(f"Extracting audio from: {file_name}")
    ffmpeg_command = [
        "ffmpeg",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        temp_file_path,
        "-y"
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Audio extracted to: {temp_file_path}")
        return temp_file_path
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio from {file_name}: {e}")
        return None

def format_as_srt(result):
    """Converts Whisper transcription result into SRT format."""
    srt_output = []
    for i, segment in enumerate(result["segments"]):
        start_time = format_time(segment["start"])
        end_time = format_time(segment["end"])
        text = segment["text"].strip()

        srt_output.append(f"{i + 1}")
        srt_output.append(f"{start_time} --> {end_time}")
        srt_output.append(text)
        srt_output.append("")  # Blank line between entries

    return "\n".join(srt_output)


def format_time(seconds):
    """Formats time in seconds to SRT timestamp (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def generate_subtitle(wav_file: str, output_folder: str, model):
    """Generates subtitles for a .wav file and saves it in the output folder."""
    print(f"Generating subtitles for: {wav_file}")

    result = model.transcribe(
        audio=wav_file,
        language="es",                # Specify the language as Spanish
        # word_timestamps=True,         # Enable word-level timestamps
        # max_line_width=20             # Set max line width for subtitles
    )

    srt_content = format_as_srt(result)

    base_name = os.path.splitext(os.path.basename(wav_file))[0]
    output_file = os.path.join(output_folder, f"{base_name}.srt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(srt_content)

    print(f"Subtitles saved to: {output_file}")


def move_file(source_path: str, dest_folder: str):
    """Moves a file to the destination folder."""
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest_path = os.path.join(dest_folder, os.path.basename(source_path))
    shutil.move(source_path, dest_path)
    print(f"Moved file to: {dest_path}")


def cleanup_file(file_path: str):
    """Removes a file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted temporary file: {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")


def main(input_folder: str, output_folder: str):
    """Runs the main process."""
    # List all source .mp4 files
    file_list = list_mp4_files(input_folder)
    if not file_list:
        return

    # Load the Whisper model once
    model = whisper.load_model("large", download_root=MODEL_DOWNLOAD_PATH)
    print("Whisper model loaded.")

    for file_name in file_list:
        print(f"Processing file: {file_name}")

        # 1. Extract audio to .wav
        wav_file = extract_audio(input_folder, file_name)
        if not wav_file:
            continue  # Skip this file if audio extraction failed

        # 2. Generate subtitles
        generate_subtitle(wav_file, output_folder, model)

        # 3. Move the source .mp4 file to the output folder
        source_mp4_path = os.path.join(input_folder, file_name)
        move_file(source_mp4_path, output_folder)

        # 4. Remove the .wav file from the temp folder
        cleanup_file(wav_file)

    print("Processing complete.")


if __name__ == "__main__":
    # Check if correct arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python tcv_subs.py <inputFolder> <outputFolder>")
        sys.exit(1)

    # Get the folder paths from arguments
    in_folder = sys.argv[1]
    out_folder = sys.argv[2]

    main(in_folder, out_folder)
