import os
from django.http import HttpResponse
from django.conf import settings
from django.template import Template, Context, RequestContext

from dirty import Template1_5

try:
    from hamlpy import hamlpy
except ImportError:
    hamlpy = None

template = """
fragments = {
{% for fragment in fragments %}
    {{ fragment.name }}: {{ fragment.content|safe }}
{% endfor %}
}
"""

def fragments(request):
    fragments_dir = settings.FRAGMENTS_DIR

    if hasattr(settings, "FRAGMENTS_IGNORED_FILE_TYPES"):
        ignored_files = settings.FRAGMENTS_IGNORED_FILE_TYPES
    else:
        ignored_files = ('.swp', '.swo', '.pyc', '~')

    fragments = []
    for fragment in os.listdir(fragments_dir):
        if any(map(lambda x: fragment.endswith(x), ignored_files)):
            continue
        key = ".".join(fragment.split(".")[:-1])
        fragment_content = open(os.path.join(fragments_dir, fragment), "r").read()

        if fragment.endswith(".haml") and hamlpy is not None:
            fragment_content = hamlpy.Compiler().process(fragment_content)

        context = Context(RequestContext(request))
        fragments.append({
            "name": key,
            "content": Template1_5(fragment_content).render(context).encode("Utf-8").__repr__()
        })
    return HttpResponse(Template(template).render(Context({"fragments": fragments})), content_type="text/javascript")
