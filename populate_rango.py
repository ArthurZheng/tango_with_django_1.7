import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
	python_cat = add_cat('Python', 128, 10)
	django_cat = add_cat('Django', 64, 20)
	others = add_cat('Other Frameworks', 32, 30)

	add_page(cat=python_cat, title='Official Python Tutorial', url='http://docs.python.org', views='88')
	add_page(cat=python_cat, title='Think Like a Computer Scientist', url='http://www.yahoo.com', views='65')
	add_page(cat=python_cat, title='Learn Python in 10 Minutes', url='http://www.163.com', views='54')
	add_page(cat=django_cat, title='Django documentation', url='http://docs.djangoproject.com', views='92')
	add_page(cat=django_cat, title='Django Rocks', url='http://www.tangowithdjango.com', views='78')
	add_page(cat=others, title='Ruby on Rails', url='http://www.ruby.com', views='76')

	for c in Category.objects.all():
		for p in Page.objects.filter(category = c):
			print "-{0} - {1}".format(str(c), str(p))

			
def add_cat(name, views=0, likes=0):
	c = Category.objects.get_or_create(name=name)[0]
	c.views = views
	c.likes = likes
	c.save()

	return c


def add_page(cat, title, url, views=0):
	p = Page.objects.get_or_create(category = cat, title=title)[0]
	p.url = url
	p.views = views
	p.save()

	return p


if __name__ == '__main__':
	print "Starting Rango population script ..."
	populate()
