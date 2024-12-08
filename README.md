# Video Search and Upload Bot Assignment

## Overview

This is a Python script that fetches, downloads, uploads, and posts motivational video content from Instagram on your server. With this solution, using the Instagram Graph API and an upload API on the server, it becomes possible to post motivational content with automatically generated captions on any platform in the most efficient way possible.

This document explains how the system works, the steps to set it up, and how it can be used to integrate motivational content seamlessly.

## Features

- **Instagram Video Fetching:** Automatically fetches the latest video posts based on a specified hashtag, such as `#motivational`.
- **Video Downloading:** The script downloads the videos asynchronously to your local directory.
- **Automatic Uploading:** The downloaded videos are uploaded on a dedicated server using a pre-signed URL.
- **Motivational Caption Generation:** It generates customized captions for every video by adding motivational phrases to it along with the relevant hashtags.
- **Parallel Processing:** Processes multiple videos in parallel for efficient handling of large datasets
- **Error Handling:** Robust error handling has been implemented to ensure smooth running even if there is any failure.

## Setup

Use this script as follows:

1. Clone the Repository

Clone the repository to your local machine by running the following command in command terminal:

```bash
git clone https://github.com/ankur-raii/video-bot.git
cd Desktop\video-bot  #Go into the project directory:
```


2. Set Up a Virtual Environment (Optional but Recommended)

  Creating a virtual environment helps keep dependencies separate:

```bash
python -m venv venv
venv\Scripts\activate
```
3. Install Dependencies

Install the required libraries from requirements.txt:

```bash
pip install -r requirements.txt
```
This will install necessary libraries like `aiohttp`, `requests`, `aiofiles`, and `tqdm`.

4. Exit from Virtual Environment:


```bash
video-bot>deactivate
```

5. Run the Script

Finally, run the script in file directory:

```bash
video-bot>python main.py
```


## How It Works:

### Step-by-Step Process

1. **Retrieve Hashtag ID:**  
   The script first fetches the ID associated with the given hashtag (e.g., `#motivational`) from the Instagram Graph API. This ID is essential for searching posts under that hashtag.

2. **Fetch Instagram Posts:**
The script then retrieves the last few media posts based on the hashtag ID. Since only video posts are considered in this process, only the video content is downloaded and uploaded.

3. **Download Videos**: 
 After posting retrieval, the script download each video asynchronously to the `videos/` directory in the local machine.

4. **Captions Generation**:
After downloading, the script produces a caption for each video. This caption contains a random motivational phrase and relevant hashtags to maximize engagement and reach.

5. **Upload Videos:**
   Once the caption is generated, the script uploads the video to your custom server. The script uses a pre-signed URL for this upload, so that the server knows where to store the video.

6. **Publish post:**  When uploading successfully, it generates a post attached with a video and its generated caption onto the server.

7. **Cleanup:**  The script removes the locally placed video after successfully posting the content onto the server. It frees the available hard disk space.
--------------------------------

### Expected Outcomes

The script will log the following steps during execution:

Fetch the hashtag ID
Download each video
Upload all videos to the server
Create posts with captions that were generated
Delete all processed video files

Example output

```bash
Fetching hashtag ID for #motivational
Hashtag ID: 17841404143868690
Fetching posts for hashtag #motivational
Downloading video from: https://video_url_here
Uploading video: motivational_video.mp4
Creating post for: Stay positive! #Motivation
Successfully uploaded a random motivational reel from Instagram to Socialverse server!
```

---

## Error Handling

The script contains error handling for different failure scenarios:

**Invalid Access Token:** If the Instagram access token is invalid, an authentication error is shown. Make sure that the token has the necessary permissions.
**Rate Limiting:** Instagram or your custom server may have rate limits. If you get rate limiting errors, you can add a delay between requests or manage retries.
**Category ID Issues:** In case the `category_id` is incorrect, then the post creation will fail. Ensure that the category ID is corresponding to a valid category on the server.

---

## Troubleshooting

If you still have problems, here are some common problems and solutions:

**Invalid Instagram Token:**   Ensure that the access token is valid and has permissions for the necessary endpoints. You might need to regenerate it if it expires.

**Missing Category ID:**  
  If the category ID is missing or incorrect, the post creation step will fail. Ensure that you are using the correct category ID that aligns with your server configuration.

**Server Upload Failure:**  
  Check if the server's upload URL is reachable. If uploading fails, verify that the server is configured to accept the video file and the API key is valid.


## Conclusion

This Python script provides a powerful tool for automating the reposting of motivational video content to a custom platform or server. Utilizing Instagram's Graph API and server-side upload capabilities, the system assists in efficient content reposting and engagement management.

Please feel free to contact me for any further inquiries or modifications. I am happy to assist in integrating this solution into your workflow.
