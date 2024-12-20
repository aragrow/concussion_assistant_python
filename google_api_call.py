
import google.generativeai as genai
import json
from dotenv import load_dotenv
from flask import request, jsonify
import requests

class GoogleApiCall:

  def __init__(self):
      
      print('Exec=> GoogleApiCall.__init__()')  
      #self.nonce = NonceTool.generate_nonce()
      self.bookFile = 'book.json'

  # End of __init__()

  def main(self):
    
    print('Exec=> GoogleApiCall.main()')
    
    try:
      json_data = request.get_json() 

      # Convert JSON string to Python list
      if 'what' not in json_data['context']:
          return {"error": "Missing 'what' in the request body"}, 400
    
      if 'text' not in json_data['context']:
          return {"error": "Missing 'text' in the request body"}, 400

      # Create the model
      generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
      }
      
      print('---- genai.GenerativeModel()')
      model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction='''
          You are a highly knowledgeable expert on concussion. 
          Your primary goal is to assist the user by accurately analyzing and answering their requests related to the book. 
          If the user provides additional context, you must carefully incorporate it to tailor your response, ensuring accuracy and relevance.
          When crafting your answer:
          Be thorough, clear, and insightful.
          Use evidence from the text where applicable.
          Adapt your tone and depth based on the user’s query, whether it is a detailed literary analysis, a concise summary, or a specific interpretation.
          Always strive to provide value by addressing the user’s needs with precision and depth.
          Use easy readable natural human language                        
        ''',
      )

      print('---- self.load_json_file()')
      book = self.load_json_file()

      print('---- model.start_chat()')
      chat_session = model.start_chat(
        history = book['content']
      )

      prompt  = {
        'role': 'user',  # Correct role
        'content': {
            'parts': [
                {'type': 'text', 'text': f"what: {json_data['context']['what']}, text: {json_data['context']['text']}"}
            ]
        }
      }

      print(prompt)  # Debug: To check if the prompt is correct

      print('---- chat_session.send_message()')
      response = chat_session.send_message(prompt)

      print(response)

      return response.text

    except Exception as e:
      print(f"An unexpected error occurred: {e}")
      return None

  # End of main()

  def load_json_file(self):

    print('Exec=> GoogleApiCall.load_json_file()')
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

  # End of load_json_file()

  def save_json_array(self, data, filepath):

    print('Exec=> GoogleApiCall.load_json_file()')
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

  # End of save_json_array()