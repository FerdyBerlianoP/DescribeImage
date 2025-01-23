from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
import requests
import io

class ImageDescriber:
  """
  A class to encapsulate image description logic.
  """
  def __init__(self, api_key):
    self.api_key = api_key
    genai.configure(api_key=api_key)
    self.model = genai.GenerativeModel("gemini-1.5-flash")

  def describe_image(self, image_url):
    """
    Generates a description for a given image URL.

    Args:
      image_url: The URL of the image.

    Returns:
      The description of the image or an error message.
    """
    try:
      response = requests.get(image_url, stream=True)
      response.raise_for_status() 
      image = Image.open(io.BytesIO(response.content))
      prompt_and_image = ["Describe this image", image]
      response = self.model.generate_content(prompt_and_image)
      return response.text
    except Exception as e:
      return f"Error: Could not describe image from URL: {image_url} - {str(e)}"

app = Flask(__name__)

# Replace with your actual API key
image_describer = ImageDescriber("AIzaSyC9BUs5B7d1B5qVwYHnhTBUCssCKXuiR5w")

@app.route('/describe_images', methods=['POST'])
def describe_images():
  """
  API endpoint to receive image URLs and return descriptions.
  """
  try:
    data = request.get_json()
    image_urls = data.get('image_urls')

    if not image_urls:
      return jsonify({"error": "Missing 'image_urls' in request body"}), 400

    descriptions = []
    for image_url in image_urls:
      try:
        description = image_describer.describe_image(image_url)
        descriptions.append({"url": image_url, "description": description})
      except Exception as e:
        descriptions.append({"url": image_url, "error": f"Error: Could not describe image: {e}"})

    return jsonify({"descriptions": descriptions})

  except Exception as e:
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
  # app.run(debug=True)
  app.run(host='0.0.0.0', port=port, debug=True)

# from flask import Flask, request, jsonify
# import google.generativeai as genai
# from PIL import Image
# import requests
# import io

# class ImageDescriber:
#   """
#   A class to encapsulate image description logic.
#   """
#   def __init__(self, api_key):
#     self.api_key = api_key
#     genai.configure(api_key=api_key)
#     self.model = genai.GenerativeModel("gemini-1.5-flash")

#   def describe_image(self, image_url):
#     """
#     Generates a description for a given image URL.
#     """
#     try:
#       response = requests.get(image_url, stream=True)
#       response.raise_for_status() 
#       image = Image.open(io.BytesIO(response.content))
#       prompt_and_image = ["provide a brief description of any drawings or diagrams that illustrate the invention. Each drawing must be numbered and described in a short, clear manner.", 
#                           image]
#       response = self.model.generate_content(prompt_and_image)
#       return response.text
#     except Exception as e:
#       print(f"Error processing image from URL: {e}")
#       return f"Error: Could not describe image from URL: {image_url}"

# app = Flask(__name__)

# # Replace with your actual API key
# image_describer = ImageDescriber("AIzaSyC9BUs5B7d1B5qVwYHnhTBUCssCKXuiR5w")

# @app.route('/describe_image', methods=['POST'])
# def describe_image():
#   """
#   API endpoint to receive image URL and return its description.
#   """
#   try:
#     data = request.get_json()
#     image_url = data.get('image_url')

#     if not image_url:
#       return jsonify({"error": "Missing 'image_url' in request body"}), 400

#     description = image_describer.describe_image(image_url)
#     return jsonify({"description": description})

#   except Exception as e:
#     return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#   app.run(debug=True)
