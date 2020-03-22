import os
import sys
import yaml


def update_json_file(url):
    full_path = os.path.abspath("services/swagger/swagger.yml")
    with open(full_path, "r") as file:
        data = yaml.load(file, yaml.FullLoader)
    data["servers"][0]["url"] = url
    with open(full_path, "w") as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)
    return True


if __name__ == "__main__":
    try:
        update_json_file(sys.argv[1])
    except IndexError:
        print("Please provide a URL.")
        print("USAGE: python update-spec.py URL")
        sys.exit()
