import os
from django.http import HttpResponse
from django.conf import settings
from django.template import Template, Context, RequestContext

template = """
fragments = {
{% for fragment in fragments %}
    {{ fragment.name }}: {{ fragment.content|safe }}
{% endfor %}
}
"""

def fragments(request):
    fragments_dir = settings.FRAGMENTS_DIR
    fragments = []
    for fragment in os.listdir(fragments_dir):
        key = ".".join(fragment.split(".")[:-1])
        fragment_content = open(os.path.join(fragments_dir, fragment), "r").read()
        context = Context(RequestContext(request))
        fragments.append({
            "name": key,
            "content": Template(fragment_content).render(context).encode("Utf-8").__repr__()
        })
    return HttpResponse(Template(template).render(Context({"fragments": fragments})), content_type="text/javascript")
