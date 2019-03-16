import os
import yaml
from collections import namedtuple

CONFIG_YAML = './config/db.yaml'
assert os.path.exists(CONFIG_YAML), "Missing config file: {}".format(CONFIG_YAML)

config = yaml.load(open(CONFIG_YAML))
