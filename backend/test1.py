def format_dialogue_for_gpt(dialogue_history):
    formatted_history = ""
    for entry in dialogue_history:
        for role, text in entry.items():
            formatted_history += f"{role}: {text}\n"
    return formatted_history

# 假设的对话历史
dialogue_history = [
    {'user': 'How is the weather today?'},
    {'assistant': 'It is quite sunny today.'},
    {'user': 'Do you recommend any outdoor activity?'},
]

# 格式化对话历史为字符串
formatted_history = format_dialogue_for_gpt(dialogue_history)

# 新的用户输入
new_user_input = {'user': 'What about tomorrow?'}

# 更新对话历史
dialogue_history.append(new_user_input)

# 再次格式化对话历史
formatted_history = format_dialogue_for_gpt(dialogue_history)

print(formatted_history,type(formatted_history))
