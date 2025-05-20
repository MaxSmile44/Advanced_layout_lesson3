import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


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
    meta_data = list(chunked(meta_data, 10))
    for i, file_data in enumerate(meta_data, start=1):
        os.makedirs(os.path.join('.', 'pages'), exist_ok=True)
        rendered_page = template.render(meta_data=file_data, num_pages=len(meta_data), num_page=i)
        with open(f'./pages/index{i}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
