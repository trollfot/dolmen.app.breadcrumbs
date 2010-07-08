======================
dolmen.app.breadcrumbs
======================

`dolmen.app.breadcrumbs` provides a breadcrumbs navigation for the
Dolmen applications. It registers a viewlet to render the links.

Getting started
===============

  >>> from grokcore.component import testing

To test the breadcrumbs' features, we need to create some content in
an hypothetical application::

  >>> from grokcore.content import Container
  >>> from zope.component.hooks import getSite

  >>> app = getSite()
  >>> app['cave'] = Container()
  >>> app['cave']['pot'] = Container()

To finish, we create a view. As we use a viewlet, we need a view to
display something::

  >>> import grokcore.view
  >>> from zope.interface import Interface

  >>> class simpleView(grokcore.view.View):
  ...   grokcore.view.context(Interface)
  ...   def render(self):
  ...     return u'For test purposes'

  >>> testing.grok_component('simpleview', simpleView)
  True


Adapting
========

The component that allows to build URLs and Breadcrumbs is a multi
adapter providing the IAbsoluteUrl interface. let's have a closer
look::

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> from zope.traversing.browser.interfaces import IAbsoluteURL

  >>> request = TestRequest()
  >>> url = getMultiAdapter((app['cave'], request), IAbsoluteURL)

  >>> url
  <dolmen.app.breadcrumbs.url.DescriptiveAbsoluteURL object at ...>

  >>> from zope.interface.verify import verifyObject
  >>> verifyObject(IAbsoluteURL, url)
  True

  >>> url()
  'http://127.0.0.1/cave'

  >>> url.breadcrumbs()
  ({'url': 'http://127.0.0.1', 'name': ''},
   {'url': 'http://127.0.0.1/cave', 'name': u'cave'})

The breadcrumbs uses the ``zope.dublincore`` interface,
`IDCDescriptiveProperties`, in order to get the renderable title::

  >>> from zope.dublincore.interfaces import IDCDescriptiveProperties
  >>> adapter = IDCDescriptiveProperties(app['cave'])
  >>> adapter.title
  u''


Rendering
========= 

Now, we have some contents in our application. We can call our view
and render the viewlet using its manager. 

  >>> from dolmen.app.layout import master
  >>> from dolmen.app.breadcrumbs import Breadcrumbs

  >>> view = getMultiAdapter((app['cave'], request), name="simpleview")
  >>> view
  <simpleView object at ...>


The Breadcrumbs viewlet is registered for the `dolmen.app.layout.Top`
manager::

  >>> manager = master.Top(app['cave'], request, view)
  >>> viewlet = Breadcrumbs(app['cave'], request, view, manager)
  >>> viewlet
  <dolmen.app.breadcrumbs.crumbs.Breadcrumbs object at ...>

Our contents have no title yet. If we render the viewlet, it uses the
location in the parent (`__name__`)::

  >>> viewlet.update()
  >>> print viewlet.render()
  <div id="breadcrumb">
    <span class="you-are-here">You are here :</span>
    <span class="crumb">
      <a href="http://127.0.0.1/cave">cave</a>
    </span>
  </div>

If we set a title, it uses the title::

  >>> adapter = IDCDescriptiveProperties(app['cave'])
  >>> adapter.title = u'My cave with a fireplace'

  >>> viewlet.update() 
  >>> print viewlet.render()
  <div id="breadcrumb">
    <span class="you-are-here">You are here :</span>
    <span class="crumb">
      <a href="http://127.0.0.1/cave">My cave with a fireplace</a>
    </span>
  </div>

It works with all kind of objects, even if their metadata title is not
set::

  >>> app['cave']['pot']['bone'] = object()
  >>> bone = app['cave']['pot']['bone']
  >>> viewlet = Breadcrumbs(bone, request, view, manager)

  >>> viewlet.update()
  >>> print viewlet.render()
  <div id="breadcrumb">
    <span class="you-are-here">You are here :</span>
    <span class="crumb">
      <a href="http://127.0.0.1/cave">My cave with a fireplace</a>
      <span class="breadcrumb-separator">&rarr;</span>
    </span>
    <span class="crumb">
      <a href="http://127.0.0.1/cave/pot">pot</a>
      <span class="breadcrumb-separator">&rarr;</span>
    </span>
    <span class="crumb">
      <a href="http://127.0.0.1/cave/pot/bone">bone</a>
    </span>
  </div>

If the object is not locatable, we raise a TypeError::

  >>> unlocatable = Container()
  >>> viewlet = Breadcrumbs(unlocatable, request, view, manager)
  >>> viewlet.update()
  Traceback (most recent call last):
  ...
  TypeError: There isn't enough context to get URL information. This is probably due to a bug in setting up location information.
