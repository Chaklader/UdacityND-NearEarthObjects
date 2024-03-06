"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach

import csv
import json


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    with open(neo_csv_path, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                neo = NearEarthObject(
                    designation=row["pdes"],
                    name=row["name"] or None,
                    diameter=float(row["diameter"]) if row["diameter"] else None,
                    hazardous=False if row["pha"] in ["", "N"] else True,
                )
                neos.append(neo)
            except (KeyError, ValueError) as err:
                print(f"Error creating NearEarthObject: {err}")
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.

    fields are as per JSON file ["des", "orbit_id", "jd", "cd", "dist", "dist_min", "dist_max", "v_rel", "v_inf", "t_sigma_f", "h"]
    """
    approaches = []
    with open(cad_json_path, "r") as infile:
        data = json.load(infile)
        for row in data["data"]:
            try:
                approach = CloseApproach(
                    designation=row[0],
                    time=row[3],
                    distance=float(row[4]),
                    velocity=float(row[7]),
                )
                approaches.append(approach)
            except (IndexError, ValueError) as err:
                print(f"Error creating CloseApproach: {err}")
    return approaches
