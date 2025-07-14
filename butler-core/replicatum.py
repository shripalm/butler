import os
import replicate
import requests

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_IZap0NpQfEMpb4uGRgHZuVFDqGAdIeG0cili4"

# Model with working image generation + dimensions
model = "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc"
# model = "stability-ai/stable-diffusion-3"

# Prompt
prompt = "A futuristic, cinematic digital landscape representing the \"AI takeoff\" of June 2025. In the center, a glowing humanoid AI figure is lifting off like a rocket, symbolizing the singularity. Around it, floating fragments of the world: code, DNA helixes, robotic arms, glowing satellites, and news articles swirl in orbit. In the background, a sleek sci-fi city skyline with glowing neural networks woven into skyscrapers. Sam Altman's silhouette gazes toward a digital horizon, while dramatic lighting and deep contrast give a poetic, awe-inspiring feel. Incorporate elements of tension and wonder—symbolizing breakthroughs, ethical dilemmas, and a rapidly accelerating future. Style: hyperrealistic, cinematic, horizontal, 16:9 ratio, dark sci-fi palette with electric blues and neon magentas."

# Call Replicate API
output = replicate.run(
    model,
    input={
        "prompt": prompt,
        "aspect_ratio": "16:9",  # Horizontal aspect ratio
    }
)

print("Generated Image URLs:", output)

# Download it locally
for index, item in enumerate(output):
    with open(f"output_{index}.webp", "wb") as file:
        file.write(item.read())