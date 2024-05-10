# -*- coding: utf-8 -*-
import uuid
import requests
import hashlib
import time


YOUDAO_URL = 'https://openapi.youdao.com/ttsapi'
APP_KEY = '6dd2e289581eec52'
APP_SECRET = '1UsMhnrNgOnrNb7kXZrRNK5mdATSbftv'


def encrypt(signStr):
    hash_algorithm = hashlib.md5()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

def split_text(text, max_length=2000):
    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break
        else:
            # Try to break at a sentence ending
            pos = text.rfind('.', 0, max_length)
            if pos == -1:
                pos = max_length
            parts.append(text[:pos + 1])
            text = text[pos + 1:]
    return parts

def text_to_speech(text):
    parts = split_text(text)
    all_file_paths = ''
    for part in parts:
        data = {}
        data['langType'] = 'en'
        salt = str(uuid.uuid1())
        signStr = APP_KEY + part + salt + APP_SECRET
        sign = encrypt(signStr)
        data['appKey'] = APP_KEY
        data['q'] = part
        data['salt'] = salt
        data['sign'] = sign

        response = do_request(data)
        
        contentType = response.headers['Content-Type']
        if contentType == "audio/mp3":
            millis = int(round(time.time() * 1000))
            filePath = "D:/workspace/foreign_magazine_repo/frontend/public/audio/audio_" + str(millis) + ".mp3"
            result = "/audio/audio_" + str(millis) + ".mp3"
            all_file_paths += result + ','
            with open(filePath, 'wb') as fo:
                fo.write(response.content)
            print("Audio saved to", filePath)
            
        else:
            print("Failed to retrieve audio:", response.content)
    return all_file_paths

# Example usage
# if __name__ == '__main__':
#     text = '''
# In May 2022, Liu recorded another video, singing the English children's song Row, Row, Row Your Boat while on a bamboo raft on the Yulong River in Yangshuo. Once again, his infectious accent captivated viewers, earning a staggering 3 million likes. The song became one of the most popular background tracks on Douyin. "My song has become so popular that it has reached Paris and New York," Liu remarked. Within days, his fan base surpassed 1 million, and he was affectionately dubbed "Shank Q Brother" by his supporters.
# In the months following the video's release, Liu encountered a range of opinions online. Initially, some mocked his accent, others accused him of deliberately mispronouncing the words to attract attention and some even resorted to hate speech. However, as Liu's story gained media attention and his background gradually came to light, the negative voices transformed into ones of genuine respect and support. He has emerged as an inspirational figure, symbolizing perseverance in the face of adversity, as he learned English while tending to cows and studied in a cave.

# '''
#     # text_to_speech(text)
