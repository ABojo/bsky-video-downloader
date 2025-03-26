import argparse
from atproto import Client
import yt_dlp
from concurrent.futures import ThreadPoolExecutor

def get_args():
    parser = argparse.ArgumentParser(description="A script for downloading the videos on a BlueSky profile.")

    parser.add_argument('username', type=str, help='The username of the profile you want to download videos from.')
    parser.add_argument('-f', '--folder', type=str, help='The folder you wish to store the videos in.', required=False)
    parser.add_argument('-t', '--threads', type=int, default=3, help='The number of threads to use when downloading videos.')

    return parser.parse_args()

def get_users_videos(client, username, cursor = None):
    posts = []
    curr_cursor = cursor

    while True:
        response = client.get_author_feed(actor=username, filter="posts_with_video", cursor=curr_cursor)
        curr_cursor = response["cursor"]
        raw_posts = response["feed"]

        for post in raw_posts:
            playlist_url = post["post"]["embed"]["playlist"]
            timestamp = post["post"]["indexed_at"]

            posts.append({"playlist_url": playlist_url, "timestamp": timestamp})

        if not curr_cursor:
            break

    return posts

def download_video(url, folder, filename):
    ydl_options = {"format": "best", "quiet": True, "outtmpl": f"{folder}/{filename}"}

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download(url)
    
def main():
    args = get_args()
    folder = args.folder if args.folder else args.username
    client = Client(base_url="https://public.api.bsky.app/")

    try:
        cleaned_posts = get_users_videos(client, args.username)

        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            for post in cleaned_posts:
                executor.submit(download_video, post["playlist_url"], folder, f"{args.username}-{post["timestamp"]}.mp4")

    except Exception as e:
        print(e)
        print("Sorry, but I couldn't find any data for that username. Please make sure you entered it correctly.")


if __name__ == "__main__":
    main()