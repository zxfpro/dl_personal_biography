


import pandas as pd
from dl_personal_biography.core import BiographyGenerate
import asyncio

from demo.dongsheng import vitae, memory_cards, material


def get_session_message(session_list:list[str]):
    # 最后的结尾已human结尾 当前模式都是以ai作为结尾的, 那么
    # 我们就将最后一句话删除掉
    session_message = ""
    for i,t in enumerate(session_list[:-1]):# ai处理
        if i%2 == 0:
            session_message +=('ai:')
        else:
            session_message += ("human:")
        session_message += (t)
        session_message += '\n'
    return session_message

def get_chat_messages():
    df = pd.read_csv('tests/resource/chat_message.csv')
    chat_history_str_s = [get_session_message(list(session.content)) for i,session in df.groupby('session_id')]
    return chat_history_str_s


async def test_memory_cards():
    bg = BiographyGenerate()
    chat_history_str_s = get_chat_messages()

    tasks = []
    for chat_history_str in chat_history_str_s:
        if not chat_history_str:
            continue
        tasks.append(bg.agenerate_memory_card(chat_history_str))
        print(f"Creating task for chapter: {info.get('chapter_number')} {info.get('title')}")
    results = await asyncio.gather(*tasks, return_exceptions=False) 
    return results

# results = asyncio.run(test_memory_cards())
# print(results,'results')



def test_material_generate():

    bg = BiographyGenerate()
    material = bg.material_generate(vitae, memory_cards)
    return material

# material = test_material_generate()
# print(material,'material')



def test_outline_generate():

    bg = BiographyGenerate()
    outline = bg.outline_generate(material)
    return outline

# outline = test_outline_generate()
# print(outline,'outline')


def test_awrite_chapter():
    bg = BiographyGenerate()




# def test_generate_biograph_by_parallel():
#     pass





####


# async def main():
#     x = get_chat_messages()
#     tasks = []

#     for i in x:
#         if i:
#             print(f"create task {i[:30]}")
#             tasks.append(generate_memory_card(i))
#     results = await asyncio.gather(*tasks, return_exceptions=False) 
#     cp = []
#     for i,orig in s:
#         if i:
#             cp +=i['chapters']

#     cp

#     return results



# if __name__ == "__main__":
#     s = asyncio.run(main())
