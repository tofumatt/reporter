import datetime
import json
from urllib import urlencode

from django.conf import settings

from jingo import register
import jinja2
from product_details.version_compare import Version

import input
from input.urlresolvers import reverse
from search.forms import ReporterSearchForm, VERSION_CHOICES


@register.function
@jinja2.contextfunction
def search_url(context, defaults=None, extra=None, feed=False, **kwargs):
    """Build a search URL with default values unless specified otherwise."""
    if feed:
        search = reverse('search.feed')
    else:
        search = reverse('search')
    if not defaults:
        defaults = {}
    data = []

    # fallbacks other than None
    fallbacks = {'version': '--'}
    if not 'product' in defaults and not 'product' in kwargs:
        prod = context['request'].default_prod
        fallbacks['product'] = prod.short
        fallbacks['version'] = (getattr(prod, 'default_version', None) or
                                Version(input.LATEST_BETAS[prod]).simplified)

    # get field data from keyword args or defaults
    for field in ReporterSearchForm.base_fields:
        val = kwargs.get(field, defaults.get(
            field, fallbacks.get(field, None)))
        if val:
            data.append((field, unicode(val).encode('utf-8')))

    # append extra fields
    if extra:
        data = dict(data)
        data.update(extra)

    return u'%s?%s' % (search, urlencode(data))


def new_context(context, **kw):
    """Helper adding variables to the existing context."""
    c = dict(context.items())
    c.update(kw)
    return c


def render_template(template, context):
    """Helper rendering a Jinja template."""
    t = register.env.get_template(template).render(context)
    return jinja2.Markup(t)


@register.function
@jinja2.contextfunction
def big_count_block(context, count):
    if not context['request'].mobile_site:
        tpl = 'search/opinion_count.html'
    else:
        tpl = 'search/mobile/opinion_count.html'
    return render_template(tpl, new_context(**locals()))


@register.function
@jinja2.contextfunction
def locales_block(context, locales, total, defaults=None):
    if not context['request'].mobile_site:
        tpl = 'search/locales.html'
    else:
        tpl = 'search/mobile/locales.html'
    return render_template(tpl, new_context(**locals()))


@register.function
@jinja2.contextfunction
def message_list(context, opinions, defaults=None, show_notfound=True):
    """A list of messages."""
    if not context['request'].mobile_site:
        tpl = 'search/message_list.html'
    else:
        tpl = 'search/mobile/message_list.html'
    return render_template(tpl, new_context(**locals()))


@register.function
@jinja2.contextfunction
def platforms_block(context, platforms, total, defaults=None):
    if not context['request'].mobile_site:
        tpl = 'search/platforms.html'
    else:
        tpl = 'search/mobile/platforms.html'
    return render_template(tpl, new_context(**locals()))


@register.function
@jinja2.contextfunction
def manufacturer_block(context, manufacturers, total, defaults=None):
    if not getattr(context['request'], 'mobile_site', False):
        tpl = 'search/manufacturers.html'
    else:
        tpl = 'search/mobile/manufacturers.html'
    return render_template(tpl, new_context(**locals()))


@register.function
@jinja2.contextfunction
def device_block(context, devices, total, defaults=None):
    if not getattr(context['request'], 'mobile_site', False):
        tpl = 'search/devices.html'
    else:
        tpl = 'search/mobile/devices.html'
    return render_template(tpl, new_context(**locals()))


@register.function
@jinja2.contextfunction
def overview_block(context, sent, defaults=None):
    if not context['request'].mobile_site:
        tpl = 'search/overview.html'
    else:
        tpl = 'search/mobile/overview.html'
    return render_template(tpl, new_context(**locals()))


@register.function
@jinja2.contextfunction
def sites_block(context, sites, defaults=None):
    """Sidebar block for frequently mentioned sites."""
    if not (settings.DATABASES.get('website_issues') and sites):
        return None

    if not context['request'].mobile_site:
        tpl = 'search/sites.html'
    else:
        tpl = 'search/mobile/sites.html'
    return render_template(tpl, new_context(**locals()))


@register.function
@jinja2.contextfunction
def themes_block(context, themes, defaults=None):
    """Sidebar block for frequently used terms."""
    if not context['request'].mobile_site:
        tpl = 'search/themes.html'
    else:
        tpl = 'search/mobile/themes.html'
    return render_template(tpl, new_context(**locals()))


@register.inclusion_tag('search/products.html')
@jinja2.contextfunction
def products_block(context, products, product):
    latest_versions = dict((prod.short,
                            Version(prod.default_version if
                                    getattr(prod, 'default_version', None)
                                    else v).simplified)
                           for prod, v in input.LATEST_BETAS.items())
    version_choices = {}
    for prod in VERSION_CHOICES:
        version_choices = json.dumps(
            dict((prod.short,
                  [map(unicode, v) for v
                   in VERSION_CHOICES[prod]]) for prod in
                 VERSION_CHOICES))
    return new_context(**locals())


@register.inclusion_tag('search/versions.html')
@jinja2.contextfunction
def versions_block(context, versions, version):
    data=dict(version=version, versions=versions)
    return new_context(data)


@register.function
@jinja2.contextfunction
def when_block(context, form, defaults=None, selected=None):
    if not context['request'].mobile_site:
        tpl = 'search/when.html'
    else:
        tpl = 'search/mobile/when.html'
    return render_template(tpl, new_context(**locals()))


@register.function
def date_ago(**kwargs):
    """Returns the date for the given timedelta from now."""
    return datetime.date.today() - datetime.timedelta(**kwargs)


@register.inclusion_tag('includes/filter_box_toggle.html')
@jinja2.contextfunction
def filter_box_toggle(context, label=''):
    return new_context(**locals())


@register.inclusion_tag('search/mobile/bar.html')
@jinja2.contextfunction
def mobile_bar(context, name, label, value=None, id=None, count=0,
               total=None, selected=False):
    """Filter / stats bars for mobile site."""
    if total:
        percentage = int(count / float(total) * 100)
    else:
        percentage = 100

    if not id:
        id = name

    return new_context(**locals())

