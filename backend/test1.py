from openai import OpenAI
import json
import re

def call_gpt(role_setting, prompt):
    client = OpenAI(
        api_key="sk-AfYIYMRHxLdKnMew1fF6E0F6D2C54e2eAc26BaE6135046Bd",
        base_url="https://api.openai.com/v1"
    )
    client.base_url="https://ai-yyds.com/v1"

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": role_setting},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo-0125",
    )
    result = response.choices[0].message.content
    print(result)
    
    
sentence = '''
A treasure trove of 38 pieces of Chinese cultural relics, once lost but now on the cusp of returning to their ancestral homeland from New York, serves as a poignant symbol of the profound bond and goodwill shared between the American and Chinese people.
'''

role_setting = 'You are an AI with excellent language skills and extensive reading of various foreign magazines. Your goal is to help users better understand the text.'
prompt = f'''
    Your task is to analyze the sentence enclosed by <> to explain the grammatical structure and provide a detailed explaination of this sentence.
    <{sentence}>
'''

call_gpt(role_setting, prompt)