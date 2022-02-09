from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()  
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
    # @login_required(login_url='common:login') 로그인 없이 글 싸지르려고 하면 강제로 로그인 페이지로 이동시킨다

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author: #유저와 작성자가 다르면 수정 불가
        messages.error(request, '수정 권한이 없누')
        return redirect('pybo:detail', question_id = answer.question.id) #돌아가

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now() #수정일시 저장
            answer.save()
            return redirect('pybo:detail', question_id = answer.question.id)

    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form' : form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author: #유저와 작성자가 다르면 삭제 불가
        messages.error(request, '삭제 권한이 없누')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)