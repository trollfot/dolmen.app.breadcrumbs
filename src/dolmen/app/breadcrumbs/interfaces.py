# -*- coding: utf-8 -*-

from zope.interface import Interface


class IBreadcrumbs(Interface):

    def __call__(object, request):
        """returns an iterable of dict, containing base crumb info.
        Required keys are : `url` and `name`.
        """
