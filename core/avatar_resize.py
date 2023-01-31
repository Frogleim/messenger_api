from PIL import Image
from io import BytesIO


def resize_image_50(image):
    image = Image.open(BytesIO(image))
    image = image.resize((50, 50))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_resized = buffer.getvalue()
    return image_resized


def resize_image_100(image):
    image = Image.open(BytesIO(image))
    image = image.resize((100, 100))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_resized = buffer.getvalue()
    return image_resized


def resize_image_400(image):
    image = Image.open(BytesIO(image))
    image = image.resize((400, 400))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_resized = buffer.getvalue()
    return image_resized
