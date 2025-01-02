import sqlite3
from groq import Groq
import requests
import time

def generate_podcast(username, title, topic):
    # ...existing imports...
    client = Groq(api_key='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')
    
    # Fetch the assistant's first response from the chat history
    query = '''
    SELECT content FROM chat_history WHERE username = ? AND title = ? AND topic = ? AND role = 'assistant' 
    ORDER BY timestamp ASC LIMIT 1'''
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute(query, (username, title, topic))
    response = cursor.fetchone()
    conn.close()
    
    if not response:
        return None  # No content to generate podcast
    
    # Generate podcast script using AI
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": f"""
                Give me a Podcast Friendly Discussion Script for 2 hosts format. The podcast has to be a deep dive of the given Topic & Data: {response[0]}.
                Give at least 20 dialogues for each host. Make it a beginner-friendly, long podcast without technical jargon.
                The script should be formatted like:
                Host 1: ...
                Host 2: ...
                After ending the script, write "Thank you for listening to the podcast."
                Only provide the script; any other information is invalid.
                """
            }
        ],
        temperature=1,
        max_tokens=5000,
        top_p=0.7,
        stream=False,
        stop=None,
    )
    
    generated_transcript = completion.choices[0].message.content.strip()
    print(generated_transcript)
    
    # Set up headers for API requests
    user_id = 'WayNXGmUolfPoRXFuwa5XuIFFmj1'
    secret_key = 'ak-1434c93eae2d40c4bd9846e8d5e88bb7'
    headers = {
        'X-USER-ID': user_id,
        'Authorization': secret_key,
        'Content-Type': 'application/json',
    }
    
    # Define voices and model
    model = 'PlayDialog'
    voice_1 = 's3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json'
    voice_2 = 's3://voice-cloning-zero-shot/e040bd1b-f190-4bdb-83f0-75ef85b18f84/original/manifest.json'
    
    payload = {
        'model': model,
        'text': generated_transcript,
        'voice': voice_1,
        'voice2': voice_2,
        'turnPrefix': 'Host 1:',
        'turnPrefix2': 'Host 2:',
        'outputFormat': 'mp3',
    }
    
    # Send request to generate podcast audio
    response_url = requests.post('https://api.play.ai/api/v1/tts/', headers=headers, json=payload)

    if response_url:
        job_id = response_url.json().get('id')
        print(job_id)
    
    # Poll for completion
        url = f'https://api.play.ai/api/v1/tts/{job_id}'
        print(url)

    return url

def check_podcast_status(job_id):
    user_id = 'WayNXGmUolfPoRXFuwa5XuIFFmj1'
    secret_key = 'ak-1434c93eae2d40c4bd9846e8d5e88bb7'
    headers = {
        'X-USER-ID': user_id,
        'Authorization': secret_key,
        'Content-Type': 'application/json',
    }
    
    url = f'https://api.play.ai/api/v1/tts/{job_id}'
    delay_seconds = 10

    while True:
        response = requests.get(url, headers=headers)

        if response.ok:
            status = response.json().get('output', {}).get('status')
            # print(status)
            if status == 'COMPLETED':
                podcast_audio = response.json().get('output', {}).get('url')
                return podcast_audio
            # print("Still processing...")
        time.sleep(delay_seconds)
