import os
import argparse
import csv
import update

#'C:\Users\KIRAJU\Documents\FDX_Test_CSV_V1.csv'


def handle_csv(func, resource_type):
    try:
        with open(args.csv_file, mode="r") as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                id = lines.pop(list(lines.keys())[0])
                func(resource_id=id, tags=lines, resource_type=resource_type)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    description = "\n".join(
        [
            "This updates the tags",
            "pip install -r requirements.txt",
            "python main.py <config_profile>",
        ]
    )
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("resource", help="Enter the resource to be updated")
    parser.add_argument(
        "--csv_file",
        help="Enter the full path/location of the csv file.",
        required=True,
    )
    args = parser.parse_args()
    resource_type = args.resource
    handle_csv(update.update_tag, resource_type)

