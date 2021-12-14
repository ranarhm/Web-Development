from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import regular_user, admin_user, EventsStory, User, Comment
from actions.models import Action
from django.http import JsonResponse
import requests
import boto3
from django.template.loader import render_to_string
from django.contrib.auth import authenticate


# Create your views here.
def events_story_list(request):
    events_stories = EventsStory.objects.all()
    sort = request.POST.get('sort-by-register')
    if sort == 'Registered':
        events_stories = EventsStory.objects.order_by('-registered')
    sort1 = request.POST.get('sort-by-date')
    if sort1 == 'Recently updated':
        events_stories = EventsStory.objects.order_by('-date_posted')
    return render(request,
                  "events/events_story/list.html",
                  {"stories": events_stories}
                  )


def events_story_detail(request, story_id):
    story = EventsStory.objects.get(pk=story_id)

    endpoint = "https://en.wikipedia.org/w/api.php"
    parameters = {
        "action": "query",
        "list": "search",
        "srsearch": story.title,
        "format": "json",
    }

    try:
        response = requests.get(endpoint, params=parameters)
        wikidata = response.json()
        top_wiki_title = wikidata["query"]["search"][0]["title"]
    except IndexError:
        top_wiki_title = None

    return render(request,
                  "events/events_story/detail.html",
                  {"story": story,
                   "top_wiki_title": top_wiki_title}
                  )


def home(request):
    if request.session.get("username", False):
        actions = Action.objects.all().order_by('-created')

        return render(request,
                      "events/events_story/dashboard.html",
                      {"actions": actions}
                      )

    else:
        return render(request,
                      "events/home.html",
                      )


def create_event(request):
    return render(request,
                  "events/events_story/add.html",
                  )


def event_added(request):
    if request.method == 'POST':
        # process the form
        title = request.POST.get('add-title')
        description = request.POST.get('add-description')
        startdate = request.POST.get('add-start date')
        starttime = request.POST.get('add-start time')
        location = request.POST.get('add-location')
        guests = request.POST.get('add-guests')
        role = request.POST.get('add-role')

        # content moderation
        endpoint = "https://isvttextmod.cognitiveservices.azure.com/contentmoderator/moderate/v1.0/ProcessText/Screen"
        parameters = {
            'classify': True,
        }
        headers = {
            'Content-Type': 'text/plain',
            'Ocp-Apim-Subscription-Key': '5d85180a097b4949ba5bc2b583c6569f',
        }
        data = description
        response = requests.post(endpoint, params=parameters, headers=headers, data=data)
        response_json = response.json()
        review_recommended = response_json["Classification"]["ReviewRecommended"]
        if review_recommended:
            messages.add_message(request, messages.ERROR,
                                 "Your description contains inappropriate contents. Please change it.")
            return redirect('events:create-event')

        user = User.objects.get(username=request.session.get("username"))

        es = EventsStory(
            title=title,
            description=description,
            date_weekday=startdate,
            date_month=startdate,
            # date_day=startdate,
            time=starttime,
            location=location,
            performers=guests,
            author=request.session.get('username'),
            user=user,
            role=role,
        )
        es.save()

        # begin mturk
        mturk_sandbox = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
        mturk = boto3.client('mturk',
                             aws_access_key_id="AKIA2H4GXO6OS6WFJL4Z",
                             aws_secret_access_key="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",
                             region_name='us-east-1',
                             endpoint_url=mturk_sandbox
                             )
        print("I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my Sandbox account")

        # question = open(name='questions.xml', mode='r').read()
        question = render_to_string('events/events_story/questions.xml', {'story_id': es.id, 'domain': request.META['HTTP_HOST']})
        new_hit = mturk.create_hit(
            Title='Find the Facebook Home Page link for a Given Guest',
            Description='Use Google, social media platforms, or any other resources to find the Facebook home page link for a given guest.',
            Keywords='headline, event, facebook, cs5774f21',
            Reward='0.15',
            MaxAssignments=10,
            LifetimeInSeconds=600,
            AssignmentDurationInSeconds=600,
            AutoApprovalDelayInSeconds=600,
            Question=question,
        )
        print("A new HIT has been created. You can preview it here:")
        print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
        print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")

        # end mturk

        # log the action
        action = Action(
            user=user,
            verb="created the new story",
            target=es
        )
        action.save()
        messages.add_message(request, messages.SUCCESS, "You successfully submitted a new event story: %s" % es.title)
        element = es
        return redirect('events:story-detail', element.id)
    else:
        # show the template
        return render(request,
                      "events/events_story/add.html",
                      )


def edit_event(request, story_id):
    story = EventsStory.objects.get(pk=story_id)
    return render(request,
                  "events/events_story/edit.html",
                  {"story": story}
                  )


def event_changed(request, story_id):

    es = EventsStory.objects.get(pk=story_id)

    mturk = request.GET.get('mturk', False)
    if mturk == 'yes':
        user = authenticate(username='mturk', password='mturk')
        request.session['username'] = user.username
        request.session['role'] = user.details.role
    else:
        user = User.objects.get(username=request.session.get("username"))

    if user.id == es.user.id or request.session['role'] == 'admin' or user.username == 'mturk':
        if request.method == 'POST':
            # process the form
            title = request.POST.get('edit-title')
            description = request.POST.get('edit-description')
            print(description)
            startdate = request.POST.get('edit-date')
            starttime = request.POST.get('edit-time')
            location = request.POST.get('edit-location')
            guests = request.POST.get('edit-guests')
            print(guests)
            role = request.POST.get('edit-role')
            print(role)

            if title:
                es.title = title
            if description:
                es.description = description
            if startdate:
                es.startdate = startdate
            if starttime:
                es.starttime = starttime
            if location:
                es.location = location
            if guests:
                es.guests = guests
            if role:
                es.role = role
            es.save()

            # log the action
            action = Action(
                user=user,
                verb="edited a story",
                target=es
            )
            action.save()

            messages.add_message(request, messages.SUCCESS, "You successfully edited an event story: %s" % es.title)
            element = es
            return redirect('events:story-detail', story_id=story_id)
        else:
            # show the template
            return render(request,
                          "events/events_story/edit.html",
                          )


def delete_event(request, story_id):
    instance = EventsStory.objects.get(id=story_id)
    instance.delete()

    messages.add_message(request, messages.WARNING, "The following event story was deleted: %s" % instance.title)

    return redirect('events:story-list')


def events_story_registered(request):
    # redirect if not logged in
    if not request.session.get("username", False):
        return redirect('events:story-list')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        story_id = request.POST.get('story_id')
        try:
            story = EventsStory.objects.get(pk=story_id)
            story.registered = story.registered + 1
            story.save()
            return JsonResponse({'success': 'success', 'registered': story.registered}, status=200)

        except EventsStory.DoesNotExist:
            return JsonResponse({'error': 'No story found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


def events_story_like(request):
    # redirect if not logged in
    if not request.session.get("username", False):
        return redirect('events:story-list')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        story_id = request.POST.get('story_id')
        try:
            story = EventsStory.objects.get(pk=story_id)
            story.score = story.score + 1
            story.save()
            return JsonResponse({'success': 'success', 'score': story.score}, status=200)

        except EventsStory.DoesNotExist:
            return JsonResponse({'error': 'No story found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


def events_story_dislike(request):
    # redirect if not logged in
    if not request.session.get("username", False):
        return redirect('events:story-list')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        story_id = request.POST.get('story_id')
        try:
            story = EventsStory.objects.get(pk=story_id)
            story.score = story.score - 1
            story.save()
            return JsonResponse({'success': 'success', 'score': story.score}, status=200)

        except EventsStory.DoesNotExist:
            return JsonResponse({'error': 'No story found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


def events_story_description(request):
    # redirect if not logged in
    if not request.session.get("username", False):
        return redirect('events:home')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "GET":
        # story_id = request.POST.get('story_id')
        try:
            story = EventsStory.objects.all()
            story.info = story.info
            story.save()
            return JsonResponse({'success': 'success', 'info': story.info}, status=200)

        except EventsStory.DoesNotExist:
            return JsonResponse({'error': 'No data found with that ID.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


def search_results(request):
    events_stories = EventsStory.objects.filter(title__contains="Party")
    return render(request,
                  "events/events_story/list-search-main.html",
                  {"stories": events_stories}
                  )


def search_results_none(request):
    return render(request,
                  "events/events_story/list-search-main.html",
                  )


def view_comments(request):
    events_stories = Comment.objects.all()
    return render(request,
                  "events/events_story/comments.html",
                  {"comments": events_stories}
                  )


def add_comment(request):
    if request.method == 'POST':
        # process the form
        title = request.POST.get('add-title')
        comment = request.POST.get('add-comment')

        user = User.objects.get(username=request.session.get("username"))

        cm = Comment(
            title=title,
            comment=comment,
            author=request.session.get('username'),
            user=user,
        )
        cm.save()
        # log the action
        action = Action(
            user=user,
            verb="posted a new comment",
            target=cm
        )
        action.save()
        messages.add_message(request, messages.SUCCESS, "You successfully posted a new comment")
        return redirect('events:view_comments')
    else:
        # show the template
        return render(request,
                      "events/events_story/comments.html",
                      )


def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    return render(request,
                  "events/events_story/edit-comment.html",
                  {"comment": comment}
                  )


def delete_comment(request, comment_id):
    cm = Comment.objects.get(pk=comment_id)
    user = User.objects.get(username=request.session.get("username"))
    if user.id == cm.user.id or request.session['role'] == 'admin':
        cm = Comment.objects.get(id=comment_id)
        cm.delete()

        return redirect('events:view_comments')


def comment_changed(request, comment_id):

    cm = Comment.objects.get(pk=comment_id)

    user = User.objects.get(username=request.session.get("username"))

    if user.id == cm.user.id or request.session['role'] == 'admin':
        if request.method == 'POST':
            # process the form
            title = request.POST.get('edit-title')
            comment = request.POST.get('edit-comment')

            if title:
                cm.title = title
            if comment:
                cm.comment = comment

            cm.save()

            # log the action
            action = Action(
                user=user,
                verb="edited a comment",
                target=cm
            )
            action.save()

            return redirect('events:view_comments')
        else:
            # show the template
            return render(request,
                          "events/events_story/edit-comment.html",
                          )


def members(request):
    user = User.objects.all()
    return render(request,
                  "events/events_story/members.html",
                  {"users": user}
                  )


def performer_facebook(request, story_id):
    story = EventsStory.objects.get(pk=story_id)
    return render(request,
                  "events/events_story/performer-facebook.html",
                  {"story": story}
                  )


def performer_facebook_added(request, story_id):

    es = EventsStory.objects.get(pk=story_id)
    if request.method == 'POST':
        # process the form
        url = request.POST.get('add-url')

        if url:
            es.url = url
        es.save()

        return redirect('events:story-detail', story_id=story_id)
    else:
        # show the template
        return render(request,
                      "events/events_story/performer-facebook.html",
                      )


def contact(request):
    return render(request,
                  "events/events_story/contact.html",
                  )


def media(request):
    return render(request,
                  "events/events_story/media.html",
                  )


def about(request):
    return render(request,
                  "events/events_story/isvt-about.html",
                  )


def directory(request):
    return render(request,
                  "events/events_story/isvt-executive.html",
                  )


def join(request):
    return render(request,
                  "events/events_story/isvt-join.html",
                  )
