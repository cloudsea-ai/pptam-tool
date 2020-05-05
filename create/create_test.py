#!/usr/bin/env python3.7

import os
import shutil
import json
import argparse
import logging
import uuid
from datetime import datetime
from os import path
from tools import replace_values_in_file


def create_test(configuration_file_path, configuration_entries_to_overwrite):
    if not path.exists(configuration_file_path):
        logging.fatal(f"Cannot find the configuration file {configuration_file_path}.")
        quit()

    with open(configuration_file_path, "r") as f:
        configuration = json.load(f)["Configuration"]

    for argument in configuration_entries_to_overwrite:
        parts = argument.split('=')
        configuration[parts[0]] = parts[1]

    output = configuration["test_case_creation_folder"]
    if not path.isdir(output):
        logging.debug(f"Creating {output}, since it does not exist.")
        os.makedirs(output)

    path_to_templates = path.abspath("./templates")
    path_to_drivers = path.abspath("./drivers")
    path_to_temp = path.join(path_to_drivers, "tmp")

    now = datetime.now()
    test_id = configuration["test_case_prefix"] + "-" + \
        now.strftime("%Y%m%d%H%M%S") + "-" + str(uuid.uuid4())[:8]
    logging.debug(f"Generating a test with the id {test_id} in {path_to_temp}.")

    if path.isdir(path_to_temp):
        shutil.rmtree(path_to_temp)

    logging.debug(f"Creating new driver, based on the templates in {path_to_templates}.")
    shutil.copytree(path.join(path_to_templates, "faban", "driver", "ecsa"), path_to_temp)
    shutil.copyfile(path.join(path_to_templates, "deployment_descriptor", "template", "docker-compose.yml"), path.join(path_to_temp, "deploy", "docker-compose.yml"))

    replacements = []
    for entry in configuration:
        replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": configuration[entry]})
        replacements.append({"search_for": "${" + entry.lower() + "}", "replace_with": configuration[entry]})

    replacements.append({"search_for": "${TEST_NAME}", "replace_with": test_id})

    logging.debug(f"Replacing values.")
    replace_values_in_file(path.join(path_to_temp, "build.properties"), replacements)
    replace_values_in_file(path.join(path_to_temp, "deploy", "run.xml"), replacements)
    shutil.copyfile(path.join(path_to_temp, "deploy", "run.xml"), path.join(path_to_temp, "config", "run.xml"))
    replace_values_in_file(path.join(path_to_temp, "src", "ecsa", "driver", "WebDriver.java"), replacements)
    replace_values_in_file(path.join(path_to_temp, "deploy", "docker-compose.yml"), replacements)

    logging.debug("Compiling the Faban driver")
    current_folder = os.getcwd()
    os.chdir(path_to_temp)
    command = "ant deploy.jar -q -S"
    result = os.system(command)
    os.chdir(current_folder)

    if result != 0:
        logging.fatal(f"Could not compile test in {path_to_temp}.")
        quit()

    path_to_output = path.join(path.abspath(output), test_id)
    logging.info(f"Writing the test case into {path_to_output}.")

    os.makedirs(path_to_output)
    shutil.copyfile(path.join(path_to_temp, "build", f"{test_id}.jar"), path.join(path_to_output, f"{test_id}.jar"))
    shutil.copyfile(path.join(path_to_temp, "config", "run.xml"), path.join(path_to_output, "run.xml"))
    shutil.copyfile(path.join(path_to_temp, "deploy", "docker-compose.yml"), path.join(path_to_output, "docker-compose.yml"))
    shutil.move(path_to_temp, path.join(path_to_drivers, test_id))
    logging.info(f"Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates test cases.")
    parser.add_argument("--configuration", metavar="path_to_configuration_file", help="Configuration file", default="configuration.json")
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)
    parser.add_argument("--overwrite", help="Configuration values, which overwrite the values in the configuration file. Format: name1=value1 name2=value2 ...", metavar="key=value", nargs="+", default=[])
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
    create_test(args.configuration, args.overwrite)
