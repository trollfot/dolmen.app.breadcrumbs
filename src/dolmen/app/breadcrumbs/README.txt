======================
dolmen.app.breadcrumbs
======================

  >>> import grokcore.view
  >>> import dolmen.content
  >>> import dolmen.app.breadcrumbs 

  >>> from dolmen.app.layout import master
  >>> from grokcore.component import testing

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest

  >>> class Container(dolmen.content.Container):
  ...    dolmen.content.name('A dummy container')

  >>> testing.grok_component('container', Container)
  True

  >>> class simpleView(grokcore.view.View):
  ...   grokcore.view.context(dolmen.content.IBaseContent)
  ...   def render(self):
  ...     return u'For test purposes'

  >>> testing.grok_component('simpleview', simpleView)
  True

  >>> request = TestRequest()

  >>> root = getRootFolder()
  >>> root['cave'] = Container()
  >>> root['cave']['pot'] = Container()

  >>> view = getMultiAdapter((root['cave'], request), name="simpleview")
  >>> view
  <dolmen.app.breadcrumbs.ftests.simpleView object at ...>

  >>> manager = master.Top(root['cave'], request, view)
  >>> viewlet = dolmen.app.breadcrumbs.Breadcrumbs(
  ...    root['cave'], request, view, manager)
  >>> viewlet
  <dolmen.app.breadcrumbs.crumbs.Breadcrumbs object at ...>

  >>> viewlet.update()
  >>> print viewlet.render()
  <div id="breadcrumb">
    <span class="you-are-here">You are here:</span>
    <span class="crumb">
      <a href="http://127.0.0.1/cave">cave</a>
    </span>
  </div>

  >>> root['cave'].title = u"My cave with a fireplace"

  >>> viewlet.update() 
  >>> print viewlet.render()
  <div id="breadcrumb">
    <span class="you-are-here">You are here:</span>
    <span class="crumb">
      <a href="http://127.0.0.1/cave">My cave with a fireplace</a>
    </span>
  </div>

  >>> root['cave']['pot']['bone'] = object()

  >>> viewlet = dolmen.app.breadcrumbs.Breadcrumbs(
  ...    root['cave']['pot']['bone'], request, view, manager)
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

  >>> viewlet = dolmen.app.breadcrumbs.Breadcrumbs(
  ...    Container(), request, view, manager)
  >>> viewlet.update()
  Traceback (most recent call last):
  ...
  TypeError: There isn't enough context to get URL information. This is probably due to a bug in setting up location information.
