======================
dolmen.app.breadcrumbs
======================

`dolmen.app.breadcrumbs` provides a breadcrumbs navigation for the
Dolmen applications. It registers a viewlet to render the links.

Getting started
===============

To test the breadcrumbs' features, we need to create some content. We
used here `dolmen.content` contents, as our breadcrumbs' behavior works
only for IBaseContent objects::

  >>> import dolmen.content
  >>> from grokcore.component import testing

  >>> class Container(dolmen.content.Container):
  ...    dolmen.content.name('A dummy container')

  >>> testing.grok_component('container', Container)
  True

We now create our contents in an hypothetical application::

  >>> app = getRootFolder()
  >>> app['cave'] = Container()
  >>> app['cave']['pot'] = Container()

To finish, we create a view. As we use a viewlet, we need a view to
display something::

  >>> import grokcore.view

  >>> class simpleView(grokcore.view.View):
  ...   grokcore.view.context(dolmen.content.IBaseContent)
  ...   def render(self):
  ...     return u'For test purposes'

  >>> testing.grok_component('simpleview', simpleView)
  True


Rendering
========= 

Now, we have some contents in our application. We can call our view
and render the viewlet using its manager. 

  >>> from dolmen.app.breadcrumbs import Breadcrumbs
  >>> from dolmen.app.layout import master
  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest

  >>> request = TestRequest()
  >>> view = getMultiAdapter((app['cave'], request), name="simpleview")
  >>> view
  <dolmen.app.breadcrumbs.ftests.simpleView object at ...>


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
    <span class="you-are-here">You are here:</span>
    <span class="crumb">
      <a href="http://127.0.0.1/cave">cave</a>
    </span>
  </div>

If we set a title, it uses the title::

  >>> app['cave'].title = u"My cave with a fireplace"

  >>> viewlet.update() 
  >>> print viewlet.render()
  <div id="breadcrumb">
    <span class="you-are-here">You are here:</span>
    <span class="crumb">
      <a href="http://127.0.0.1/cave">My cave with a fireplace</a>
    </span>
  </div>

It works with all kind of objects although the title will only be used
for objects providing `dolmen.content.IBaseContent`::

  >>> app['cave']['pot']['bone'] = object()

  >>> viewlet = Breadcrumbs(
  ...    app['cave']['pot']['bone'], request, view, manager)
  >>> viewlet.update()
  >>> print viewlet.render()
  <div id="breadcrumb">
    <span class="you-are-here">You are here:</span>
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
