import sys
from tata.models import basicInfo

import aiohttp, random, time, asyncio


def get_information(request):
    if request.method == 'GET':
        return {"informace": basicInfo.objects.all()}
    elif request.method == 'POST':
        return {}


async def get_quotes():
    kill_me = {}
    URL = 'https://zenquotes.io/api/quotes/authors'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as res:
            data = await res.json()

            rand = random.randrange(0, len(data))
            kill_me.update({'quote':data[rand]["q"]})
            kill_me.update({'autor':data[rand]["a"]})
            print(kill_me)
            if(rand > len(data)):
                rand = len(data) - random.randrange(0, len(data)-1)

        await session.close()

        return kill_me


def pokus(request):
    kokos = asyncio.run(get_quotes())

    print(kokos)

    return kokos

# async def pokus(request):
#     qoute = get_quotes()
#     kokos = await qoute.__anext__()
#     return kokos
#
#



# async def get_qoutes(request):
#     got = Uryvky.get(self="index", request=request)
#     print(got)

# async def quotes(request):
#     if request=='GET':
#         URL = 'https://zenquotes.io/api/quotes/authors'
#         async with aiohttp.ClientSession() as session:
#             async with session.get(URL) as res:
#                 data = await res.json()
#                 for d in range(len(data)):
#                     i = d
#                 print(data[0]["q"])
#                 rand = random.randrange(0, i)
#                 context = {
#                     "quote": data[rand]["q"],
#                     "autor": data[rand]["a"],
#                 }
#         return context
#     else:
#         return {}


