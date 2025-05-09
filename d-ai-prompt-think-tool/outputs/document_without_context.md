# Audio Normalization in Mux: A Simple Guide  
   
## Introduction  
   
**Audio normalization** is the process of adjusting the volume of audio tracks so that they play at a consistent level. This is important for a good user experience—nobody likes to turn the volume up and down between videos!  
   
**Mux** is a popular video API platform that handles video (and audio) processing, streaming, and delivery. If you want to ensure your videos have consistent audio levels, you might wonder: *How do I normalize audio in Mux?*  
   
---  
   
## Does Mux Support Audio Normalization?  
   
**Short answer:**    
Mux does not currently offer a direct, built-in audio normalization feature as part of its standard video processing pipeline (as of June 2024).  
   
**What does this mean?**    
- Mux will encode and deliver your audio as-is, without adjusting the loudness or normalizing the audio levels.  
- If you need normalized audio, you must handle this **before** uploading your video to Mux.  
   
---  
   
## What is Audio Normalization?  
   
**Audio normalization** means making sure all your audio tracks are at a similar loudness.    
- Think of it like making sure all your friends speak at the same volume in a group photo—no one is whispering, and no one is shouting.  
   
**Why is it important?**  
- Consistent user experience  
- Avoids sudden loud or quiet moments  
- Professional quality  
   
---  
   
## How to Normalize Audio Before Uploading to Mux  
   
Since Mux doesn't do this for you, you need to normalize your audio **before** uploading. Here’s how you can do it:  
   
### 1. **Using FFmpeg (Open Source Tool)**  
   
**FFmpeg** is a powerful command-line tool for processing audio and video files.  
   
#### Example Command  
   
```bash  
ffmpeg -i input.mp4 -af "loudnorm" -c:v copy output.mp4  
```  
   
- `-i input.mp4`: Your original video file  
- `-af "loudnorm"`: Applies the EBU R128 loudness normalization filter  
- `-c:v copy`: Copies the video stream without re-encoding (faster, no quality loss)  
- `output.mp4`: The normalized output file  
   
**Analogy:**    
Think of FFmpeg as a kitchen blender—you put in your ingredients (video), press a button (command), and get a smooth, consistent result (normalized audio).  
   
---  
   
### 2. **Using Audio Editing Software**  
   
If you prefer a graphical interface, you can use tools like:  
- **Audacity** (free)  
- **Adobe Audition**  
- **DaVinci Resolve**  
   
**Steps:**  
1. Extract the audio from your video.  
2. Normalize the audio in your editor.  
3. Recombine the audio with the video.  
4. Upload the final video to Mux.  
   
---  
   
## End-to-End Example  
   
**Scenario:**    
You have a video file `lecture.mp4` with quiet audio. You want to normalize it before uploading to Mux.  
   
**Steps:**  
1. **Normalize with FFmpeg:**  
   ```bash  
   ffmpeg -i lecture.mp4 -af "loudnorm" -c:v copy lecture_normalized.mp4  
   ```  
2. **Upload `lecture_normalized.mp4` to Mux** using their API or dashboard.  
   
---  
   
## Real-World Applications  
   
- **Online courses:** Ensures all lessons have the same audio level.  
- **User-generated content:** Keeps volume consistent across uploads.  
- **Corporate training:** Professional, polished video presentations.  
   
---  
   
## Summary  
   
- **Mux does not currently normalize audio automatically.**  
- **Normalize your audio before uploading** using tools like FFmpeg or audio editors.  
- **Consistent audio** improves user experience and professionalism.  
   
---  
   
> **Tip:** Always preview your video after normalization to ensure the audio sounds right!  
   
---  
   
**References:**  
- [Mux Documentation](https://docs.mux.com/docs)  
- [FFmpeg loudnorm filter](https://ffmpeg.org/ffmpeg-filters.html#loudnorm)  
- [Audacity Normalization Guide](https://manual.audacityteam.org/man/normalize.html)  
   
---  
   
If you have more questions about Mux or audio processing, feel free to ask!