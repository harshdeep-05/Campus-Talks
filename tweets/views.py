from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Tweet
from .forms import TweetForm,TweetReplyForm
from accounts.models import UserProfile
import re

def get_trending_hasgtags():
	trends = {}
	tweets = Tweet.objects.all()
	for tweet_data in tweets:
		text = tweet_data.content
		pat = re.compile(r'[#](\w+)')
		hashtags = pat.finditer(text)
		for hasgtag in hashtags:
			try:
				trends[hasgtag.group().lower()]+=1
			except KeyError:
				trends[hasgtag.group().lower()] = 1
	trending = []
	for w in sorted(trends, key=trends.get, reverse=True):
  		trending.append(dict(hasgtag=w, tweet_count=trends[w]))
	return trending[:3]

@login_required(login_url = '/accounts/login')
def feed(request):
	who_to_follow = request.user.profile.get_who_to_follow()
	trends = get_trending_hasgtags()
	tweetss_data = Tweet.objects.all().filter(parent=None).order_by('-timestamp')
	tweets_data = [tweets_data for tweets_data in tweetss_data if request.user.profile.do_i_follow(tweets_data.user.profile)]
	user_tweets = Tweet.objects.filter(user=request.user).count()
	return render(request, 'tweets/feed.html', {'tweets_data':tweets_data, 'user_tweets':user_tweets, 'trends':trends, 'who_to_follow':who_to_follow})

@login_required(login_url = '/accounts/login')
@csrf_protect
def single_tweet(request, user_username, tweet_id):
	if request.method == 'POST':
		try:
			reply_tweet_obj = Tweet()
			reply_tweet_obj.content = request.POST.get('content')
			reply_tweet_obj.user = User.objects.get(id = int(request.POST.get('tweet_user')))
			parent_id = int(request.POST.get('parent'))
			if parent_id:
				parent_obj = Tweet.objects.filter(id=parent_id)
				if parent_obj is not None:
					reply_tweet_obj.parent = parent_obj.first()
				reply_tweet_obj.save()
		except:
			return HttpResponseRedirect("/%s/%s" % (user_username, tweet_id))
		return HttpResponseRedirect("/%s/%s" % (user_username, tweet_id))
	else:
		tweet_data = Tweet.objects.get(id = tweet_id)
		if tweet_data.is_parent is not True:
			tweet_data = tweet_data.parent
		return render(request, 'tweets/single_tweet.html', {'tweet_data':tweet_data})

@login_required(login_url = '/accounts/login')
@csrf_protect
def add_tweet(request):
	if request.method == 'POST':
		form = TweetForm(request.POST)
		if form.is_valid():
			tweet_form = form.save(commit = False)
			tweet_form.user = request.user
			tweet_form.save()
		return HttpResponseRedirect("/")
	else:
		args = {}
		args['form'] = TweetForm()
		return render(request, 'tweets/post_tweet.html', args)

@login_required(login_url = '/accounts/login')
@csrf_protect
def like(request):
	if request.method == 'POST':
		tweet_id = request.POST.get('like', False)
		if tweet_id:
			try:
				req_tweet = Tweet.objects.get(id = tweet_id)
				if req_tweet.like.filter(id = request.user.id).exists():
					req_tweet.like.remove(request.user)
				else:
					req_tweet.like.add(request.user)
			except ObjectDoesNotExist:
				return HttpResponseRedirect('/')

	return HttpResponseRedirect('/')

@login_required(login_url = '/accounts/login')
@csrf_protect
def retweet(request):
	if request.method == 'POST':
		tweet_id = request.POST.get('retweet', False)
		if tweet_id:
			try:
				req_tweet = Tweet.objects.get(id = tweet_id)
				new_tweet = Tweet()
				new_tweet = req_tweet
				new_tweet.pk = None
				new_tweet.retweet_status = True
				new_tweet.origin_tweet_user = req_tweet.user
				new_tweet.user = request.user
				new_tweet.save()
			except ObjectDoesNotExist:
				return HttpResponseRedirect('/')
	return HttpResponseRedirect('/')

@login_required(login_url = '/accounts/login')
def search(request):
	trends = get_trending_hasgtags()
	who_to_follow = request.user.profile.get_who_to_follow()
	query = request.GET.get('search')
	if str(query) == '':
		return HttpResponseRedirect('/')
	pat = re.compile(r'[@](\w+)')
	attags = pat.finditer(query)
	search_profile = None
	for attag in attags:
		try:
			search_profile = User.objects.get(username = attag.group()[1:])
			return HttpResponseRedirect('/accounts/profile/user/%s'%search_profile.username)
		except ObjectDoesNotExist:
			search_profile = None
		break
	search_data = Tweet.objects.filter(content__icontains=query).order_by('-timestamp')
	people = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
	return render(request, 'tweets/search_results.html', {'search_data':search_data, 'query':query, 'search_profile':search_profile, 'people':people, 'trends':trends, 'who_to_follow':who_to_follow})
	#We can differenitate here on the basis of the search query we have got like @ and # or any other textual query
