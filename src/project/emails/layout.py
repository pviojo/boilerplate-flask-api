import os
from datetime import date
from pathlib import Path

from flask import render_template_string, Response
from premailer import transform

class Layout:

    @classmethod
    def process(
        cls,
        template=None,
        css=None,
        body=None,
        params=None
            ):
        folder = os.path.dirname(os.path.abspath(__file__))
        if template is not None:

            css = None
            css_file = '%s/layouts/%s/index.css' % (folder, template)

            if css_file is not None and Path(css_file).is_file():
                f = open(css_file, 'r')
                css = f.read()
                f.close

            html_file = '%s/layouts/%s/index.html' % (folder, template)
            if Path(html_file).is_file():
                f = open(html_file, 'r')
                html = f.read()
                f.close

                if params:
                    html = cls.process_params(html=html, params=params)
                
                if css is not None:
                    html = html.replace(
                        '%%css%%', '<style type="text/css">' + css + '</style>')
                body = html.replace('%%body%%', body)
        else:
            body = """
                <html>
                <style type="text/css">
                %s
                </style>
                <body>
                %s
                </body>
            """ % (css, body)

        body = transform(body)

        return body

    @classmethod
    def process_params(cls, html=None, params=None):
        try:
            return render_template_string(
                html,
                params=params
            )
        except Exception as e:
            print(e)
            return html
