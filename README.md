# BlueSky Video Downloader

## Description

A Python-based command line tool to download the videos posted on a BlueSky profile.

## Usage

### Clone the Repository

```bash
git clone https://github.com/ABojo/bsky-video-downloader
cd bsky-video-downloader
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Usage

```bash
python bsky_video_downloader.py username [options]
```

### Options

- `-f, --folder`: Specify the folder to place the videos in.
- `-t, --threads`: Set the number of threads. The default is 3.
- `-l, --limit`: Limit the number of videos that will be downloaded.
- `-s, --start-date`: Videos before this day will not be downloaded. (MM-DD-YYYY)
- `-e, --end-date`: Videos after this day will not be downloaded. (MM-DD-YYYY)

### Examples

```bash
# Download all videos from a user
python bsky_video_downloader.py username

# Download videos to a specific folder
python bsky_video_downloader.py username -f ./videos

# Download 10 videos and use 5 threads
python bsky_video_downloader.py username -l 10 -t 5

# Download videos between 3-20 and 3-25
python bsky_video_downloader.py username -s 03-20-2025 -e 03-25-2025
```
