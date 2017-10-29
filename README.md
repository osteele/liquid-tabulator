# Liquid Democracy Vote Tabulator

The Olin Election Techology Co-Curricular Vote Counter tabulates votes from a Google Sheet.

We use this to vote on when and where to meet.
It has an appropriate investment in security and privacy (i.e., none).

## Setup

Install yarn. (Or npm if you must.)

Install Docker.

Follow the instructions at <https://docs.serverless.com> to credential a cloud provider.

Set environment variables:

* `LIQUID_TABULATOR_GSHEET_KEY` is the doc key of the Published Google Sheet.
* `LIQUID_TABULATOR_GSHEET_RANGE` is the cell range for vote tabulation.


```bash
$ yarn install serverless  # or npm install -g serverless
```

## Deployment

```bash
$ serverless deploy -v
```

Edit/deploy/run:

```bash
$ serverless deploy function -f tabulate
$ serverless invoke -f tabulate -l
```

## License

MIT
