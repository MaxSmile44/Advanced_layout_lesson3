import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


server = Server()
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def on_reload():
    template = env.get_template('template.html')
    with open('meta_data.json', 'r', encoding='utf-8') as my_file:
        meta_data_json = my_file.read()
    meta_data = json.loads(meta_data_json)
    rendered_page = template.render(meta_data=meta_data)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


server.watch('template.html', on_reload)
server.serve(root='index.html')