import os
import json

try:
    import unzip_requirements
except ImportError:
    pass

from jinja2 import Environment, Template
import pandas as pd

import tabulator


def dataframe_table_filter(df, **kwargs):
    """A Jinja filter that turns a Pandas DataFrame into HTML.

    Keyword arguments are passed to DataFrame.to_html.
    The Pandas display option is dynamically set to allow full-width text in the cells.
    """
    pd_display_max_colwidth_key = 'display.max_colwidth'
    saved_max_colwidth = pd.get_option(pd_display_max_colwidth_key)
    try:
        pd.set_option(pd_display_max_colwidth_key, -1)
        return df.to_html(**kwargs)
    finally:
        pd.set_option(pd_display_max_colwidth_key, saved_max_colwidth)


def series_table_filter(series):
    return dataframe_table_filter(pd.DataFrame(series), classes=['table', 'table-sm'])


env = Environment()
env.filters['series_table'] = series_table_filter

with open(os.path.join(os.path.dirname(__file__), './results.html')) as f:
    template = env.from_string(f.read())

GITHUB_REPO_URL = os.getenv('GITHUB_REPO_URL')


def tabulate(event, context):
    gsheet_key = os.getenv('GOOGLE_SHEET_KEY')
    gsheet_range = os.getenv('GOOGLE_SHEET_RANGE')
    tabulation = tabulator.tabulate(gsheet_key, gsheet_range)
    body = template.render(
        results=tabulation, github_repo_url=GITHUB_REPO_URL, title='Poll Results')

    response = {
        "statusCode": 200,
        "headers": {
            "content-type": "text/html"
        },
        "body": body
    }

    return response


def test():
    gsheet_key = os.getenv('GOOGLE_SHEET_KEY')
    gsheet_range = os.getenv('GOOGLE_SHEET_RANGE')
    tabulation = tabulator.tabulate(gsheet_key, gsheet_range)
    print(template.render(
        results=tabulation, github_repo_url=GITHUB_REPO_URL, title='Poll Results'))


if __name__ == '__main__':
    test()
