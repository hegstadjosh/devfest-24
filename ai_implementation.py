import os
import openai
from openai import OpenAI
import json
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import g4f
import ai_test

song_metrics = ["gratitude", "goal-orientation", "social-support", "happiness", "anger", "satisfaction", "self-esteem" ]
sys_msg = "You are a text analysis machine. You read journal entries of users and try to analyze them for mental health markers. Grade the following criteria from 0 to 9 (0 is least healthy): {metrics} in the format \"gratitude\":0 . The default value is -1 (not enough info to grade)."
example_diary_1 = "Today was a pretty good day. I had a math test in the morning, and I think I did well. I studied hard for it, and I remembered most of the formulas. I hope I get a good grade. \
After school, I hung out with my friends at the park. We played some soccer and had a lot of fun. I'm glad I have such supportive and kind friends. They always cheer me up when I'm feeling down. \
When I got home, I helped my mom with dinner. She made my favorite dish, lasagna. It was delicious. I thanked her for cooking and told her I love her. She smiled and hugged me. I'm grateful for my family and how they care for me. \
Before going to bed, I watched some TV and read a book. I'm currently reading Harry Potter and the Prisoner of Azkaban. It's so exciting and magical. I can't wait to finish it and see what happens next."
ast_response_1 = "\"gratitude\":9\n\"goal-orientation\":3\n\"social-support\":7\n\"happiness\":8\n\"anger\":1\n\"satisfaction\":8\n\"self-esteem\":-1"
example_diary_2 = "Today was another awful day. I had a paper due in the afternoon, and I barely finished it. I didn't have time to proofread or edit it. I know I'm going to get a bad grade. \
After class, I went back to my dorm and stayed in my room. I didn't feel like talking to anyone. I don't have any real friends here. They all seem to have their own lives and interests. I feel so alone and isolated. \
When I got hungry, I ordered some pizza and ate it by myself. It was greasy and cold. I didn't enjoy it at all. I felt guilty for wasting money and calories. I hate my body and how I look. \
Before going to sleep, I tried to distract myself with some Netflix and social media. But nothing made me happy. I saw everyone else posting about their achievements and adventures. They all seem to have it so easy and fun. I can't help but compare myself and feel inadequate."

messages=[
    {"role": "system", "content": sys_msg},
    {"role": "user", "content": example_diary_1},
    {"role": "assistant", "content": ast_response_1},
    {"role": "user", "content": example_diary_2}
  ]

chat_response = ai_test.chat_completion_request(
    messages=messages
)
assistant_message = chat_response.json()["choices"][0]["message"]
messages.append(assistant_message)
ai_test.pretty_print_conversation(messages)

