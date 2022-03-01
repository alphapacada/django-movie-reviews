from django.shortcuts import get_object_or_404, render
from django.db.models.functions import Lower
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
import requests
import json
from .models import Collections, Movie, Bookmark
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import AddToCollectionForm, CreateFolderForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, FormView
from django.core import serializers


API_URL = "https://api.nytimes.com/svc/movies/v2/reviews/search.json"


def load_reviews(user=None, query=None, offset=None, critics_pick=None):
	"""Method to download movie reviews from NYT API.

	Args:
		user (_type_, optional): Current logged in user. Defaults to None.
		query (str, optional): Movie title to search on API. Defaults to None.
		offset (int, optional): Offset for the next 20 movie reviews to request. Defaults to None.
		critics_pick (str, optional):. Defaults to None.

	Returns:
		list: list of dicts containing movie review details
	"""

    res = requests.get(
        API_URL,
        params={
            "api-key": settings.NYT_API_KEY,
            "critics-pick": critics_pick,
            "offset": offset,
            "query": query,
        },
    )

	res.raise_for_status()
	if res.ok:
		
		data = []
		
        for movie in res.json()["results"]:
            obj = {
                "url": movie["link"]["url"],
                "img_src": movie["multimedia"]["src"],
                "display_title": movie["display_title"],
                "bookmarked": False,
            }
			if user:
				# Check if user has bookmarked movie
                mov = Movie.objects.filter(display_title=movie["display_title"])

				if mov.exists():
					if mov[0].check_bookmarked_by(user):
                        obj["bookmarked"] = True
			data.append(obj)
		return data
	
class Reviews(View):
    #
	template_name = "reviews/index.html"

	def get(self, request, title="Home", template_name=None):
        user = request.user
        if user.is_authenticated:
            print("USER AUTHENTICATED")
		if template_name:
			self.template_name = template_name
		query = request.GET.get("q", None)
		content = {}
		res = load_reviews(user=user, query=query)
		if len(res) > 10:
			content["hasMore"] = True
        content["data"] = res
		content["title"] = title
		if title == "Search":
			content["page_title"] = f"Search results for: {query}"
		
		return render(request, self.template_name, content)

class LoadJSONReview(View):
	def get(self, request, *args, **kwargs):
		user = None
        offset = kwargs.get("offset")
		content = {}
		try:
            content["data"] = load_reviews(user=user, offset=offset)
			return JsonResponse(content, status=200)
		except requests.exceptions.HTTPError as e:
            return JsonResponse({}, status=400)


class LoadMoreReviews(View):
	def get(self, request, *args, **kwargs):
		user = None
        offset = kwargs.get("offset")
		content = {}
        content["data"] = load_reviews(user=user, offset=offset)
        return render(request, "reviews/movie_list.html", content)


@login_required
def add_bookmark(request):
    mov, created = Movie.objects.get_or_create(
        display_title=request.POST.get("display_title"),
        url=request.POST.get("url"),
        img_src=request.POST.get("img_src"),
    )

    q = Bookmark.objects.filter(folder__user=request.user, movie=mov.id)
    if q.exists():
		# remove bookmark
        q.delete()
    return JsonResponse({}, status=200)
