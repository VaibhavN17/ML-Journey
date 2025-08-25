from PIL import Image

def enhance_image(input_path, output_path):
    img = Image.open(input_path).convert("RGB")
    # Dummy ML enhancement: just resize for demo
    img = img.resize((img.width * 2, img.height * 2))
    img.save(output_path)
    return True