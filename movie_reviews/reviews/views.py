from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import JsonResponse
import requests
import json
API_URL = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json'


def load_reviews(query=None, offset=None, critics_pick='Y'):
	res = requests.get(API_URL, params={'api-key': settings.NYT_API_KEY, 'critics-pick':critics_pick, 'offset':offset, 'query':query})
	print(res.request.url)
	print(res.request.body)
	print(res.request.headers)
	print(res)
	return res

class Reviews(View):
	
	template_name = "reviews/index.html"
	def get(self, request):
		content = {}
		res = load_reviews()
		if res.ok:
			# limit to 10 reviews
			content['data'] = res.json()['results']
			print(type(content['data'][0]))
		return render(request, self.template_name, content)

class LoadJSONReview(View):
	def get(self, request, *args, **kwargs):
		offset = kwargs.get('offset')
		res = load_reviews(offset=offset)
		response = {
			'data':  res.json()['results']
		}
		if response['data']:
			return JsonResponse(response, status=200)
		return JsonResponse({}, status = 400)

