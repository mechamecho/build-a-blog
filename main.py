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

#creating an entity called art for the database
class Art(db.Model):
	title=db.StringProperty(required = True)
	art=db.TextProperty(required = True)
	created=db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):

	def render_font(self, title="", art="", error=""):
		arts=db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
		self.render("font.html", title=title, art=art, error=error, arts=arts)

	def get(self):
		self.render_font()

	def post(self):
		# to get the title and art from the request, to validate
		title=self.request.get("title")
		art=self.request.get("art")

		#checking if one of the fields was left empty, to 
		#render the form again
		if title and art:
			#creating a new Art instance with the user input 
			# and saving it to the data base 
			a= Art(title= title, art= art)
			a.put()
			
			#redirect to the frontpage to avoid reload message
			self.redirect("/")
		else:
			error="we need both a title and some artwork!"
			self.render_font(title, art, error)

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
