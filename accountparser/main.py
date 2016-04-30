import csv
import os
import sys
import logging
from urllib.parse import urljoin
from argparse import ArgumentParser
from time import strptime, strftime
import requests


def parse_args(args):
    usage = "Get account status details from API based on input account CSV."
    parser = ArgumentParser(usage=usage)

    parser.add_argument(
        "-i",
        "--input",
        dest="in_csv",
        required=True,
        help="Input CSV of account records"
    )

    parser.add_argument(
        "--url",
        dest="url",
        required=True,
        help="endpoint for account status API"
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="out_csv",
        default="output.csv",
        help="Destination for output CSV"
    )

    parser.add_argument(
        "-e",
        "--encoding",
        dest="encoding",
        default="utf-8",
        help="Input CSV's character encoding (output CSV uses same encoding)"
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Specify whether existing output files should be overwritten"
    )

    return parser.parse_args(args)


def get_account_status(url, account):
    """Fetch the status for a given account ID from the API. If status is not
    found, API returns unparsable response, or other error occurs, log & return
    None.
    """
    url = urljoin(url, account)
    request = requests.get(url)
    try:
        request.raise_for_status()
    except requests.exceptions.HTTPError:
        # 4XX or 5XX errors will raise here
        if request.status_code == 404:
            logging.error("No status found for account {}".format(account))
        else:
            logging.error("Error fetching account {} status".format(account))
        return None
    try:
        body = request.json()
    except ValueError:
        logging.error("Unable to parse status for account {}".format(account))
        return None
    return body


def create_output_row(url, row):
    """Create the output record based on an input row. Input must have a valid
    header row including column "Account ID"; rows must have values for
    "Account ID" column.
    """
    default_status = {"status": None, "created_on": None}
    try:
        account = row["Account ID"]
    except KeyError:
        logging.error("input CSV has invalid header")
        return None
    if not account:
        logging.error("Input rows must have account number values")
        return None

    status = get_account_status(url, account) or default_status
    for key in ["status", "created_on"]:
        if status.get(key) is None:
            logging.warning("No value for {} in account {}".format(key,
                                                                   account))
            status[key] = default_status[key]
    try:
        created = strptime(row.get("Created On", ""), "%m/%d/%y")
        row_created = strftime("%Y-%m-%d", created)
    except ValueError:
        logging.warning("Invalid 'Created On' for account {}".format(account))
        row_created = None

    new_row = {
        "Account ID": account,
        "First Name": row.get("First Name"),
        "Created On": row_created,
        "Status": status["status"],
        "Status Set On": status["created_on"]
    }
    return new_row


def _main(args):
    options = parse_args(args)

    if os.path.exists(options.out_csv) and options.overwrite is False:
        logging.error(
            ("Output already exists: "
             "either specify a new output filename, or use '--overwrite'")
        )
        return 1

    out_fields = [
        "Account ID", "First Name", "Created On", "Status", "Status Set On"
    ]

    # specifying newline='' per https://docs.python.org/3/library/csv.html#id3
    with open(
        options.out_csv, 'w', newline='', encoding=options.encoding
    ) as out_file:
        writer = csv.DictWriter(out_file, fieldnames=out_fields)

        with open(
            options.in_csv, newline='', encoding=options.encoding
        ) as in_file:
            writer.writeheader()
            reader = csv.DictReader(in_file)

            for row in reader:
                output = create_output_row(options.url, row)
                if output is None:
                    return 1
                writer.writerow(output)

    return 0


def main():
    sys.exit(_main(sys.argv[1:]) or 0)
