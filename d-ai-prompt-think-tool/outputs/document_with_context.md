# Audio Normalization in Mux: A Simple Guide

## Introduction

**Audio normalization** is the process of adjusting the loudness of your video's audio track to a standard level, so your viewers don't have to constantly adjust their volume. In Mux, you can enable audio normalization when you create a new on-demand asset (i.e., when you upload a video for streaming).

Let's walk through what this means, when to use it, and how to enable it in Mux.

---

## What is Audio Normalization?

- **Loudness normalization** adjusts the audio so that the average loudness matches a target value (in Mux, this is –24 LUFS).
- This helps ensure a consistent listening experience across all your videos.
- It's especially useful if your source videos come from different creators or devices with varying audio levels.

**Analogy:**  
Think of audio normalization like a movie theater employee who makes sure every movie is played at the same comfortable volume, no matter how loud or quiet the original file is.

---

## When Should You Use Audio Normalization?

- If your videos come from many sources and you want a consistent audio experience.
- If you notice some videos are much louder or quieter than others.
- If you want to meet broadcast or streaming standards for loudness.

**Note:**  
Audio normalization is only available for **on-demand assets** (not live streams) and must be set at the time of asset creation. You cannot enable it after the asset is created.

---

## How to Enable Audio Normalization in Mux

You enable audio normalization by setting the `normalize_audio` parameter to `true` when you create a new asset via the API.

### Example: Enabling Audio Normalization via API

Here's a sample `POST` request to create an asset with audio normalization enabled:

```bash
curl https://api.mux.com/video/v1/assets \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
        "input": "https://example.com/myVideo.mp4",
        "playback_policy": ["public"],
        "video_quality": "basic",
        "normalize_audio": true 
    }' \
  -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET}
```

**Key part:**  
```json
"normalize_audio": true
```

### What Happens Next?

- Mux will process your video and adjust the audio loudness to the target level (–24 LUFS).
- The rest of your asset creation flow remains the same.

---

## Important Notes

- **You cannot enable or disable audio normalization after the asset is created.**  
  If you forget to set it, you'll need to re-upload the video.
- **Audio normalization is not available for live streams.**
- **Target loudness:** Mux normalizes to –24 LUFS, which is a common standard for broadcast and streaming.

---

## Summary Table

| Feature                | Supported?         |
|------------------------|-------------------|
| On-demand assets       | ✅ Yes             |
| Live streams           | ❌ No              |
| Enable after creation  | ❌ No              |
| Default target loudness| –24 LUFS          |

---

## Summary

- **Audio normalization** in Mux ensures your videos have consistent loudness.
- Enable it by setting `"normalize_audio": true` when creating an asset.
- It's only available for on-demand assets and must be set at creation time.
- This helps provide a better, more professional experience for your viewers.

---

**Reference:**  
[Official Mux Docs – Adjust audio levels](https://docs.mux.com/guides/adjust-audio-levels)

---

**"Consistent audio is key to a great viewing experience. With Mux, it's just a single parameter away!"**