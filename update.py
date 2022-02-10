from jinja2 import Environment, FileSystemLoader
import yaml
import pathlib
from time import gmtime, asctime
import os

TEMPLATE_ENV_PATH = "./template"
MAIN_TEMPLATE = "main.html"
BLOG_TEMPLATE = "blogi.html"
OUTPUT = "./index.html"
TEMPLATE_ENV = Environment(loader=FileSystemLoader(searchpath=TEMPLATE_ENV_PATH))


def get_blogs(dir):
    """
    Reads blogs from `dir`.

    Return: list of dict-items containing blog data
    """
    blogs = []
    for file in sorted(pathlib.Path(dir).iterdir(), key=os.path.getmtime, reverse=True):
        with open(file, 'r') as blog_f:
            blog = yaml.safe_load(blog_f)
            blog['date'] = asctime(gmtime(file.stat().st_mtime))
            blogs.append(blog)

    return blogs

if __name__ == '__main__':
    template = TEMPLATE_ENV.get_template(MAIN_TEMPLATE)

    with open('config.yaml', 'r') as conf_f:
        conf = yaml.safe_load(conf_f)
        blogdir = conf['blogdir']
        name = conf['name']

    kwargs = {
        'blogin_nimi': name,
        'blogs': get_blogs(blogdir)
    }

    with open(OUTPUT, 'w') as outfile:
        outfile.write(template.render(**kwargs))


