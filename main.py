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

import webapp2, cgi, jinja2, os, re
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


class Handler(webapp2.RequestHandler):
    
    def write(self, *a, **kw):
    	self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
    	t=jinja_env.get_template(template)
    	return t.render(params)

    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw))

#creating an entity called post for the database
class Post(db.Model):
	subject=db.StringProperty(required = True)
	post=db.TextProperty(required = True)
	created=db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):

	def render_front(self):
		posts=db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
		self.render("front.html", posts=posts)

	def get(self):
		self.render_front()

	


class NewPostHandler(Handler):

	def render_newpost(self, subject="", post="", error=""):
		self.render("newpost.html", subject=subject, post=post, error=error)

	def get(self):
		self.render_newpost()

	def post(self):
		# to get the subject and post from the request, to validate
		subject=self.request.get("subject")
		post=self.request.get("post")

		#checking if one of the fields was left empty, to 
		#render the form again
		if subject and post:
			#creating a new post instance with the user input 
			# and saving it to the data base 
			a= Post(subject= subject, post= post)
			a.put()
			
			#redirect to the frontpage to avoid reload message
			self.redirect("/blog")
		else:
			error="we need both a subject and some postwork!"
			self.render_newpost(subject, post, error)


app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/blog/newpost', NewPostHandler)
], debug=True)
