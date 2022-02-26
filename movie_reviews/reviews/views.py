from django.shortcuts import render
from django.views import View
from django.conf import settings
import requests
import json
API_URL = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json'
# Create your views here.
def index(request):
	return render(request, "reviews/index.html")


class Reviews(View):
	
	template_name = "reviews/index.html"
	def get(self, request):
		res = requests.get(API_URL, params={'api-key': settings.NYT_API_KEY, 'critics-pick':'Y'})
		print(res.request.url)
		print(res.request.body)
		print(res.request.headers)
		print(res)
		content = {}
		if res.ok:
			# limit to 10 reviews
			content['data'] = res.json()['results']
			print(type(content['data'][0]))
		return render(request, self.template_name, content)
		