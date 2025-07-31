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

    def create_tts(self, text, output_path='temp_audio.mp3'):
        """Convert text to speech"""
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        return output_path

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

    def create_video(self, text, output_path='output.mp4'):
        """Create a video from the given text with synchronized chunks"""
        # Create audio
        audio_path = self.create_tts(text)
        audio_clip = AudioFileClip(audio_path)
        # Speed up the audio using MoviePy's with_speed_scaled
        audio_clip = audio_clip.with_speed_scaled(factor=1.25)
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
            output_path,
            fps=60,
            codec='libx264',
            audio_codec='aac',
        )

        # Clean up
        audio_clip.close()
        final_clip.close()
        os.remove(audio_path)

        return output_path

# Example usage
if __name__ == "__main__":
    generator = VideoGenerator()
    text = "This is a test video for YouTube Shorts. The text will be synchronized with the voiceover."
    generator.create_video(text, "output.mp4")
