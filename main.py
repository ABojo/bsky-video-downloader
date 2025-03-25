import argparse
from atproto import Client


def get_args():
    parser = argparse.ArgumentParser(description="A script for downloading the videos on a BlueSky profile.")

    parser.add_argument('username', type=str, help='The username of the profile you want to download videos from.')
    parser.add_argument('-f', '--folder', type=str, help='The folder you wish to store the videos in.', required=False)

    return parser.parse_args()

def main():
    args = get_args()
    client = Client(base_url="https://public.api.bsky.app/")
    
    try:
        response = client.get_author_feed(actor=args.username, filter="posts_with_video")
        raw_posts = response["feed"]
        cleaned_posts = []
        
        for post in raw_posts:
            new_post = {"playlist_url": post["post"]["embed"]["playlist"], "timestamp": post["post"]["indexed_at"]}
            cleaned_posts.append(new_post)
    
    except Exception as e:
        print("Sorry, but I couldn't find any data for that username. Please make sure you entered it correctly.")


if __name__ == "__main__":
    main()