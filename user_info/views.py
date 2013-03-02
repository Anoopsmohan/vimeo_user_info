import requests

from user_info.models import UserDetails
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string


def home(request):
    return render_to_response('home.html')

def fetch_info(request):
    if request.GET.get('limit'):
        base_id = 406307
        count = 0
        while(1):
            try:
                base_id += 1
                info = requests.get('http://vimeo.com/api/v2/%s/info.json' % str(base_id)).json
                if UserDetails.objects.filter(profile_url=info['profile_url']).exists():
                    continue
                user_info = UserDetails()
                user_info.name = info['display_name']
                user_info.profile_url = info['profile_url']
                user_info.paying = int(info['is_plus'])
                user_info.staff_pick = False
                if int(info['total_channels']) > 0:
                    channel_info = requests.get('http://vimeo.com/api/v2/%s/channels.json' % str(base_id)).json
                    for i in channel_info:
                        if i['id'] == 927:
                            user_info.staff_pick = True
                            break
                else:
                    user_info.staff_pick = False
                if int(info['total_videos_uploaded']) >= 0:
                    user_info.video_uploaded = 1
                else:
                    user_info.video_uploaded = 0
                user_info.save()
                count += 1
                if count >= int(request.GET.get('limit')):
                    break
            except:
                continue
        return HttpResponse('User Details added')

    elif int(request.GET.get('clean')) == 1:
        UserDetails.objects.all().delete()
        messages.success(request, 'User details removed from the database')
        return HttpResponse('User Details Deleted')


def get_results(request):
    if request.GET.get('search_text'):
        results = UserDetails.objects.filter(name__contains=request.GET.get('search_text')).order_by('name')
        search_results = render_to_string('search_results.html', {'results': results[:100], 'search_count': results.count()})
        return HttpResponse(search_results)
