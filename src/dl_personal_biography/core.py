'''
Author: 823042332@qq.com 823042332@qq.com
Date: 2025-09-01 10:15:21
LastEditors: 823042332@qq.com 823042332@qq.com
LastEditTime: 2025-09-03 14:49:17
FilePath: /dl_personal_biography/src/dl_personal_biography/core.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import time
import asyncio
import json
from dl_personal_biography.utils import extract_json, extract_article
from dl_personal_biography.prompt import prompt_get_infos, prompt_base
from dl_personal_biography.prompt import outline_prompt
from dl_personal_biography.prompt import interview_material_clean_prompt, interview_material_add_prompt
from dl_personal_biography.prompt import memory_card_system_prompt
from llmada.core import BianXieAdapter



class BiographyGenerate():
    def __init__(self):
        model_name = "gemini-2.5-flash-preview-05-20-nothinking"
        bx = BianXieAdapter()
        bx.model_pool.append(model_name)
        bx.set_model(model_name=model_name)
        self.bx = bx

    def material_generate(self,vitae:str,memory_cards:str)->str: # 简历, 
        """
        素材整理
        vitae : 简历
        memory_cards : 记忆卡片们
        """
        def split_into_chunks(my_list, chunk_size = 5):
            """
            使用列表推导式将列表分割成大小为 chunk_size 的块。
            """
            return [my_list[i:i + chunk_size] for i in range(0, len(my_list), chunk_size)]

        # --- 示例 ---
        chunks = split_into_chunks(memory_cards, chunk_size = 5)

        material = ""
        for i,chunk in enumerate(chunks):
            if i == 0:
                material = self.bx.product(interview_material_clean_prompt + vitae + chunk)
            else:
                material = self.bx.product(interview_material_add_prompt + "#素材:\n" + material + "#记忆卡片:\n" + chunk)
        return material


    def outline_generate(self,material:str)->str:
        """
        大纲生成
        """
        outline = self.bx.product(outline_prompt + material)
        return outline


    async def agenerate_memory_card(self,chat_history_str:str, weight:int = 1000):
        
        number_ = len(chat_history_str)//weight

        
        base_prompt = memory_card_system_prompt.format(number = number_) + chat_history_str
        try:
            result = await asyncio.to_thread(self.bx.product, base_prompt) 
            result_json_str = extract_json(result)

            if result_json_str:
                return json.loads(result_json_str), chat_history_str
            else:
                return ""
        except Exception as e:
            print(f"Error processing  {chat_history_str[:30]}: {e}")
            return ""



    async def awrite_chapter(self,info,master = "",material_all = "", 
                             outline:dict = {},suggest_number_words = 3000):
        created_material =""
        try:
            material_prompt = prompt_get_infos.format(material= material_all,frame = json.dumps(outline), requirements = json.dumps(info))
            material = await asyncio.to_thread(self.bx.product, material_prompt) 
            words = prompt_base.format(master = master, chapter = f'{info.get("chapter_number")} {info.get("title")}', topic = info.get("topic"),
                                number_words = suggest_number_words,material = material ,reference = "",port_chapter_summery = '' )
            article = await asyncio.to_thread(self.bx.product, words) # Python 3.9+
            return extract_article(article), material, created_material
        except Exception as e:
            print(f"Error processing chapter {info.get('chapter_number')}: {e}")
            return None


    async def parallel_create_mode(self,version = "V4-4",
                                outline = {}, # 大纲
                                material_all:str  = "", # 自传素材

                                    ):
        # path 
        path = f"/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/TODO/马恪{version}.md"
        material_path = f"/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/TODO/马恪{version}_material.md"
        tasks = []
        for bu,chapter in outline.items():
            for info in chapter:
                print(f"Creating task for chapter: {info.get('chapter_number')} {info.get('title')}")
                tasks.append(awrite_chapter(info,material_all = material_all,outline = outline))
        results = await asyncio.gather(*tasks, return_exceptions=False) 




        
        results[30] = ("1","2","3")


        i = 1
        t = 0

        tt1 = []
        content = "" + str(time.time()) + "\n"
        material = "" + str(time.time()) + "\n"
        for bu,chapter in outline.items():
            content += f'# {bu}'
            content += "\n"
            material += f'# {bu}'
            material += "\n"
            tt1+=chapter
            
            # print("#",bu)
            t += len(chapter)
            while True:
                # print(i)
                content += results[i-1][0]
                content += "\n"
                material += results[i-1][1]
                material += "\n\n"
                material += results[i-1][2]
                material += "\n\n"
                # print(results[i-1])
                i +=1
                if i > t:
                    break

        with open(path,'w') as f:
            f.write(content)

        with open(material_path,'w') as f:
            f.write(material)

