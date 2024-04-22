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
China will continue to actively fulfill the memorandum of understanding with the United States on preventing the illegal entry of Chinese cultural relics into the United States, and work with the United States to establish a sound mechanism for information sharing on stolen relics, contributing the wisdom and strength of both countries to safeguarding cultural heritage and promoting mutual understanding through cultural exchanges, Li said.
'''

role_setting = 'You are an AI with excellent language skills and extensive reading of various foreign magazines. Your goal is to help users better understand the text.'
prompt = f'''
    Your task is to perfrom the following actions:
    1 - Analyze the sentence enclosed by <> to identify the main clause, retaining only the main part of the sentence and removing any modifying elements.
    2 - Identify any pronouns in the sentence that may require clarification for English learners and determine their referents.
    3 - Discuss any idioms or fixed usages present in the sentence worth mentioning for learners. If there are none, indicate "None" for this part.
    4 - Provide an overall explanation of the sentence to assist English learners in understanding its structure and meaning.
    5 - Output the result in the following format:
        Main clause
        main_clause
        Subject: subject
        Predicate verb: ptrdicate_verb

        Pronouns
        pronoun: referent
        ...

        Idioms and fixed usages
        idiom: explanation
        fixed_usage: explanation
        ...

        Overall explanation for structure and meaning
        Subordinate Clauses:
        subordinate clause
        its explanation
        ...

        Overal explanation
        overall explanation for meaning
    <{sentence}>
    
'''

call_gpt(role_setting, prompt)