import os
import sys
from os.path import join
import markdown

import settings
from flask import Flask
from jamstack.api.template import base_context, generate
from livereload import Server

context = base_context()
context.update({
    "info": settings.info
})

def md_data(text: str):
    '''
    text:
        file source
    '''
    md = markdown.Markdown(extensions=["extra", "smarty", "meta"])
    html = md.convert(text)
    metadata = md.Meta
    return {
        'html': html,
        'meta': metadata
    }


def fetch_profiles():
    profiles = []
    
    # loop trough folders
    #   read then get source file
    for file in os.listdir(settings.DATA_FOLDER):
        file_path = os.path.join(settings.DATA_FOLDER, file)
        with open(file_path) as f:
            file_data = md_data(f.read())
            file_data.update({'slug': file[:-3]})
            profiles.append(file_data)

    return profiles

coder_profiles = fetch_profiles()





def generate_profiles():
    # create /profile/
    if not os.path.exists(settings.PROFILE_FOLDER):
        os.mkdir(settings.PROFILE_FOLDER)

    for file_data in coder_profiles:
        context.update({
            'path': '../../',
            'coder_name': file_data['meta']['name'][0],
            'coder_info': file_data['meta']['info'][0],
            'coder_died': file_data['meta']['died'][0],
            'coder_text': file_data['html'],
            'page_title': file_data['meta']['name'][0]
            })
        profile_slug_path = os.path.join(settings.PROFILE_FOLDER, file_data['slug'])
        
        try:
            os.mkdir(profile_slug_path)
        except:
            pass
        generate('sections/profile.html', join(profile_slug_path, 'index.html'), **context)


def main(args):
    def gen():
        context.update({'path': './', 'coder_profiles': coder_profiles, 'page_title': 'OpenSource obituaries'})

        generate('index.html', join(
            settings.OUTPUT_FOLDER, 'index.html'), **context)

        generate_profiles()

    if len(args) > 1 and args[1] == '--server':
        app = Flask(__name__)

        # remember to use DEBUG mode for templates auto reload
        # https://github.com/lepture/python-livereload/issues/144
        app.debug = True
        server = Server(app.wsgi_app)

        # run a shell command
        # server.watch('.', 'make static')

        # run a function

        server.watch('.', gen, delay=5)
        server.watch('*.py')

        # output stdout into a file
        # server.watch('style.less', shell('lessc style.less', output='style.css'))

        server.serve()
    else:
        gen()


if __name__ == '__main__':
    main(sys.argv)
