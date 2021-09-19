import configparser
import sys

cfg = configparser.ConfigParser()
cfg.read(sys.argv[1])


for i in cfg:
    print(dict(cfg[i]))

