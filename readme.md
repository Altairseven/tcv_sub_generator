# Subtitle Generator

For our **Spanish (Latin American) D&D channel, "Tira con Ventaja"**, we needed a solution to quickly generate subtitles for social media video clips. This tool was created to simplify the process by automating subtitle creation. After generating subtitles, the output can later undergo **human revision**, ensuring accuracy and readability for our audience.

---

## Description

This script automates the process of subtitle generation by leveraging:
1. **FFmpeg**: Extracts audio from `.mp4` video files.
2. **OpenAI Whisper**: Transcribes the audio into subtitles, generating a formatted `.srt` file.

The script processes each video from an input folder, generates subtitles, moves the videos and subtitles to the output folder, and cleans up temporary files created during processing.

---

## Usage

The script requires two folder paths as arguments: 
- **Input Folder**: Directory containing the `.mp4` video files to be processed.
- **Output Folder**: Directory where the subtitles (`.srt` files) and processed videos will be saved.

### Command Example

Run the script with relative paths like so:

```bash
python generate_subtitles.py ./input ./output
```

### What Happens
1. The script extracts the audio from each `.mp4` file in the **input folder**.
2. The audio is transcribed into subtitles and saved as `.srt` files in the **output folder**.
3. The original videos are moved to the **output folder**.
4. Temporary audio files are deleted after processing.

---

## Requirements

1. **FFmpeg**: 
   - FFmpeg must be installed and added to your PATH for the script to work.
   - [Download FFmpeg here](https://ffmpeg.org/download.html).

2. **Python Libraries**:
   - Install the required libraries using the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

## About "Tira con Ventaja" [![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://www.youtube.com/@TiraConVentaja) [![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/tiraconventaja/) [![TikTok](https://img.shields.io/badge/TikTok-000000?style=flat&logo=tiktok&logoColor=white)](https://www.tiktok.com/@tira.con.ventaja)![Argentina](https://img.shields.io/badge/Argentina-%F0%9F%87%A6%F0%9F%87%B7-blue)





**Tira con Ventaja** is an Youtube channel from Argentina that produces Dungeons & Dragons content. This tool was developed as part of our effort to improve content accessibility and engagement on social media. By creating subtitles for short video clips, we ensure our content reaches a wider audience quickly and efficiently.
