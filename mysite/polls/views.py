from .forms import QuestionForm
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.db.models import Sum


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class QuestionDeleteView(generic.DeleteView):
    model = Question
    template_name = "polls/question_delete.html"

    def get_success_url(self):
        return reverse_lazy("polls:index")

    def get_context_data(self, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        num_votes = question.choice_set.aggregate(num_votes=Sum('votes'))
        context = super(QuestionDeleteView, self).get_context_data(**kwargs)
        context["num_votes"] = num_votes["num_votes"]
        return context


class QuestionCreateView(generic.CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "polls/create_question.html"

    def get_success_url(self):
        return reverse_lazy('polls:index')
