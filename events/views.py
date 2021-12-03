from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import regular_user, admin_user, EventsStory, User, Comment
from actions.models import Action
from django.http import JsonResponse


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
    events_stories = EventsStory.objects.all()
    for story in events_stories:
        if story.id == story_id:
            break
    return render(request,
                  "events/events_story/detail.html",
                  {"story": story}
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
    events_stories = EventsStory.objects.all()
    for story in events_stories:
        if story.id == story_id:
            break
    return render(request,
                  "events/events_story/edit.html",
                  {"story": story}
                  )


def event_changed(request):
    if request.method == 'POST':
        # process the form
        title = request.POST.get('edit-title')
        description = request.POST.get('edit-description')
        startdate = request.POST.get('edit-date')
        starttime = request.POST.get('edit-time')
        location = request.POST.get('edit-location')
        guests = request.POST.get('edit-guests')
        role = request.POST.get('edit-role')

        user = User.objects.get(username=request.session.get("username"))

        es = EventsStory.objects.all()[0]
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
        return redirect('events:story-detail', element.id)
    else:
        # show the template
        return render(request,
                      "events/events_story/edit.html",
                      )


def delete_event(request, story_id):
    instance = EventsStory.objects.get(id=story_id)
    instance.delete()

    user = User.objects.get(username=request.session.get("username"))
    # log the action
    action = Action(
        user=user,
        verb="deleted a story",
        target=instance
    )
    action.save()
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


def search_results(request):
    return render(request,
                  "events/events_story/list-search-main.html",
                  )


def view_comment(request, story_id):
    events_stories = EventsStory.objects.all()
    for story in events_stories:
        if story.id == story_id:
            break
    return render(request,
                  "events/events_story/comments.html",
                  {"story": story}
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
        element = cm
        return redirect('events:view_comment', element.id)
    # else:
    #     # show the template
    #     return render(request,
    #                   "events/events_story/comments.html",
    #                   )


def members(request):
    user = User.objects.all()
    return render(request,
                  "events/events_story/members.html",
                  {"users": user}
                  )

