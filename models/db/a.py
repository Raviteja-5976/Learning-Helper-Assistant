# import requests
# import os

# # Define the URL of your PDF file
# SOURCE_FILE_URL = r"C:\Users\ravit\Desktop\Learning-Helper-Assistant\models\db\amzn_shareholder-letter-20072.pdf"

# # PlayNote API URL
# url = "https://api.play.ai/api/v1/playnotes"

# # Retrieve API key and User ID from environment variables
# user_id = 'WayNXGmUolfPoRXFuwa5XuIFFmj1'
# api_key = 'ak-1434c93eae2d40c4bd9846e8d5e88bb7'

# # Set up headers with authorization details
# headers = {
#     'AUTHORIZATION': api_key,
#     'X-USER-ID': user_id,
#     'accept': 'application/json'
# }



# # Configure the request parameters
# files = {
#     'sourceFileUrl': (None, SOURCE_FILE_URL),
#     'synthesisStyle': (None, 'podcast'),
#     'voice1': (None, 's3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json'),
#     'voice1Name': (None, 'Angelo'),
#     'voice2': (None, 's3://voice-cloning-zero-shot/e040bd1b-f190-4bdb-83f0-75ef85b18f84/original/manifest.json'),
#     'voice2Name': (None, 'Deedee'),
# }

# # Send the POST request
# response = requests.post(url, headers=headers, files=files)

# # Check the response
# if response.status_code == 201:
#     print("Request sent successfully!")
#     playNoteId = response.json().get('id')
#     print(f"Generated PlayNote ID: {playNoteId}")
# else:
#     print(f"Failed to generate PlayNote: {response.text}")
#     playNoteId = None

# # Ensure playNoteId is defined before proceeding
# if playNoteId:
#     import urllib.parse
#     import time

#     # Double-encode the PlayNote ID for the URL
#     double_encoded_id = urllib.parse.quote(playNoteId, safe='')

#     # Construct the final URL to check the status
#     status_url = f"https://api.play.ai/api/v1/playnotes/{double_encoded_id}"

#     # Poll for completion
#     while True:
#         response = requests.get(status_url, headers=headers)
#         if response.status_code == 200:
#             playnote_data = response.json()
#             status = playnote_data['status']
#             if status == 'completed':
#                 print("PlayNote generation complete!")
#                 print("Audio URL:", playnote_data['audioUrl'])
#                 break
#             elif status == 'generating':
#                 print("Please wait, your PlayNote is still generating...")
#                 time.sleep(120)  # Wait for 2 minutes before polling again
#             else:
#                 print("PlayNote creation failed, please try again.")
#                 break
#         else:
#             print(f"Error polling for PlayNote status: {response.text}")
#             break
# else:
#     print("PlayNote ID is not defined. Exiting.")

# import PyPDF2
# from gtts import gTTS
# import requests
# import os

# # Step 1: Extract Text from the PDF
# pdf_path = r"C:\Users\ravit\Desktop\Learning-Helper-Assistant\models\db\amzn_shareholder-letter-20072.pdf"

# # Extract text from the PDF
# with open(pdf_path, 'rb') as file:
#     reader = PyPDF2.PdfReader(file)
#     text = ''.join(page.extract_text() for page in reader.pages)

# # Step 2: Convert Text to Audio using gTTS (Google Text-to-Speech)
# audio_file_path = "output_audio.mp3"
# tts = gTTS(text, lang='en')
# tts.save(audio_file_path)

# # Step 3: Upload Audio to PlayNote API

# # PlayNote API URL
# url = "https://api.play.ai/api/v1/playnotes"

# # Retrieve API key and User ID from environment variables
# user_id = 'WayNXGmUolfPoRXFuwa5XuIFFmj1'  # Add your user ID here
# api_key = 'ak-1434c93eae2d40c4bd9846e8d5e88bb7'  # Add your API key here

# # Set up headers with authorization details
# headers = {
#     'AUTHORIZATION': api_key,
#     'X-USER-ID': user_id,
#     'accept': 'application/json'
# }

# # Define the audio file to upload
# files = {
#     'sourceFileUrl': open(audio_file_path, 'rb'),
#     'synthesisStyle': (None, 'podcast'),
#     'voice1': (None, 's3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json'),
#     'voice1Name': (None, 'Angelo'),
#     'voice2': (None, 's3://voice-cloning-zero-shot/e040bd1b-f190-4bdb-83f0-75ef85b18f84/original/manifest.json'),
#     'voice2Name': (None, 'Deedee'),
# }

# # Send the POST request
# response = requests.post(url, headers=headers, files=files)

# # Check the response
# if response.status_code == 201:
#     print("Request sent successfully!")
#     playNoteId = response.json().get('id')
#     print(f"Generated PlayNote ID: {playNoteId}")
# else:
#     print(f"Failed to generate PlayNote: {response.text}")
#     playNoteId = None

# # Ensure playNoteId is defined before proceeding
# if playNoteId:
#     import urllib.parse
#     import time

#     # Double-encode the PlayNote ID for the URL
#     double_encoded_id = urllib.parse.quote(playNoteId, safe='')

#     # Construct the final URL to check the status
#     status_url = f"https://api.play.ai/api/v1/playnotes/{double_encoded_id}"

#     # Poll for completion
#     while True:
#         response = requests.get(status_url, headers=headers)
#         if response.status_code == 200:
#             playnote_data = response.json()
#             status = playnote_data['status']
#             if status == 'completed':
#                 print("PlayNote generation complete!")
#                 print("Audio URL:", playnote_data['audioUrl'])
#                 break
#             elif status == 'generating':
#                 print("Please wait, your PlayNote is still generating...")
#                 time.sleep(120)  # Wait for 2 minutes before polling again
#             else:
#                 print("PlayNote creation failed, please try again.")
#                 break
#         else:
#             print(f"Error polling for PlayNote status: {response.text}")
#             break
# else:
#     print("PlayNote ID is not defined. Exiting.")



import requests
# import os
import time

# Set up headers with your API secrety key and user ID
user_id = 'WayNXGmUolfPoRXFuwa5XuIFFmj1'
secret_key = 'ak-1434c93eae2d40c4bd9846e8d5e88bb7'

headers = {
    'X-USER-ID': user_id,
    'Authorization': secret_key,
    'Content-Type': 'application/json',
}

# define the model
model = 'PlayDialog'

# define voices for the 2 hosts
# find all voices here https://docs.play.ai/tts-api-reference/voices
voice_1 = 's3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json'
voice_2 = 's3://voice-cloning-zero-shot/e040bd1b-f190-4bdb-83f0-75ef85b18f84/original/manifest.json'

# podcast transcript should be in the format of Host 1: ... Host 2:
transcript = """
Host 1: Welcome to our podcast on Python Functions and Arguments! Today, we're going to dive deep into the different types of arguments that can be passed to a function in Python.

Host 2: That's right! Arguments are values that are used within a function, and they can be passed in different ways. Let's start with Required Arguments.

Host 1: Required arguments are arguments that must be passed to a function when it is called. They are specified in the function definition and must be provided in the correct order.

Host 2: For example, if we have a function that adds two numbers, we would define it with two required arguments.

Host 1: Right. Here's what that might look like:

```
def add_two_numbers(num1, num2):
    return num1 + num2
```

Host 2: Exactly. In this case, `num1` and `num2` are both required arguments, and if we call the function without passing in two arguments, we'll get an error.

Host 1: Now, let's talk about Keyword Arguments.

Host 2: Keyword arguments are arguments that are passed to a function using a keyword. This allows you to specify the argument name along with the value.       

Host 1: Keyword arguments are useful when we want to make our code more readable and easier to understand. Here's an example:

```
def greet(name, salutation="Hello"):
    print(f"{salutation} {name}!")
```

Host 2: In this case, `name` is a required argument, and `salutation` is a keyword argument with a default value of "Hello". We can call the function like this:

```
greet(name="John")
greet(name="John", salutation="Good morning")
```

Host 1: Another type of argument is Default Arguments.

Host 2: Default arguments are arguments that have a default value assigned to them in the function definition. If no value is provided for this argument when the function is called, it will use the default value.

Host 1: Here's an example of a function with a default argument:

```
def get_message(name="World"):
    return f"Hello {name}"
```

Host 2: In this case, the `name` argument has a default value of "World", so if we call the function without passing in a value for `name`, it will return "Hello World".

Host 1: Now, let's talk about Variable-Length Arguments.

Host 2: Variable-length arguments are arguments that can be passed to a function in any order or quantity. This is useful when we want to pass a variable number of arguments to a function.

Host 1: Here's an example of a function with variable-length arguments:

```
def my_function(*args):
    for arg in args:
        print(arg)
```

Host 2: In this example, the function `my_function` takes a variable number of arguments, which are stored in the `args` tuple. The function then prints each argument to the console.

Host 1: And that's a wrap! We've covered the different types of arguments that can be passed to a function in Python.

Host 2: Understanding the different types of arguments is important for writing effective and efficient Python code.

Host 1: Thanks for listening to our podcast on Python Functions and Arguments!

Host 2: Join us next time for another deep dive into the world of programming.
"""

payload = {
    'model': model,
    'text': transcript,
    'voice': voice_1,
    'voice2': voice_2,
    'turnPrefix': 'Host 1:',
    'turnPrefix2': 'Host 2:',
    'outputFormat': 'mp3',
}

# Send the POST request to trigger podcast generation
response = requests.post('https://api.play.ai/api/v1/tts/', headers=headers, json=payload)

# get the job id to check the status
job_id = response.json().get('id')

# use the job id to check completion status
url = f'https://api.play.ai/api/v1/tts/{job_id}'
print(url)
delay_seconds = 10

# keep checking until status is COMPLETED.
# longer transcripts take more time to complete.
while True:
    response = requests.request('GET', url, headers=headers)

    if response.ok:
        status = response.json().get('output', {}).get('status')
        print(status)
        if status == 'COMPLETED':
            # once completed audio url will be avaialable
            podcast_audio = response.json().get('output', {}).get('url')
            break
        print("Still processing...")
    time.sleep(delay_seconds)

print(podcast_audio)
