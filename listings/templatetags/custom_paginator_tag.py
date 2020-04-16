from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>
    """
    query_string = context['request'].GET.copy()
    for key, value in kwargs.items():
        query_string[key] = value
    # Remove all the empty query string values
    for key in [key for key, value in query_string.items() if not value]:
        del query_string[key]
    return query_string.urlencode()