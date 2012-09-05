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
    "{{ fragment.name }}": {{ fragment.content|safe }},
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
    for root, dirnames, filenames in os.walk(fragments_dir):
        for fragment in filenames:
            if any(map(lambda x: fragment.endswith(x), ignored_files)):
                continue
            key = ".".join(fragment.split(".")[:-1])
            if root != fragments_dir:
                key = "_".join([os.path.split(root)[1], key])
            fragment_content = open(os.path.join(root, fragment), "r").read()

            if fragment.endswith(".haml") and hamlpy is not None:
                fragment_content = hamlpy.Compiler().process(fragment_content.decode("Utf-8"))

            context = Context(RequestContext(request))
            fragments.append({
                "name": key,
                "content": Template1_5(fragment_content).render(context).strip().__repr__()[1:]
            })
    return HttpResponse(Template(template).render(Context({"fragments": fragments})), content_type="text/javascript")
