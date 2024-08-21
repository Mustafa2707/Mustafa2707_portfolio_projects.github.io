from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms
from . import util
from random import choice

class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search",required= False,widget= forms.TextInput (attrs={'placeholder':'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title",required = True,
    widget= forms.TextInput
    (attrs={'placeholder':'Enter Title'}))

    body = forms.CharField(label="Markdown content",required= False, 
    widget= forms.Textarea
    (attrs={'placeholder':'Enter markdown content','class':'col-sm-11','style':'top:.5rem'}))

class NewEditForm(forms.Form):
    pagename = forms.CharField(label="Title",required = False,
    widget= forms.HiddenInput
    (attrs={'class':'col-sm-12','style':'bottom:1rem'}))
   
    body = forms.CharField(label="Markdown content",
    widget= forms.Textarea
    (attrs={"rows":20, "cols":80,'class':'col-sm-11','style':'top:.5rem'}))


form = NewSearchForm()
page = NewPageForm()
ePage = NewEditForm()

def convert_md_to_HTML(title):
    markdowner = Markdown()
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":form
    })

def entry(request,title):
    html_content = convert_md_to_HTML(title)
    if html_content == None:
        message = f"{title} entry not found"
        return render(request,"encyclopedia/error.html", {
            "error_message": message,
            "form":form
        })
    else:
        return render(request,"encyclopedia/entry.html", {
            "title": title,
            "content" : html_content,
            "form":form
        })
    
def search(request):
    if request.method == 'GET':
        form = NewSearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data["search"].lower()
            entries = util.list_entries()   

            pages = [pagename for pagename in entries if query in pagename.lower()]

            if len(pages) == 0:
                return render(request,"encyclopedia/search.html", {
                    "error": "No results found!",
                    "form":form
                })
            elif len(pages) == 1 and pages[0].lower() == query:
                title = pages[0]
                return entry(request,title)
            else:
                title = [pagename for pagename in pages if query == pagename.lower()]
                if len(title)>0:
                    return entry(request,title[0])
                else:
                    return render(request, "encyclopedia/search.html", {
                        "results": pages,
                        "form":form
                    })
        else:
            return index(request)
    
    return index(request)

def new_entry(request):
        if request.method == 'GET':
            page = NewPageForm(request.GET)
            return render(request, 'encyclopedia/new_entry.html',{
                "NewPage":page,
                "form":form,
                "error_message":""
            })
        else:
            page = NewPageForm(request.POST)

            if page.is_valid():
                title = page.cleaned_data["title"]
                content = page.cleaned_data["body"]

                entries = util.list_entries()

                for file in entries:
                    if file.lower() == title.lower():
                        error_message = "Entry already exits"
                        page = NewPageForm()
                        return  render(request,"encyclopedia/new_entry.html",{
                            "error_message":error_message,
                            "form":form,
                            "MewPage":page 
                        })
                    
                util.save_entry(title,content)
                return entry(request,title)
            else:
                return render(request,"encyclopedia/new_entry.html",{
                    "NewPage":page,
                    "form":form
                })

def Edit_Page_choice(request):
    return render(request,"encyclopedia/edit_choice.html",{
        "form":form,
        "entries":util.list_entries()
    })

def edit_page(request,title):
    content = util.get_entry(title)
    ePage = NewEditForm(initial={'pagename': title, 'body':content})          
    if ePage.is_valid():
        return render(request,"encyclopedia/edit_page.html",{
            "title":title,
            "form":form,
            "ePage":ePage
        })
    else:
        return render (request, "encyclopedia/edit_page.html",{
                "title": title,
                "form":form,
                "ePage":ePage      

        })

def save_edited_page(request):
    ePage = NewEditForm(request.POST)
    if ePage.is_valid():
        title = ePage.cleaned_data["pagename"]
        content = ePage.cleaned_data["body"]

        val = util.save_entry(title,content)

        return entry(request,title)
    else:
        return render (request, "encyclopedia/edit_page.html",{
                "form":form,
                "ePage":ePage
            
        })
    
def random_page(request):
    return entry(request,choice(util.list_entries()))