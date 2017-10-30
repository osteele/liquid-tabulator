"""Liquid Democracy vote tabulator.

Usage:
  tabulator.py SPREADSHEET_KEY SPREADSHEET_RANGE
"""

import sys
from collections import namedtuple

import pandas as pd

Tabulation = namedtuple('Tabulation', ['counts', 'winners', 'warnings'])


def tabulate(spreadsheet_key, spreadsheet_range):
    url = 'https://docs.google.com/spreadsheets/d/e/{}/pub?gid=0&single=true&output=csv'.format(
        spreadsheet_key)
    if spreadsheet_range:
        url += '&range=' + spreadsheet_range

    df = pd.read_csv(url, names=['Voter', 'Vote',
                                 'Delegate', 'Position'], index_col=0)

    warnings = []
    dups = df.index.get_duplicates()
    if dups:
        warnings.append("{} voted twice".format(', '.join(dups)))

    # Remove voters who neither voted nor delegated
    df = df.loc[~df['Vote'].isnull() | ~df['Delegate'].isnull()]

    # Fill in missing votes by delegates' votes, or delegates' delegates' votes, etc.
    df = fixed_point(follow_delegates, df)

    # Warn (don't error) on unresolved votes.
    # FIXME "voters" who entered neither a vote nor delegate should be reported separately
    nas = df['Vote'].isnull().sum()
    if nas:
        warnings.append("{} delegated votes did not resolve".format(nas))

    counts = df['Vote'].value_counts()
    winners = counts[counts == counts[counts.idxmax()]].index
    return Tabulation(counts=counts, warnings=warnings, winners=winners)


def fixed_point(fn, df):
    """Find the fixed point of a DataFrame function."""
    while True:
        df0, df = df, fn(df)
        if df.equals(df0):
            return df


def follow_delegates(votes):
    """Return a new DataFrame with delegates replaced by those delegates' votes."""
    # Each voter's delegate, or themself if they didn't choose a delegate
    delegates = votes['Delegate'].fillna(votes.index.to_series())
    delegate_vote = delegates.apply(dict(votes['Vote']).__getitem__)
    return votes.assign(Vote=votes['Vote'].fillna(delegate_vote))


def report_tabulation(tabulation):
    counts, warnings, winners = tabulation.counts, tabulation.warnings, tabulation.winners
    for warning in tabulation.warnings:
        sys.stderr.write(warning + "\n")
    print('Totals:\n{}\n'.format(counts.to_string()))
    if len(winners) > 1:
        print('Winners (tie):', ', '.join(winners.index))
    else:
        print('Winner:', winners[0])


if __name__ == '__main__':
    from docopt import docopt
    args = docopt(__doc__)
    tabulation = tabulate(args['SPREADSHEET_KEY'], args['SPREADSHEET_RANGE'])
    report_tabulation(tabulation)
