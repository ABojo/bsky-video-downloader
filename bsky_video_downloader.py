import argparse
from atproto import Client
import yt_dlp
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from datetime import datetime, timedelta

def valid_date(date_string):
    try:
        return datetime.strptime(date_string, "%m-%d-%Y")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{date_string}'. Please use YYYY-MM-DD.")

def get_args():
    parser = argparse.ArgumentParser(description="A script for downloading the videos on a BlueSky profile.")

    parser.add_argument('username', type=str, help='The username of the profile you want to download videos from.')
    parser.add_argument('-f', '--folder', type=str, help='The folder you wish to store the videos in.', required=False)
    parser.add_argument('-t', '--threads', type=int, default=3, help='The number of threads to use when downloading videos.')
    parser.add_argument('-l', '--limit', type=int, required=False, help='Limit the number of videos that will be downloaded.')
    parser.add_argument('-s', '--start-date', type=valid_date, required=False, help="Videos before this day will not be downloaded. Format: MM-DD-YYYY")
    parser.add_argument('-e', '--end-date', type=valid_date, required=False, help="Videos after this day will not be downloaded. Format: MM-DD-YYYY")

    args = parser.parse_args()

    if args.start_date and args.end_date and args.start_date > args.end_date:
        raise argparse.ArgumentTypeError(f"Your start date must be lower than your end date.")

    return args

def get_users_videos(client, username, limit = None, start_date = None, end_date = None):
    posts = []
    curr_cursor = (end_date + timedelta(1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ") if end_date else None
    
    while True:
        response = client.get_author_feed(actor=username, filter="posts_with_video", cursor=curr_cursor)
        curr_cursor = response["cursor"]
        raw_posts = response["feed"]
        
        for post in raw_posts:
            playlist_url = post["post"]["embed"]["playlist"]
            timestamp = post["post"]["indexed_at"]

            if start_date and datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") < start_date:
                return posts
            
            posts.append({"playlist_url": playlist_url, "timestamp": timestamp})

        if limit and len(posts) >= limit:
            return posts[0:limit]

        if not curr_cursor:
            break

    return posts

def download_video(url, folder, filename):
    ydl_options = {"format": "best", "quiet": True, "noprogress": True, "outtmpl": f"{folder}/{filename}"}

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download(url)
    
def main():
    args = get_args()
    folder = args.folder if args.folder else args.username
    client = Client(base_url="https://public.api.bsky.app/")

    try:
        print(f"Fetching videos from {args.username}")
        cleaned_posts = get_users_videos(client, args.username, args.limit, args.start_date, args.end_date)

        if not cleaned_posts:
            print("Sorry, I couldn't find any videos on that profile.")
            return 
        
        print(f"Found {len(cleaned_posts)} videos.")

        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = []

            for post in cleaned_posts:
                futures.append(executor.submit(download_video, post["playlist_url"], folder, f"{args.username}-{post["timestamp"]}.mp4"))

            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading Videos"):
                future.result() 

        print("Downloading complete.")

    except Exception as e:
        print(e)
        print("Sorry, but I couldn't find any data for that username. Please make sure you entered it correctly.")


if __name__ == "__main__":
    main()