import sys
from tata.models import basicInfo

import aiohttp, random, time, asyncio


def get_information(request):
    if request.method == 'GET':
        return {"informace": basicInfo.objects.all()}
    elif request.method == 'POST':
        return {}

# asynchroní funkce dostane úryvky ze zenqoutes API.
async def get_quotes():
    kill_me = {}
    URL = 'https://zenquotes.io/api/quotes/authors'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as res:
            data = await res.json()
            rand = random.randrange(0, len(data))
            kill_me.update({'quote':data[rand]["q"]})
            kill_me.update({'autor':data[rand]["a"]})
            if(rand > len(data)):
                rand = len(data) - random.randrange(0, len(data)-1)

        await session.close()

        return kill_me

#změna z asynchroní funkce na synchronní,
# aby tyto data šla posílat přes context_processors
# a synchronní přístupy k nim měli přístup
def pokus(request):
    kokos = asyncio.run(get_quotes())
    return kokos


