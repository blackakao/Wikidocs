from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Question, Answer, Comment
from .forms import QuestionForm, AnswerForm, CommentForm

# Create your views here.

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page','1') #페이지

    #조회
    question_list = Question.objects.order_by('-create_date')

    #페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

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
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()  
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
    # @login_required(login_url='common:login') 로그인 없이 글 싸지르려고 하면 강제로 로그인 페이지로 이동시킨다

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: #유저와 작성자가 다르면 수정 불가
        messages.error(request, '수정 권한이 없누')
        return redirect('pybo:detail', question_id = question.id) #돌아가

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now() #수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id = question.id)

    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: #유저와 작성자가 다르면 삭제 불가
        messages.error(request, '삭제 권한이 없누')
        return redirect('pybo:detail', question_id = question.id) #돌아가
    question.delete()
    return redirect('pybo:index')

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

@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    pybo 질문댓글 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author: #유저와 작성자가 다르면 수정 불가
        messages.error(request, '댓글 수정 권한이 없누')
        return redirect('pybo:detail', comment_id = comment.question.id) #돌아가

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now() #수정일시 저장
            comment.save()
            return redirect('pybo:detail', question_id = comment.question.id)

    else:
        form = CommentForm(instance=comment)
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    pybo 질문댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author: #유저와 작성자가 다르면 삭제 불가
        messages.error(request, '댓글삭제 권한이 없누')
        return redirect('pybo:detail', question_id = comment.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id = comment.question.id)


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    pybo 답글댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id = comment.answer.question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    pybo 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author: #유저와 작성자가 다르면 수정 불가
        messages.error(request, '댓글 수정 권한이 없누')
        return redirect('pybo:detail', question_id = comment.answer.question.id) #돌아가

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now() #수정일시 저장
            comment.save()
            return redirect('pybo:detail', question_id = comment.answer.question.id)

    else:
        form = CommentForm(instance=comment)
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    pybo 답글댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author: #유저와 작성자가 다르면 삭제 불가
        messages.error(request, '댓글삭제 권한이 없누')
        return redirect('pybo:detail', question_id = comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id = comment.answer.question.id)