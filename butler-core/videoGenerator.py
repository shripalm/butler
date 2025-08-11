from gtts import gTTS
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import os

class VideoGenerator:
    def __init__(self):
        self.width = 1080  # Width for YouTube Shorts (9:16 aspect ratio)
        self.height = 1920
        self.background_color = (0, 0, 0)  # Black background (fallback)
        self.font_size = 70
        self.font_color = 'white'
        # Use a system font that's guaranteed to be available on macOS
        self.font = 'Arial'
        # Default background video path from home directory
        self.bg_video_path = os.path.expanduser('~/projects/butler/butler-core/bgvids/video720.mp4')

    def create_tts(self, text, output_path='temp_audio.mp3', speed=1.25, slow=False):
        """Convert text to speech and optionally apply pitch-preserving speed-up (default 1.25x)."""
        import tempfile
        tts = gTTS(text=text, lang='en', slow=slow)
        # If speed is 1.0, write directly to output
        if abs(speed - 1.0) < 1e-6:
            tts.save(output_path)
            return output_path
        # Otherwise write to a temp file, then speed up into output_path
        fd, temp_path = tempfile.mkstemp(suffix='.mp3')
        os.close(fd)
        try:
            tts.save(temp_path)
            try:
                self.speed_up_audio_ffmpeg(temp_path, output_path, factor=speed)
                return output_path
            except Exception as e:
                # Fallback to librosa time-stretch -> wav -> mp3
                print(f"FFmpeg atempo failed for TTS speed-up ({e}). Falling back to librosa.")
                tmp_wav = output_path + '.wav'
                self.time_stretch_audio(temp_path, tmp_wav, rate=speed)
                try:
                    import subprocess
                    subprocess.run([
                        'ffmpeg', '-y', '-i', tmp_wav, '-vn', '-codec:a', 'libmp3lame', output_path
                    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                finally:
                    try:
                        if os.path.exists(tmp_wav):
                            os.remove(tmp_wav)
                    except Exception:
                        pass
                return output_path
        finally:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass

    def create_text_clip(self, text, duration, start_time=0):
        """Create a text clip with the specified duration"""
        margin = 200  # Increased margin for better visibility
        text_clip = TextClip(
            text=text,
            font=self.font,
            font_size=self.font_size,
            color=self.font_color,
            size=(self.width - margin, self.height - margin),  # Add height constraint with margins
            method='caption',  # Use caption method for auto text wrapping
            text_align='center',  # Center align the text
            vertical_align='center',  # Center vertically
            stroke_color='black',  # Add black border to text
            stroke_width=2,  # Width of the border
            bg_color=None,  # Transparent background
            transparent=True
        )
        text_clip = text_clip.with_position('center')
        text_clip = text_clip.with_start(start_time)
        text_clip = text_clip.with_duration(duration)
        return text_clip

    def split_into_chunks(self, text, max_words=5):
        """Split text into chunks of maximum 5 words"""
        words = text.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            current_chunk.append(word)
            if len(current_chunk) >= max_words:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        
        if current_chunk:  # Add any remaining words
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def estimate_chunk_duration(self, chunk, total_duration, total_text):
        """Estimate the duration for each chunk based on both word count and character length"""
        # Word-based calculation
        total_words = len(total_text.split())
        chunk_words = len(chunk.split())
        word_based_duration = (chunk_words / total_words) * total_duration
        
        # Character-based calculation (excluding spaces and punctuation)
        total_chars = len(''.join(c for c in total_text if c.isalnum()))
        chunk_chars = len(''.join(c for c in chunk if c.isalnum()))
        char_based_duration = (chunk_chars / total_chars) * total_duration if total_chars > 0 else 0
        
        # Use weighted average (60% word-based, 40% character-based)
        # Words matter more for natural speech timing, but character count helps with long words
        duration = (0.6 * word_based_duration) + (0.4 * char_based_duration)
        
        # Ensure minimum duration for very short chunks
        return max(duration, 1.0)

    def time_stretch_audio(self, input_path, output_path, rate=1.25):
        """Time-stretch audio using librosa to preserve pitch and tone"""
        import librosa
        import soundfile as sf
        y, sr = librosa.load(input_path, sr=None)
        y_stretched = librosa.effects.time_stretch(y, rate=rate)
        sf.write(output_path, y_stretched, sr)
        return output_path

    def speed_up_audio_ffmpeg(self, input_path, output_path, factor=1.25):
        """Use FFmpeg atempo filter to speed audio without changing pitch."""
        import subprocess
        # FFmpeg atempo supports 0.5-2.0 per filter; chain if outside.
        filters = []
        remaining = factor
        while remaining > 2.0:
            filters.append("atempo=2.0")
            remaining /= 2.0
        while remaining < 0.5 and remaining > 0:
            filters.append("atempo=0.5")
            remaining /= 0.5
        filters.append(f"atempo={remaining}")
        atempo_chain = ",".join(filters)
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vn",
            "-filter:a", atempo_chain,
            output_path,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path

    def create_video(self, text, project_name):
        """Create a video using the given text.

        Stores artifacts in a new folder: outputs/<project_name>/
        - <project_name>.mp3  (speech, 1.25x, pitch-preserving)
        - <project_name>.mp4  (final video)
        - <project_name>.txt  (script)
        Returns the output directory path.
        """
        # Prepare output directory
        base_dir = os.path.join(os.path.dirname(__file__), 'outputs', project_name)
        os.makedirs(base_dir, exist_ok=True)

        # Define artifact paths
        audio_path = os.path.join(base_dir, f"{project_name}.mp3")
        video_path = os.path.join(base_dir, f"{project_name}.mp4")
        script_path = os.path.join(base_dir, f"{project_name}.txt")

        # Save script
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            print(f"Warning: Failed to write script file: {e}")

        # Create audio using TTS with default 1.25x speed (pitch-preserving)
        audio_path = self.create_tts(text, output_path=audio_path, speed=1.25, slow=False)
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration

        # Create background from video if available
        try:
            print(f"Attempting to load background video from: {self.bg_video_path}")
            # Load and prepare background video
            bg_video = VideoFileClip(self.bg_video_path)
            print("Successfully loaded background video")
            
            # Handle video duration and start time
            if bg_video.duration < total_duration:
                print(f"Video too short, looping video (video duration: {bg_video.duration}s, needed duration: {total_duration}s)")
                bg_video = bg_video.loop(duration=total_duration)
            else:
                # Choose random start time, ensuring we have enough video left
                import random
                max_start = bg_video.duration - total_duration
                start_time = random.uniform(0, max_start)
                print(f"Starting video at {start_time:.2f}s and playing for {total_duration:.2f}s")
                bg_video = bg_video.subclipped(start_time, start_time + total_duration)
            
            # First set duration
            bg_video = bg_video.with_duration(total_duration)
            
            # Get current dimensions
            w, h = bg_video.size
            target_w, target_h = self.width, self.height
            
            # Calculate scaling to fill the frame while maintaining aspect ratio
            scale = max(target_w/w, target_h/h)
            new_size = (int(w*scale), int(h*scale))
            
            # Resize the video
            bg_video = bg_video.resized(new_size)
            
            # Center crop using x_center and y_center
            x_center = new_size[0] // 2
            y_center = new_size[1] // 2
            bg_video = bg_video.cropped(width=target_w, height=target_h, x_center=x_center, y_center=y_center)
            
            background = bg_video
        except Exception as e:
            print(f"Failed to load background video, using solid color instead: {str(e)}")
            background = ColorClip(
                size=(self.width, self.height),
                color=self.background_color,
                duration=total_duration
            )

        # Split text into chunks and create clips
        chunks = self.split_into_chunks(text)
        text_clips = []
        current_time = 0

        for chunk in chunks:
            # Calculate duration for this chunk
            chunk_duration = self.estimate_chunk_duration(chunk, total_duration, text)
            
            # Create text clip for this chunk
            chunk_clip = self.create_text_clip(chunk, chunk_duration, current_time)
            text_clips.append(chunk_clip)
            
            current_time += chunk_duration

        # Combine clips
        final_clip = CompositeVideoClip(
            [background] + text_clips,
            size=(self.width, self.height)
        ).with_audio(audio_clip)

        # Write video file with optimized settings
        final_clip.write_videofile(
            video_path,
            fps=60,
            codec='libx264',
            audio_codec='aac',
        )

        # Clean up
        try:
            audio_clip.close()
        finally:
            try:
                final_clip.close()
            finally:
                # Keep the final audio and script; temp files are removed in create_tts
                pass

        return base_dir

    # ...existing code...

# Example usage
if __name__ == "__main__":
    generator = VideoGenerator()
    text = "This is a test video for YouTube Shorts. The text will be synchronized with the voiceover."
    generator.create_video(text, "test-project")
