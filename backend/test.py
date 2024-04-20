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
        model="gpt-3.5-turbo-0125"
    )
    result = response.choices[0].message.content
    #print(result)
    
    # 移除反引号
    PATTERN = re.compile(r"(.*?\s)\[|(`{3})")
    cleaned_result = re.sub(PATTERN, '', result)
    # print(cleaned_result)
    # print(type(cleaned_result))
    # 使用json.loads()将字符串解析成Python对象
    data = json.loads(cleaned_result)
    # print(data)
    # print(type(data))

    # # 打印每个术语及其定义
    for item in data:
        print(f"Term: {item['term']}, Definition: {item['definition']}")
    

    # 遍历 entries 列表，打印每个条目的 term 和 definition
    # for entry in entries:
    #     print(f"Term: {entry['term']}")
    #     print(f"Definition: {entry['definition']}")
    #     print()  # 打印空行以分隔条目

art_text = '''Chinese President Xi Jinping meets with German Chancellor Olaf Scholz at the Diaoyutai State Guesthouse in Beijing, capital of China, on April 16 (XINHUA)
Chinese President Xi Jinping met with German Chancellor Olaf Scholz on April 16 at the Diaoyutai State Guesthouse in Beijing, calling on the two sides to carry forward the distinctive characteristics of mutual benefit and win-win outcomes and achieve mutual success.
Noting that this year marks the 10th anniversary of the establishment of the all-round strategic partnership between China and Germany, Xi said over the past 10 years, despite tremendous changes in the international landscape, China-Germany relations have maintained steady growth, and bilateral cooperation has strengthened and deepened across the board, providing impetus for the development of both countries.
Currently, transformation not seen in a century is accelerating across the globe, and humanity faces growing risks and challenges. These problems can not be resolved without major-country cooperation, Xi said.
As China and Germany are respectively the second and third largest economies in the world, the consolidation and development of their relations carries significance that goes beyond the bilateral scope, and has a major impact on the Eurasian continent and the entire world, Xi said, calling on the two countries to view and develop bilateral relations from a long-term and strategic perspective, and work together to inject greater stability and certainty into the world.
He underscored that both China and Germany have made major contribution to the progress of human civilization. The two countries do not have clashing fundamental interests between them and pose no security threat to each other. Cooperation between China and Germany benefits not just the two sides but also the world at large.
The more instability in the world, the greater the need for the two sides to strengthen the resilience and vitality of their relations, Xi said, calling for joint efforts to keep to the overall direction of cooperation and development in growing bilateral ties, and stick to the characterization of all-round strategic partnership.
China's policy toward Germany is highly stable and consistent, Xi said, noting that the two sides need to continue engaging in close exchanges with an open mind and enhance strategic mutual trust. As long as the two sides uphold mutual respect, seek common ground while reserving differences, enhance exchanges and mutual learning, and pursue win-win cooperation, China-Germany relations will continue to enjoy solid and sustained progress.
Xi noted that the industrial and supply chains of China and Germany are deeply intertwined, and that the markets of the two countries are highly interdependent. Mutually beneficial cooperation between China and Germany is not a "risk," but the guarantee for a stable bilateral relationship and an opportunity for the future.
There is huge potential to be tapped for pursuing win-win cooperation in both traditional sectors such as machinery and automobile, and new areas such as green transition, digitization and artificial intelligence, Xi said.
It is important for the two sides to promote the win-win features of their relations and enable each other to succeed, Xi said, adding that China's export of electric vehicles, lithium batteries and photovoltaic products has not only enriched global supply and eased global inflationary pressure, but also made important contribution to the global response to climate change and the green and low-carbon transition.
Noting that both China and Germany are countries built on industries, and both support free trade and economic globalization, Xi said it is important for the two countries to stay vigilant against the rise of protectionism, adopt an objective and dialectical view on the issue of production capacity through a market and global perspective and based on the laws of economics, and devote more efforts to the discussion on cooperation.
China is committed to the basic national policy of opening up, and hopes that the German side can provide a fair, transparent, open and non-discriminatory business environment for Chinese enterprises in Germany, Xi said.
Underscoring that China and Germany share a lot in common on the issue of world multipolarity, Xi pointed out that a multipolar world is, in essence, one where countries with different civilizations, systems and paths respect each other and coexist in peace.
He said China and Germany need to independently carry out collaboration on multilateral fronts, push the international community to take real actions to better address global challenges such as climate change, unbalanced development and regional conflicts, and make greater contribution to the balance and stability of the world.
For his part, Scholz noted that Germany-China relations are now in good shape. The two countries have had close exchanges at all levels and in all fields. The two sides successfully held the intergovernmental consultation and high-level dialogues on strategic and financial issues, and will hold a dialogue on climate change and green transition.
In the past two days, he visited Chongqing and Shanghai together with representatives of the German business community, and witnessed the great economic progress China made over recent years, Scholz said. He added he was particularly impressed by the close and sound cooperation between German and Chinese businesses.
Going forward, the German side will work with the Chinese side to strengthen bilateral ties, deepen dialogue and cooperation in all fields, and promote people-to-people exchanges in such areas as education and culture, which is important for both countries and the world at large, he said.
The German side stands ready to enhance communication and coordination with the Chinese side to jointly tackle climate change and other global challenges, commits to upholding the multilateral international order and promoting world peace and development, and disapproves of conflict and confrontation, Scholz said, adding that Germany opposes protectionism and supports free trade.
As an important member of the European Union, Germany is ready to play a positive role in promoting the sound development of EU-China relations, Scholz said.
The two leaders also had an in-depth exchange of views on the Ukraine crisis, noting that both China and Germany stand committed to the purposes and principles of the UN Charter, oppose the use of nuclear weapons or attack on peaceful nuclear facilities, and call for efforts to properly address the issue of global food security and observe the international humanitarian law.
Xi underscored that under the current circumstances, all parties should commit to an early restoration of peace to prevent the conflict from escalating and even spiraling out of control.
To this end, a number of principles should be followed: first, focusing on the overall interest of peace and stability rather than seeking selfish gains; second, cooling down the situation rather than adding fuel to the fire; third, accumulating conditions for restoring peace rather than further aggravating tensions; and fourth, reducing the negative impact on the world economy rather than undermining the stability of global industrial and supply chains.
China is not a party to the Ukraine crisis, but has consistently promoted talks for peace in its own way, Xi said, China encourages and supports all efforts that are conducive to the peaceful resolution of the crisis, and supports the holding in due course of an international peace conference that is recognized by both Russia and Ukraine and ensures the equal participation of all parties and fair discussions on all peace plans.
China will maintain close communication with all parties concerned, including Germany, on this matter, Xi said.
The two sides also exchanged views on the Palestinian-Israeli conflict and other international and regional issues of mutual interest. The two sides shared the view that it is important to implement UNSC Resolution 2728, prevent escalation and further deterioration of the situation, ensure unhindered and sustained humanitarian access to Gaza, support the early settlement of the Palestinian question through negotiations on the basis of the two-State solution, and call on countries with influence to play a constructive role in maintaining regional peace and stability, with a view to achieving a comprehensive, just and lasting solution to the question of Palestine at an early date.
Following the meeting, Xi and Scholz took a walk and had lunch together, during which they further exchanged views on a wide range of issues.
Chinese President Xi Jinping meets with German Chancellor Olaf Scholz at the Diaoyutai State Guesthouse in Beijing, capital of China, on April 16 (XINHUA)
Chinese President Xi Jinping and German Chancellor Olaf Scholz take a walk in Beijing, capital of China, on April 16. Xi met with German Chancellor Olaf Scholz at the Diaoyutai State Guesthouse in Beijing on April 16 (XINHUA)
Chinese President Xi Jinping and German Chancellor Olaf Scholz pose for a photo in Beijing, capital of China, on April 16. Xi met with German Chancellor Olaf Scholz at the Diaoyutai State Guesthouse in Beijing on April 16 (XINHUA)
'''

role_setting = 'You are an AI with excellent language skills and extensive reading of various foreign magazines. Your goal is to help users better understand the text.'
prompt = f'''
    Your task is to perform the following actions:
    1 - Extract the difficult words, culturally loaded terms, and important phrases from the text, enclosed by <>, especially those words that are difficult to understand for non-native speakers.
    2 - Provide a brief definition or explanation of the extracted terms or phrases according to the context.
    3 - Format the output as a list of dictionaries, where each dictionary contains two key-value pairs: "term" and "definition". Ensure each term and its corresponding definition are enclosed in a separate dictionary. The list should look like this:
        [
            {{"term": "the word or phrase extracted", "definition": "the definition or explanation of the word or phrase"}},
            {{"term": "another word or phrase extracted", "definition": "its definition or explanation"}}
        ]
    <{art_text}>
'''

call_gpt(role_setting, prompt)