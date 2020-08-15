from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from django import forms
import random

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class':'form-control'}))
    entry_content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class':'form-control'}))

def index(request):
    form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": form,
        "result": False
    })

def view_entry(request, title):
    form = SearchForm()
    print("title : " ,title)
    entry = util.get_entry(title)
    if not entry:
        return render(request, "error/404.html")
    return render(request, "encyclopedia/page.html", {
        "entry" : markdown2.markdown(entry),
        "title" : title,
        "form" : form
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
            if query in util.list_entries():
                return HttpResponseRedirect(reverse("view_entry", kwargs={
                    "title":query
                }))
            else:
                result = []
                for entry in util.list_entries():
                    if query.lower() in entry.lower():
                        result.append(entry)
                return render(request, "encyclopedia/index.html", {
                    "entries": result,
                    "form": form,
                    "result": True
                })
    return HttpResponseRedirect(reverse("index"))

def createNewEntry(request):
    entryForm = NewEntryForm()
    form = SearchForm()
    if request.method == "POST":
        entryForm = NewEntryForm(request.POST)
        if entryForm.is_valid():
            title = entryForm.cleaned_data["entry_title"]
            if title in util.list_entries():
                return render(request, "error/already_exist.html", {
                    "form": form,
                })
            content = entryForm.cleaned_data["entry_content"]
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('index'))
    return render(request, "encyclopedia/new_entry.html", {
        "form": form,
        "entryForm": entryForm,
        "route": "new_entry"
    })

def randomPage(request):
    form = SearchForm()
    pages = util.list_entries()
    title = pages[random.randrange(len(pages))]
    return HttpResponseRedirect(reverse('view_entry', kwargs={
        "title": title
    }))

def editEntry(request, title):
    entryForm = NewEntryForm(initial={"entry_title": title, "entry_content": util.get_entry(title)})
    form = SearchForm()
    if request.method == 'POST':
        entryForm = NewEntryForm(request.POST)
        if entryForm.is_valid():
            util.save_entry(entryForm.cleaned_data["entry_title"], entryForm.cleaned_data["entry_content"])
            return HttpResponseRedirect(reverse('view_entry', kwargs={"title": title}))
    return render(request, "encyclopedia/new_entry.html", {
        "form": form,
        "entryForm": entryForm,
        "route": "edit_entry",
        "title": title
    })
