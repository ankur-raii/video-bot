import os
import aiohttp
import asyncio
import aiofiles
from aiofiles import os as aio_os
from tqdm.asyncio import tqdm
from random import choice
import requests
from typing import List, Optional


# Constants
ACCESS_TOKEN = "EAAhnrHYZAZBN0BO57M1imTVMjFQZBi6VGNNu9a4POmfPboCCteEKyODvK5aeqsLrIc9i7giYwbyUpNlADmcNHVj2MMWFCnq3CEjflBAqAZBvuDd2sgmfhXGrNuAQW7P4sTHADIIphDd5MczCYcYNZBhaYT4LMKVXZA6bhg37IL0rMQhBSoX1JLiUD48MksKO4OZAB4YAzP6"
GRAPH_API_URL = "https://graph.facebook.com/v17.0/"
GET_UPLOAD_URL = "https://api.socialverseapp.com/posts/generate-upload-url"
CREATE_POST_URL = "https://api.socialverseapp.com/posts"
HASHTAG = "motivational"
VIDEOS_DIR = "videos"

# Ensure the videos directory exists
if not os.path.exists(VIDEOS_DIR):
    os.mkdir(VIDEOS_DIR)


# -------------------------------
# API Interaction Functions
# -------------------------------

def get_hashtag_id(access_token: str, hashtag: str) -> str:
    """
    Get the hashtag ID from Instagram Graph API.
    """
    url = f"{GRAPH_API_URL}ig_hashtag_search?user_id=17841404143868690&q={hashtag}&access_token={access_token}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['data'][0]['id']


def fetch_posts_by_hashtag(hashtag_id: str, access_token: str) -> List[dict]:
    """
    Fetch recent posts for a given hashtag.
    """
    url = f"{GRAPH_API_URL}{hashtag_id}/recent_media?user_id=17841404143868690&fields=id,media_type,media_url,caption&access_token={access_token}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    posts = [post for post in data.get('data', []) if post.get('media_type') == 'VIDEO']
    return posts


# -------------------------------
# Video Processing Functions
# -------------------------------

def generate_caption(caption: str) -> str:
    """
    Add some motivational text and hashtags to the caption.
    """
    motivational_phrases = [
        "Stay positive!",
        "Success starts with self-discipline!",
        "#KeepPushing",
        "Stay focused. #Motivation",
        "Let your passion fuel your progress!"
    ]
    hashtags = "#motivation #inspiration #positivity "
    
    # Adding motivational phrase and hashtags to the caption
    return f"{caption}\n\n{choice(motivational_phrases)}\n{hashtags}"


async def download_video(video_url: str, output_path: str) -> None:
    """
    Download video from a given URL.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            response.raise_for_status()
            async with aiofiles.open(output_path, "wb") as file:
                await file.write(await response.read())
    print(f"Downloaded: {output_path}")


# -------------------------------
# Upload Functions
# -------------------------------

async def get_upload_url(session: aiohttp.ClientSession) -> dict:
    """
    Get a pre-signed upload URL from the server.
    """
    headers = {
        "Flic-Token": "flic_331f0de1604ddb80c105bdbaa2c14584900ea6d08e38f5426fc6150e9b7e77ce",  # my flic token
        "Content-Type": "application/json",
    }
    async with session.get(GET_UPLOAD_URL, headers=headers) as response:
        response.raise_for_status()
        return await response.json()


async def upload_video(session: aiohttp.ClientSession, file_path: str, upload_url: str) -> None:
    """
    Upload video to the server using the pre-signed URL.
    """
    headers = {"Content-Type": "video/mp4"}
    async with aiofiles.open(file_path, "rb") as file:
        video_data = await file.read()
    async with session.put(upload_url, data=video_data, headers=headers) as response:
        response.raise_for_status()
    print(f"Uploaded: {file_path}")


async def create_post(session: aiohttp.ClientSession, video_title: str, video_hash: str, category_id: int, caption: str) -> dict:
    """
    Create a post on the server after video upload.
    """
    headers = {
        "Flic-Token": "flic_331f0de1604ddb80c105bdbaa2c14584900ea6d08e38f5426fc6150e9b7e77ce",  #my flic token
        "Content-Type": "application/json",
    }
    data = {
        "title": video_title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id,
        "caption": caption,  # Added the caption
    }
    async with session.post(CREATE_POST_URL, json=data, headers=headers) as response:
        response.raise_for_status()
        print(f"Post created for: {video_title}")
        return await response.json()


# -------------------------------
# Main Process
# -------------------------------

async def process_video(post: dict) -> None:
    """
    Process a video: download, upload, and create a post.
    """
    async with aiohttp.ClientSession() as session:
        try:
            video_url = post.get("media_url")
            caption = post.get("caption", "Motivational Video")
            video_id = post.get("id")
            output_path = os.path.join(VIDEOS_DIR, f"{video_id}.mp4")

            # Download video
            print(f"Downloading video from: {video_url}")
            await download_video(video_url, output_path)

            # Get upload URL and hash
            print(f"Getting upload URL for: {output_path}")
            upload_data = await get_upload_url(session)
            upload_url = upload_data["url"]
            video_hash = upload_data["hash"]

            # Upload the video
            print(f"Uploading video: {output_path}")
            await upload_video(session, output_path, upload_url)

            # Generate a simple caption
            new_caption = generate_caption(caption)

            # Create post
            video_title = caption
            category_id = 25  
            print(f"Creating post for: {video_title}")
            await create_post(session, video_title, video_hash, category_id, new_caption)

            # Delete processed video
            print(f"Deleting processed video: {output_path}")
            await aiofiles.os.remove(output_path)

            # Print success message 
            print("🎉🚀 Successfully uploaded a random motivational reel from Instagram to Socialverse server!")

        except Exception as e:
            print(f"Error processing video: {e}")


async def main() -> None:
    """
    Main function to arrange the video fetching, processing, and posting.
    """
    # Step 1: Get hashtag ID
    print(f"Fetching hashtag ID for #{HASHTAG}")
    hashtag_id = get_hashtag_id(ACCESS_TOKEN, HASHTAG)
    print(f"Hashtag ID: {hashtag_id}")

    # Step 2: Fetch posts
    print(f"Fetching posts for hashtag #{HASHTAG}")
    posts = fetch_posts_by_hashtag(hashtag_id, ACCESS_TOKEN)
    if not posts:
        print("No videos found for the specified hashtag.")
        return

    # Step 3: Process videos concurrently
    print(f"Processing {len(posts)} videos concurrently...")
    await asyncio.gather(*[process_video(post) for post in posts])


if __name__ == "__main__":
    asyncio.run(main())
