import configparser
import pprint

pp = pprint.PrettyPrinter(indent=2)

cfg = configparser.ConfigParser()
cfg.read("config.cfg")
pp.pprint(dict(cfg['scan']))

