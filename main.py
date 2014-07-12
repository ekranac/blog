import webapp2
import os
import jinja2
import time
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Base(webapp2.RequestHandler):


    def render_template(self, view_filename, params=None):
		if not params:
			params = {}
		template = jinja_env.get_template(view_filename)
		self.response.out.write(template.render(params))

    #def render_index(self, page_title):
    #    self.render("index.html", page_title=page_title)

    #def render_writepost(self, page_title, title, content):
    #    self.render("write.html", page_title=page_title, title=title, content=content)

class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.StringProperty(required = True)
    created  = db.DateTimeProperty(auto_now_add = True)

class MainPage(Base):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc")
        args = {"page_title":"My Blog", "posts":posts}
        self.render_template("index.html", args)

class WritePage(Base):
    def get(self):
        args = {"page_title":"New post"}
        self.render_template("write.html", args)

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        if title and content:
            p = Post(title = title, content = content)
            p.put()

            time.sleep(1)

            self.redirect("/post/%s" %p.key().id())
        else:
            args = {"page_title":"New post", "title":title, "content":content}
            self.render_template("write.html", args)


class PostPage(Base):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        args = {"post":post}

        self.render_template("post.html", args)



app = webapp2.WSGIApplication([
                                  webapp2.Route('/', MainPage),
                                  webapp2.Route("/writepost", WritePage),
                                  webapp2.Route("/post/<post_id:\d+>", PostPage)
], debug=True)