import sys
from tata.models import basicInfo

import aiohttp, random, time, asyncio


def get_information(request):
    if request.method == 'GET':
        return {"informace": basicInfo.objects.all()}
    elif request.method == 'POST':
        return {}


def check_async(request):
  ctx = {}
  if 'async' in request.get_full_path():
    ctx['async'] = True
  return ctx


async def get_quotes():
    kill_me = {}
    URL = 'https://zenquotes.io/api/quotes/authors'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as res:
            data = await res.json()
            for d in range(len(data)):
                i = d
            rand = random.randrange(0, i)
            kill_me.update({'quote':data[rand]["q"]})
            kill_me.update({'autor':data[rand]["a"]})
            print(kill_me)

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


