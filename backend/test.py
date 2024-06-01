from openai import OpenAI

def call_gpt(role_setting, prompt):
    client = OpenAI(
        api_key="sk-AfYIYMRHxLdKnMew1fF6E0F6D2C54e2eAc26BaE6135046Bd",
        base_url="https://api.openai.com/v1"
    )
    client.base_url="https://ai-yyds.com/v1"

    response = client.chat.completions.create(
        messages=[
            {"role": "assistant", "content": role_setting},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content

result = call_gpt("assistant", "你好")
print(result)