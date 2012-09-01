from django.template.base import Node, Library, Context

# code extracted for django 1.5 dev code source

register = Library()

class VerbatimNode(Node):
    def __init__(self, content):
        self.content = content

    def render(self, context):
        return self.content


@register.tag
def verbatim(parser, token):
    """
Stops the template engine from rendering the contents of this block tag.

Usage::

{% verbatim %}
{% don't process this %}
{% endverbatim %}

You can also designate a specific closing tag block (allowing the
unrendered use of ``{% endverbatim %}``)::

{% verbatim myblock %}
...
{% endverbatim myblock %}
"""
    nodelist = parser.parse(('endverbatim',))
    parser.delete_first_token()
    return VerbatimNode(nodelist.render(Context()))
