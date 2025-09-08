'''
Author: 823042332@qq.com 823042332@qq.com
Date: 2025-09-03 14:23:56
LastEditors: 823042332@qq.com 823042332@qq.com
LastEditTime: 2025-09-03 14:41:07
FilePath: /dl_personal_biography/tests/work.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''



from llmada.core import BianXieAdapter
import time
import asyncio
import json
import concurrent.futures # 用于线程池，如果 bx.product 是同步的
from dl_personal_biography.core import awrite_chapter


import asyncio
from demo.mark import 大纲, 自传素材

executor = concurrent.futures.ThreadPoolExecutor(max_workers=20) # 根据需要调整并发度
material_all = 自传素材
outline = 大纲
async def main():
    version = "V4-4"

    path = f"/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/TODO/马恪{version}.md"
    path2 = f"/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/TODO/马恪{version}_material.md"


    tasks = []
    for bu,chapter in outline.items():
        print(bu)
        print(chapter,'chapter')
        for info in chapter:
            # print(info)
            print(f"Creating task for chapter: {info.get('chapter_number')} {info.get('title')}")
            tasks.append(awrite_chapter(info,material_all = material_all,outline = outline))
    tasks = tasks 
    results = await asyncio.gather(*tasks, return_exceptions=False) 

    print(results,'resultsresults')
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

    with open(path2,'w') as f:
        f.write(material)

asyncio.run(main())


executor.shutdown(wait=True)