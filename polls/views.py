from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from polls.models import Question, Choice, Message


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# Uncomment the line below to fix FLAW3
# @login_required(login_url='/polls/login')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            }
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


@csrf_exempt  # Delete this line
def guestbook_view(request):
    messages = Message.objects.all()
    return render(request, 'polls/guestbook.html', context={'messages': messages})


@csrf_exempt  # Delete this line
def guestbook_add(request):
    if request.method == "POST":
        Message.objects.create(name=request.POST.get('name'), message_text=request.POST.get('message'))
    return redirect('/polls/guestbook/')


@csrf_exempt  # Delete this line
def guestbook_filter(request):
    messages = []
    # sql = 'select name, message_text from polls_message where name = %s'
    # Replace the line below with the one above to fix FLAW1
    sql = f'select name, message_text from polls_message where name = \'{request.POST.get('name')}\''
    if request.method == "POST":
        with connection.cursor() as cursor:
            # cursor.execute(sql, (request.POST.get('name'),))
            # Replace the line below with the one above to fix FLAW1
            cursor.execute(sql)
            result = cursor.fetchall()

            messages = [{"name": r[0], "message_text": r[1]} for r in result]

    return render(request, 'polls/guestbook.html', context={'messages': messages})
