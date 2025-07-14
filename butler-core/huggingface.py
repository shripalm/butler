import requests

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def generate_image(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "height": 512, "width": 1024})
    with open("output4.png", "wb") as f:
        f.write(response.content)

generate_image("A futuristic, cinematic digital landscape representing the \"AI takeoff\" of June 2025. In the center, a glowing humanoid AI figure is lifting off like a rocket, symbolizing the singularity. Around it, floating fragments of the world: code, DNA helixes, robotic arms, glowing satellites, and news articles swirl in orbit. In the background, a sleek sci-fi city skyline with glowing neural networks woven into skyscrapers. Sam Altman's silhouette gazes toward a digital horizon, while dramatic lighting and deep contrast give a poetic, awe-inspiring feel. Incorporate elements of tension and wonder—symbolizing breakthroughs, ethical dilemmas, and a rapidly accelerating future. Style: hyperrealistic, cinematic, horizontal, 16:9 ratio, dark sci-fi palette with electric blues and neon magentas.")