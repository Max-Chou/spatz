from jinja2 import Environment

# create template env
TemplateEnvironment = Environment()

def render_template(template_name, context=None):
    if context is None:
        context = {}
    return TemplateEnvironment.get_template(template_name).render(**context)
