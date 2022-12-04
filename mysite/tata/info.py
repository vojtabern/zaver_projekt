from tata.models import basicInfo

def get_information(request):
    if(request.method == 'GET'):
        return {"informace": basicInfo.objects.all()}
    elif(request.method == 'POST'):
        return {}

def check_async(request):
  ctx = {}
  if 'async' in request.get_full_path():
    ctx['async'] = True
  return ctx






