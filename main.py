import argparse

def main():
    parser = argparse.ArgumentParser(description="A script for downloading the videos on a BlueSky profile.")

    parser.add_argument('username', type=str, help='The username of the profile you want to download videos from.')
    parser.add_argument('-f', '--folder', type=str, help='The folder you wish to store the videos in.', required=False)

    args = parser.parse_args()
    
if __name__ == "__main__":
    main()