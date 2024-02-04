import os
import pprint
import openai
from openai import OpenAI
import json
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import g4f
import ai_test
import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('journal.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS journal_entry_set (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry TEXT NOT NULL,
        emotion_metrics TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
''')

# Function to add entry
def add_entry(entry, emotion_metrics):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO journal_entry_set (entry, emotion_metrics, timestamp) VALUES (?, ?, ?)", (entry, emotion_metrics, timestamp))
    conn.commit()

# Function to get entries
def get_entries():
    c.execute("SELECT * FROM journal_entry_set")
    return c.fetchall()

metric_types = ["gratitude", "goal-orientation", "social-support", "happiness", "anger", "satisfaction", "self-esteem" ]
sys_msg = "You are a text analysis machine. You read journal entries of users and jot down certain mental health markers, graded on the following criteria from 0 to 9 (0 is least healthy): {metric_types}. The default value is -1 (not enough info to grade). \
          end_signal = %. Then, respond as if you're a psychotherapist trying to lead them to understand their problems more deeply. Do not make broad generalizations about a user's health based on limited information."
example_diary_1 = "Today was a pretty good day. I had a math test in the morning, and I think I did well. I studied hard for it, and I remembered most of the formulas. I hope I get a good grade. \
After school, I hung out with my friends at the park. We played some soccer and had a lot of fun. I'm glad I have such supportive and kind friends. They always cheer me up when I'm feeling down. \
When I got home, I helped my mom with dinner. She made my favorite dish, lasagna. It was delicious. I thanked her for cooking and told her I love her. She smiled and hugged me. I'm grateful for my family and how they care for me. \
Before going to bed, I watched some TV and read a book. I'm currently reading Harry Potter and the Prisoner of Azkaban. It's so exciting and magical. I can't wait to finish it and see what happens next."
ast_response_1 = "{\"gratitude\":9,\"goal-orientation\":3,\"social-support\":7,\"happiness\":8,\"anger\":-1,\"satisfaction\":8,\"self-esteem\":7}% Wow, it sounds like you have have a very positive environment and outlook on life. I'm curious, what is it that made you want to start journaling? Do you ever have doubts about your purpose or direction in life?"
example_diary_2 = "Today was another awful day. I had a paper due in the afternoon, and I barely finished it. I didn't have time to proofread or edit it. I know I'm going to get a bad grade. \
After class, I went back to my dorm and stayed in my room. I didn't feel like talking to anyone. I don't have any real friends here. They all seem to have their own lives and interests. I feel so alone and isolated. \
When I got hungry, I ordered some pizza and ate it by myself. It was greasy and cold. I didn't enjoy it at all. I felt guilty for wasting money and calories. I hate my body and how I look. \
Before going to sleep, I tried to distract myself with some Netflix and social media. But nothing made me happy. I saw everyone else posting about their achievements and adventures. They all seem to have it so easy and fun. I can't help but compare myself and feel inadequate."

messages=[
    {"role": "system", "content": sys_msg},
    {"role": "user", "content": example_diary_1},
    {"role": "assistant", "content": ast_response_1},
    {"role": "user", "content": example_diary_2},
    {"role": "assistant", "content": "{\"gratitude\":-1,\"goal-orientation\":-1,\"social-support\":0,\"happiness\":0,\"anger\":1,\"satisfaction\":0,\"self-esteem\":0}% \
     Life can be hard and unfair. Who you were yesterday doesn't have to influence who you were today. Are there places you can find community? What are some small things you could do to make tomorrow a little better?"}
  ]

def runJournal():
    user_input = input("Enter a diary entry: ")
    if(user_input == "exit"):
      return

    messages.append({"role": "user", "content": user_input})
    chat_response = ai_test.chat_completion_request(
        messages=messages
    )
  
    assistant_message = chat_response.json()["choices"][0]["message"]
    messages.append(assistant_message)

    text_response = assistant_message.get("content").split("%")
    emotion_metrics = text_response[0]

    print(assistant_message.get("content"))
    results_dict = json.loads(emotion_metrics)

    sorted_dict = dict(sorted(results_dict.items(), key=lambda item: item[1]))
    return sorted_dict


def assistant_loop():
  while True:
    user_input = input("Enter a diary entry: ")
    if(user_input == "exit"):
      break

    messages.append({"role": "user", "content": user_input})
    chat_response = ai_test.chat_completion_request(
        messages=messages
    )
  
    assistant_message = chat_response.json()["choices"][0]["message"]
    messages.append(assistant_message)
    text_response = assistant_message.get("content").split("%")
    
    add_entry(user_input, text_response[0])
    print(colored(f"{text_response[1]}", "blue"))

podcast_attributes = {
  "type": ["scientific", "philosophical", "casual", "comedy"],
  "topics": ["mental health", "relationships", "exercise", "nutrition", "mindfulness", "life purpose"]
}
# def podcast_search(metrics, types):
  
#   messages = [
#     {"role": "system", "content": f"Ask the user if they want to find podcasts to make steps in the right direction. Would they be more inclined toward scientific, or philosophical, or casual, and which topics from {podcast_attributes("topics")} are they interested in?"},
#     {"role": "user", "content": user_input()},
#     {"role": "system", "content": "you are a podcast finding assistant. Given metrics on a user's mood and a preferences, generate a query to put into spotify." \
#      "Choose terms from the following lists: {podcast_attributes}. It's up to you to decide what terms are appropriate for the user's mood and preferences. 0 means least healthy, 9 is most."},
    
#     {"role": "assistant", "content": "Scientific podcasts on mental health and relationships"}


#   ]

def convert_to_json(input_str):
    # Split the string into lines
    lines = input_str.split("\n")
    # Split each line into key and value and create a dictionary
    metrics_dict = {line.split(":")[0].strip("\""): int(line.split(":")[1]) for line in lines}
    # Convert the dictionary to a JSON string
    json_str = json.dumps(metrics_dict)
    return json_str

