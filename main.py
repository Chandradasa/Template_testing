#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
import jinja2
import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

# current dir add templates files
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# jinja will load using temaplates located in current dir
jinja_env =jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir ), autoescape =True)

#form_html= """ testing jinja2"""
# autoescape escape html


# # below class testing datastore
# class Picture(ndb.Model):
#     link = ndb.StringProperty()
#     comment = ndb.StringProperty()
#     date = ndb.DateTimeProperty(auto_now_add=True)


# pic = Picture(comment= "this is my first data store")

# pic.put()



class Handler(webapp2.RequestHandler):
    # to be used by other functions  to output to web
    def write(self, *a,**kw):
        self.response.out.write(*a,**kw)
    # gets template into jinja  environment
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    # send out to web
    def render (self, template, **kw):
        self.write(self.render_str(template,**kw))


# class MainHandler(Handler):
#     def get (self):
#         items=self.request.get_all('food')
#         self.render ('shopping_list.html', items =items)

# class FizzBuzzHandler(Handler):
#       def get (self):
#          n =self.request.get('n',0)
#          n = n and  int(n)
#          self.render('fizzbuzz.html',n = n )

class CourseNotes(Handler):
      def get (self):
         concepts= [ "Lesson 1.1: The Basics of the Web and HTML",

         " Creating a Structured Document",
         "lesson 1.3:  adding CSS Style and HTML Structure","lesson 2.1  Introduction to serious programming",
         "lesson 2.2 variable and strings","lesson 2.3 input function output","lesson 2.4 Control flow: Loops if and while" 
         ,"lesson 2.5   Debugging","lesson 2.6  Structured Data: Lists and foor loops","lesson 2.7  How to solve Problems",
         "3.1-.2 introduction to abstraction  and Use functions"," lesson 3.3a,b,c, Classes","lesson 3.4a,b making Classes",
          
]
         notes = [["Lesson 1.1: The Basics of the Web and HTML","lesson_1.1"]]




         self.render('index.html',notes= notes )  
        
class Testing(Handler):
      def get (self):
         names=["dave", "john","tony"]
         some_dic={"son": "dave","age": 51}
         self.render('testing_forloops.html',names= names, **some_dic )  

    # def get(self):
     #   self.write(form_html)

class Comments(Handler):
      def get (self):
         
         self.render('comments.html')  


# We're going to use string substitution to render our HTML
# HTML_TEMPLATE = """<!DOCTYPE html>
# <head>
#   <meta charset="utf-8">
#   <title>Wall Book Example</title>
# </head>
# <body>
# <a href="/"> back to notes</a>
#   <form action="/sign?%s" method="post">
#     <div><textarea name="content" rows="3" cols="60"></textarea></div>
#     <div><input type="submit" value="Post Comment"></div>
#   </form>
#   <hr>
#   <form>Wall:
#     <input value="%s" name="wall_name">
#     <input type="submit" value="Switch">
#   </form>
#   <br>
#   Logged in as: <strong>%s</strong><br>
#   <a href="%s">%s</a>
#   <!-- user comments start here -->
#   %s
# </body>
# </html>
# """

DEFAULT_WALL = 'Public'

# We set a parent key on the 'Post' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def wall_key(wall_name=DEFAULT_WALL):
  """Constructs a Datastore key for a Wall entity.

  We use wall_name as the key.
  """
  return ndb.Key('Wall', wall_name)

# These are the objects that will represent our Author and our Post. We're using
# Object Oriented Programming to create objects in order to put them in Google's
# Database. These objects inherit Googles ndb.Model class.
class Author(ndb.Model):
  """Sub model for representing an author."""
  identity = ndb.StringProperty(indexed=True)
  name = ndb.StringProperty(indexed=False)
  email = ndb.StringProperty(indexed=False)

class Post(ndb.Model):
  """A main model for representing an individual post entry."""
  author = ndb.StructuredProperty(Author)
  content = ndb.StringProperty(indexed=False)
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
  def get(self):
    wall_name = self.request.get('wall_name',DEFAULT_WALL)
    if wall_name == DEFAULT_WALL.lower(): wall_name = DEFAULT_WALL

    # Ancestor Queries, as shown here, are strongly consistent
    # with the High Replication Datastore. Queries that span
    # entity groups are eventually consistent. If we omitted the
    # ancestor from this query there would be a slight chance that
    # Greeting that had just been written would not show up in a
    # query.

    # [START query]
    posts_query = Post.query(ancestor = wall_key(wall_name)).order(-Post.date)

    # The function fetch() returns all posts that satisfy our query. The function returns a list of
    # post objects
    posts =  posts_query.fetch()
    # [END query]

    # If a person is logged into Google's Services
    user = users.get_current_user()
    if user:
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        user_name = user.nickname()
    else:
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
        user_name = 'Anonymous Poster'

    # Create our posts html
    # posts_html = ''
    # for post in posts:

    #   # Check if the current signed in user matches with the author's identity from this particular
    #   # post. Newline character '\n' tells the computer to print a newline when the browser is
    #   # is rendering our HTML
    #   if user and user.user_id() == post.author.identity:
    #     posts_html += '<div><h3>(You) ' + post.author.name + '</h3>\n'
    #   else:
    #     posts_html += '<div><h3>' + post.author.name + '</h3>\n'

    #   posts_html += 'wrote: <blockquote>'+ cgi.escape(post.content) + '</blockquote>\n'
    #   posts_html += '</div>\n'

    error = self.request.get('error')
# cgi.escape(post.content)
    sign_query_params = urllib.urlencode({'wall_name': wall_name})

    # Render our page
   # rendered_HTML = HTML_TEMPLATE % (sign_query_params, cgi.escape(wall_name), user_name,
                     #             url, url_linktext, posts_html)
    posts_html=" " 
    rendered_HTML =  {"sign_query_params" : sign_query_params, "wall_name" : wall_name, "user_name" :user_name,
                                   "url":url, "url_linktext": url_linktext, "posts": posts,"error":error }


    # Write Out Page here
    #self.response.out.write(rendered_HTML)
    self.render("comments.html",**rendered_HTML)  
 

class PostWall(Handler):
  def post(self):
    # We set the same parent key on the 'Post' to ensure each

    # Post is in the same entity group. Queries across the
    # single entity group will be consistent. However, the write
    # rate to a single entity group should be limited to
    # ~1/second.
    wall_name = self.request.get('wall_name',DEFAULT_WALL)
    post = Post(parent=wall_key(wall_name))

    # When the person is making the post, check to see whether the person
    # is logged into Google
    if users.get_current_user():
      post.author = Author(
            identity=users.get_current_user().user_id(),
            name=users.get_current_user().nickname(),
            email=users.get_current_user().email())
    else:
      post.author = Author(
            name='anonymous@anonymous.com',
            email='anonymous@anonymous.com')


    # Get the content from our request parameters, in this case, the message
    # is in the parameter 'content'
    
  
    post.content = self.request.get('content')
    if post.content:

    # Write to the Google Database
        post.put()
        self.redirect('/MainPage')
    else:  
        self.redirect('/MainPage?error= Please add comments before submitting')

    # Do other things here such as a page redirect


app = webapp2.WSGIApplication([
('/',CourseNotes),('/comments.html',Comments),('/MainPage',MainPage),
('/sign', PostWall),('/testing_forloops',Testing)
 

], debug=True)
