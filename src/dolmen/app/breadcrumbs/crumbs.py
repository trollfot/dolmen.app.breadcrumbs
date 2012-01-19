# -*- coding: utf-8 -*-

import urllib
from cromlech.io import IPublicationRoot
from dolmen.app.breadcrumbs import IBreadcrumbs
from dolmen.location import get_absolute_url, lineage_chain
from grokcore.component import provider
from zope.dublincore.interfaces import IDCDescriptiveProperties


_safe = '@+'  # Characters that we don't want to have quoted


def resolve_name(item):
    """Choose a display name for the current context.
    This method has been splitted out for convenient overriding.
    """
    name = getattr(item, '__name__', None)
    if name is None and not IPublicationRoot.providedBy(item):
        raise KeyError('Object name (%r) could not be resolved.' % item)
    dc = IDCDescriptiveProperties(item, None)
    if dc is not None and dc.title:
        return name, dc.title
    return name, name


@provider(IBreadcrumbs)
def breadcrumbs(item, request):
    kin = lineage_chain(item)
    if kin:
        kin.reverse()
        root = kin.pop(0)
        base_url = get_absolute_url(root, request)
        name, title = resolve_name(root)
        yield {'name': title, 'url': base_url}

        for sibling in kin:
            name, title = resolve_name(sibling)
            base_url += '/' + urllib.quote(name.encode('utf-8'), _safe)
            yield {'name': title, 'url': base_url}
