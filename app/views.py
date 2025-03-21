from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from .models import Note
from .tasks import task_do_something


class NoteListView(ListView):
    model = Note
    template_name = "index.html"
    context_object_name = "notes"


class NoteDetailView(DetailView):
    model = Note
    template_name = "preview.html"
    context_object_name = "note"


class NoteCreateView(View):
    def get(self, request):
        return render(request, "form.html")

    def post(self, request):
        title = request.POST.get("title")
        content = request.POST.get("content")

        task_do_something() ##background --> insert to queue

        Note.objects.create(title=title, content=content, user=request.user)
        return redirect("index")
