import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser, User
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import AddToCollectionForm, CreateFolderForm
from .models import Bookmark, Collections, Movie

API_URL = "https://api.nytimes.com/svc/movies/v2/reviews/search.json"


class SignUpView(CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy("login")
	template_name = "registration/signup.html"


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
			# Add default values for image and link
			img_src = static("reviews/not-available.png")
			url = "#"
			if movie.get("multimedia"):
				img_src = movie.get("multimedia")["src"]
			if movie.get("link"):
				url = movie["link"]["url"]
			
			obj = {
				"url": url,
				"img_src": img_src,
				"display_title": movie["display_title"],
				"bookmarked": False,
			}

			# Show bookmarks if authenticated user has bookmarked movie
			if user.is_authenticated:
				mov = Movie.objects.filter(display_title=movie["display_title"])
				if mov.exists():
					if mov[0].check_bookmarked_by(user):
						obj["bookmarked"] = True
			
			data.append(obj)
		return data
class Reviews(View):
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
class LoadMoreReviews(View):
	def get(self, request, *args, **kwargs):
		user = request.user
		offset = kwargs.get("offset")
		content = {}
		content["data"] = load_reviews(user=user, offset=offset)
		return render(request, "reviews/movie_list.html", content)

class Bookmarks(ListView):
	def get(self, request, *args, **kwargs):
		folders = Collections.objects.filter(user=request.user).order_by(Lower("name"))
		content = []
		for fd in folders:
			folder = {}
			folder["name"] = fd.name
			folder["movies"] = []
			for bookmark in fd.bookmark_set.all():
				mov = bookmark.movie.__dict__
				mov["bookmarked"] = True
				folder["movies"].append(mov)
			content.append(folder)
		return render(request, "reviews/bookmarks.html", {"folders": content})

class FolderCreateView(LoginRequiredMixin, CreateView):
	model = Collections
	form_class = CreateFolderForm

	def post(self, request, pk, *args, **kwargs):
		if self.request.method == "POST":
			mov = get_object_or_404(Movie, pk=pk)
			form = self.form_class(self.request.POST, request=self.request)
			if form.is_valid():
				# Link created folder to movie by Bookmark
				obj = form.save(commit=False)
				obj.user = self.request.user
				obj.save()
				bk = Bookmark(movie=mov, folder=obj)
				bk.save()
				return JsonResponse({}, status=200)
			else:
				return JsonResponse({"error": form.errors}, status=400)
		return JsonResponse({"error": ""}, status=400)


class AddToFoldersView(UpdateView):
	form_class = AddToCollectionForm
	model = Movie

	def post(self, request, pk, *args, **kwargs):
		if self.request.method == "POST":
			mov = get_object_or_404(Movie, pk=pk)
			form = self.form_class(
				self.request.POST, request=self.request, instance=mov
			)
			form.fields["folders"]
			if form.is_valid():
				form.save()
				return JsonResponse({}, status=200)
			else:
				return JsonResponse({"error": form.errors}, status=400)
		return JsonResponse({"error": ""}, status=400)


@login_required
def add_bookmark(request):
	"""View to render bookmark forms (save to folder) if movie
	is not yet bookmarked by the user. If movie is already bookmarked,
	the bookmark is removed.
	"""
	mov, created = Movie.objects.get_or_create(
		display_title=request.POST.get("display_title"),
		url=request.POST.get("url"),
		img_src=request.POST.get("img_src"),
	)

	# Remove bookmark if present
	q = Bookmark.objects.filter(folder__user=request.user, movie=mov)
	if q.exists():
		q.delete()
		return JsonResponse({"deleted": True}, status=200)
	content = {}
	content["form1"] = AddToCollectionForm(request.POST, request=request, instance=mov)
	content["form2"] = CreateFolderForm(request.POST, request=request)
	content["movie"] = mov

	return render(request, "reviews/add_bookmark.html", content)
