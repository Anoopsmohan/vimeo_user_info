import requests
import re

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.db.models import Max

from user_info.models import UserDetails


def home(request):
    """ Render home page """
    return render_to_response('home.html')

def get_info(limit):
    """ Fetch info by using vimeo API's and store it in database"""

    if UserDetails.objects.count() > 0:
        base_id = UserDetails.objects.aggregate(max_id=Max('user_id'))['max_id']
    else:
        base_id = 406307
    count = 0
    while(1):
        try:
            base_id += 1
            info = requests.get('http://vimeo.com/api/v2/%s/info.json' % str(base_id)).json()
            if UserDetails.objects.filter(profile_url=info['profile_url']).exists():
                continue
            user_info = UserDetails()
            user_info.name = info['display_name']
            user_info.user_id = info['id']
            user_info.profile_url = info['profile_url']
            user_info.paying = int(info['is_plus'])
            user_info.staff_pick = False
            videos = requests.get('http://vimeo.com/api/v2/%s/videos.json' % str(base_id)).json()
            for video in videos:
                response = requests.get(video['url'])
                staff_pick = re.search('"name":"staffpicks"', response.content)
                if staff_pick:
                    user_info.staff_pick = True
                    user_info.staff_pick_url = video['url']
                    break
            if int(info['total_videos_uploaded']) > 0:
                user_info.video_uploaded = 1
            else:
                user_info.video_uploaded = 0
            user_info.save()
            count += 1
            if count >= limit:
                break

        except:
            continue

def delete_info():
    """ Delete user details from database """
    UserDetails.objects.all().delete()


def fetch_info(request):
    if request.GET.get('limit'):
        get_info(int(request.GET.get('limit')))
        return HttpResponse('User Details added')

    elif int(request.GET.get('clean')) == 1:
        delete_info()
        return HttpResponse('User Details Deleted')


def get_results(request):
    if request.GET.get('search_text'):
        if request.GET.get('action') == 'search':
            results = UserDetails.objects.filter(name__icontains=request.GET.get('search_text')).order_by('name')
        elif request.GET.get('action') == 'paying':
            results = UserDetails.objects.filter(name__icontains=request.GET.get('search_text'), paying=True).order_by('name')
        elif request.GET.get('action') == 'staff_pick':
            results = UserDetails.objects.filter(name__icontains=request.GET.get('search_text'), staff_pick=True).order_by('name')
        elif request.GET.get('action') == 'uploaded':
            results = UserDetails.objects.filter(name__icontains=request.GET.get('search_text'), video_uploaded=True).order_by('name')
        if results:
            result = {'results': results[:100], 'search_count': results.count()}
            if request.GET.get('action') == 'staff_pick':
                result['staffpick_url'] = 'true'
            search_results = render_to_string('search_results.html', result)
            return HttpResponse(search_results)
        else:
            message = 'error'
    else:
        message = 'empty_field'
    return HttpResponse(message)
