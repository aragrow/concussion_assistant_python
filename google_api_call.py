
import google.generativeai as genai
import json
from dotenv import load_dotenv
from flask import request, jsonify
import requests

class GoogleApiCall:

  def __init__(self):

      #self.nonce = NonceTool.generate_nonce()
      self.bookFile = 'prompt.json'
      self.prompt = ''

  def main(self):

    json_data = request.get_json() 
    # Convert JSON string to Python list
    if 'what' not in json_data:
        return {"error": "Missing 'what' in the request body"}, 400
    job = json_data['job']
    if 'text' not in json_data:
        return {"error": "Missing 'text' in the request body"}, 400
    
    self.what = json_data['what']
    self.text = json_data['text']

    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
      model_name="gemini-2.0-flash-exp",
      generation_config=generation_config,
      system_instruction="You are a professional close caption writer, read the file and retrieve the text of the audio order by uploaded order.",
    )

    chat_session = model.start_chat(
      history = self.load_json_file()
    )

    self.prompt = {f'''
        what:{json_data['what']},
        text:{json_data['text']}               
    '''}

    response = chat_session.send_message(self.prompt)

    print(response.text)

    return response.text

  def load_json_file(self):
    """Loads a JSON file and returns the data as a Python object."""
    try:
      with open(self.bookFile, 'r') as file:
        data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {self.bookFile}")
        return None
    except json.JSONDecodeError:
      print(f"Error: Could not decode JSON from {self.bookFile}. The file may be invalid JSON.")
      return None
    except Exception as e:
      print(f"An unexpected error occurred: {e}")
      return None

    # Example usage:
    filepath = 'data.json'  # Replace with your actual file path
    json_data = load_json_file(self.bookFile)

    if json_data:
        print(json_data)  # Print the loaded data
        # Now you can work with the json_data, for example:
        if isinstance(json_data, dict):
            print("It's a dictionary!")
            if 'name' in json_data:
                print(f"Name: {json_data['name']}")
        elif isinstance(json_data, list):
            print("It's a list!")
            print(f"Number of entries: {len(json_data)}")

  def save_json_array(self, data, filepath):
    """Saves a Python list or dictionary to a JSON file.

    Args:
      data: The Python list or dictionary to save.
      filepath: The path to the JSON file where data will be saved.
    """
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4) # the indent parameter is optional and provides better readability
        print(f"Data successfully saved to {filepath}")
    except TypeError as e:
      print(f"Error: Could not serialize data as JSON: {e}")
    except Exception as e:
      print(f"An unexpected error occurred: {e}")