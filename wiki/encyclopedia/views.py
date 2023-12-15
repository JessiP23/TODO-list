from django.shortcuts import render
from markdown import Markdown
from django.urls import reverse
from . import util
import random  #this is for random choice


def index(request):
    return render(request, "encyclopedia/index.html", { #the following is a dictionary
        "entries": util.list_entries()   #name of variable:value of variable
    })    #entries is the list of the entries existing 
#first bullet
#the title includes the name of the entry
def entry(request, title): #the parameter is the title
    html_content = markdown_path(title)  #this function is important, all content is given in the md format so it is unreadable
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "false": "This requested page was not found"  #this is a variable called message than later on will be used in html between double curly brackets
        })   #in case doesnt exist the title then will render the error.html
    else:
        return render(request, "encyclopedia/entry.html",{  #render returns a piece of code and returns a response with the rendered text
            "title": title,
            "content": html_content,
        }) #it will display a page. this is like to show in case the title exists

#this includes the tab search
def search(request):  #this is the idea of showing the main page by requesting info from the use by using the post method
    if request.method == "POST": #in case data was sent
        tab = request.POST['q']      #variable is the data sent with parameter or value q in index.html
        show_content = markdown_path(tab)  
        if show_content is not None:
            return render(request, "encyclopedia/tab_search.html",{
                "title": tab,
                "content": show_content
            })
        else:
            letter = util.list_entries()    #this is when typing some letter and show similar entries with those letters
            guess = []  #empty list 
            for entry in letter: #this is a single entry in the list of entries
                if tab in entry: #if input submitted by user matches an entry
                    guess.append(entry)     #entries matched are added to the empty list
            return render(request, "encyclopedia/search.html", {
                "guess": guess
            })

def new_page(request): 
    #get info from the server
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']   #grab title from the html as well as content
        content = request.POST['content']
        error = util.get_entry(title)
        if error is not None:  #if title exists
            return render(request, "encyclopedia/error.html", {
                "false":"Entry Page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = markdown_path(title)  #md to html
            return render(request, "encyclopedia/entry.html",{ #this entry.html outputs the button in all searches I am making for existing entries
                "title": title,
                "content": html_content
            })

def edit_page(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == 'POST':
        #variables accepting the data enclosed and save title and content
        util.save_entry(request.POST['title'], request.POST['content'])
        title = request.POST['title']
        content_conversion = markdown_path(title)  #once getting the data will convert from md to html
        return render(request, "encyclopedia/save.html",{
            "title": title,  #define title
            "content": content_conversion
        })

def rand_choice(request): 
    #call all entries and randomly choice one
    entries = util.list_entries() 
    rando_choi = random.choice(entries) #random
    #IMPORTANT: never call a function the same as random or will display error
    conversion_html = markdown_path(rando_choi) #convert to html
    return render(request, "encyclopedia/entry.html",{ #request the entry.html with variables of title and content
        "title": rando_choi,
        "content": conversion_html
    })

def markdown_path(title):    #this is to use our markdown installation
    conversion = util.get_entry(title)
    markdowner = Markdown()
    if conversion == None:  #NOne is used because in case the content does not exist or in this case is not the same
        return None
    else:
        return markdowner.convert(conversion)    


'''
Importing Markdown to HTML

import markdown2
markdown2.markdown("*boo!*")  # or use `html = markdown_path(PATH)`
'<p><em>boo!</em></p>\n'

from markdown2 import Markdown
markdowner = Markdown()
markdowner.convert("*boo!*")
'<p><em>boo!</em></p>\n'
 markdowner.convert("**boom!**")
'<p><strong>boom!</strong></p>\n'
'''