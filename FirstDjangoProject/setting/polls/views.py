

from asyncio import QueueEmpty
from re import template
from select import select

# Create your views here.
# 뷰를 호출할 url httpresponse 쪽에 url을 넣어주던지 글씨를 삽입하던지 하는 방향으로 진행되는 모양
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, response
from django.http import Http404
from django.template import context, loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# 개객끼가... 첨부터 다시하라고..
from django.views import generic

from .models import Question, Choice
from django.utils import timezone

# def index(request):
#     # return HttpResponse("Hello, world. You're at the polls index.")
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list':latest_question_list}
#     return render(request, 'polls/index.html',context)

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s" %question_id)

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# def results(request, question_id):
#     response = "You're looking at the results of question %s"
#     return HttpResponse(response %question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s" %question_id)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question':question,
            'error_message': "선택한 것이 없다.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        
        
# return render(request, 'polls/detail.html',{'question':question})
    
# def vote (request, question_id):
#     question = get_object_or_404(Question, pk=question_id)