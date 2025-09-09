from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Blog, Quiz, QuizSubmission
from .forms import QuizForm

def index(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-published_date')[:3]
    quizzes = Quiz.objects.filter(is_active=True)[:3]
    return render(request, 'index.html', {'blogs': blogs, 'quizzes': quizzes})

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    return render(request, 'blog_detail.html', {'blog': blog})

def quiz_list(request):
    quizzes = Quiz.objects.filter(is_active=True)
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, questions=quiz.questions.all())
        if form.is_valid():
            score = 0
            total_questions = quiz.questions.count()
            
            for question in quiz.questions.all():
                field_name = f'question_{question.id}'
                if field_name in form.cleaned_data:
                    user_answers = form.cleaned_data[field_name]
                    if not isinstance(user_answers, list):
                        user_answers = [user_answers]
                    
                    # Convertir les réponses en entiers pour la comparaison
                    user_answers = [int(ans) for ans in user_answers if ans.isdigit()]
                    
                    # Obtenir les IDs des options correctes
                    correct_answers = list(question.options.filter(is_correct=True).values_list('id', flat=True))
                    
                    # Vérifier si les réponses sont correctes
                    if set(user_answers) == set(correct_answers):
                        score += 1
            
            # Enregistrer le score
            submission = QuizSubmission(
                quiz=quiz,
                user=request.user if request.user.is_authenticated else None,
                score=score
            )
            submission.save()
            
            return render(request, 'quiz_result.html', {
                'quiz': quiz,
                'score': score,
                'total_questions': total_questions,
                'submission': submission
            })
    else:
        form = QuizForm(questions=quiz.questions.all())
    
    return render(request, 'quiz_detail.html', {'quiz': quiz, 'form': form})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Statistiques pour le tableau de bord admin
    blog_count = Blog.objects.count()
    quiz_count = Quiz.objects.count()
    submission_count = QuizSubmission.objects.count()
    
    return render(request, 'admin_dashboard.html', {
        'blog_count': blog_count,
        'quiz_count': quiz_count,
        'submission_count': submission_count
    })