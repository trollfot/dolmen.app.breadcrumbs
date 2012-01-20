# -*- coding: utf-8 -*-

from os import path
from dolmen.template import TALTemplate
from cromlech.browser import IRenderer
from zope.interface import implements
from dolmen.app.breadcrumbs import breadcrumbs


TEMPLATES_DIR = path.join(path.dirname(__file__), 'templates')
template = TALTemplate(path.join(TEMPLATES_DIR, 'breadcrumbs.pt'))


def render_breadcrumbs(renderer, crumbs, separator="&rarr;"):
    return template.render(renderer, breadcrumbs=crumbs, separator=separator)


class BreadcrumbsRenderer(object):
    implements(IRenderer)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def namespace(self):
        return {}

    def update(self):
        self.breadcrumbs = list(breadcrumbs(self.context, self.request))
    
    def render(self):
        return render_breadcrumbs(self, self.breadcrumbs)
