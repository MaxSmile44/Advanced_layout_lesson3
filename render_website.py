import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


NUM_BOOKS_ON_PAGE = 10


def on_reload(env):
    parser = argparse.ArgumentParser(description='Specify the path to json-file from where book data will be taken')
    parser.add_argument('-f', '--file', default='meta_data.json', type=str, help='file path')
    args = parser.parse_args()

    template = env.get_template('template.html')
    with open(args.file, 'r', encoding='utf-8') as my_file:
        meta_data_json = my_file.read()
    meta_data = json.loads(meta_data_json)
    meta_data = list(chunked(meta_data, NUM_BOOKS_ON_PAGE))
    for i, file_data in enumerate(meta_data, start=1):
        os.makedirs(os.path.join('.', 'pages'), exist_ok=True)
        rendered_page = template.render(meta_data=file_data, num_pages=len(meta_data), num_page=i)
        with open(f'./pages/index{i}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    server = Server()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    on_reload(env)
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
