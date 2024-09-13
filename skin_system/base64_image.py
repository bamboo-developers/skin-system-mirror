import base64

def encode(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    return str(base64.b64encode(image_data).decode('utf-8'))

def decode(base64_string, output_path):
    binary_data = base64.b64decode(base64_string)

    with open(output_path, "wb") as image_file:
        image_file.write(binary_data)