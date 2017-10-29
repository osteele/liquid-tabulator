import io
import os
import json

try:
    import unzip_requirements
except ImportError:
    pass

import tabulator


def tabulate(event, context):
    gsheet_key = os.getenv('GOOGLE_SHEET_KEY')
    gsheet_range = os.getenv('GOOGLE_SHEET_RANGE')
    tabulation = tabulator.tabulate(gsheet_key, gsheet_range)

    with io.StringIO() as output:
        write_tabulation_html(tabulation, output)
        body = output.getvalue()

    response = {
        "statusCode": 200,
        "headers": {
            "content-type": "text/html"
        },
        "body": body
    }

    return response


def write_tabulation_html(tabulation, output):
    counts, warnings, winners = tabulation.counts, tabulation.warnings, tabulation.winners
    lines = []
    output.write('Totals:\n{}\n'.format(counts.to_string()))
    if len(winners) > 1:
        output.write('Winners (tie): {}'.format(', '.join(winners.index)))
    else:
        output.write('Winner: {}'.format(winners[0]))
    for warning in tabulation.warnings:
        output.write(warning + "\n")


def main():
    gsheet_key = os.getenv('GOOGLE_SHEET_KEY')
    gsheet_range = os.getenv('GOOGLE_SHEET_RANGE')
    tabulation = tabulator.tabulate(gsheet_key, gsheet_range)
    with io.StringIO() as output:
        write_tabulation_html(tabulation, output)
        print(output.getvalue())


if __name__ == '__main__':
    main()
