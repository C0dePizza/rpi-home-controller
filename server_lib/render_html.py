from jinja2 import Environment, PackageLoader
import json
import os, sys

import plotly.tools as tls

import traceback, logging


pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"

declared_templates = {}

def main(path):
    with open(config_file) as data_file:
        data = json.load(data_file)

    env = Environment(loader=PackageLoader('web', 'templates'))
    
    if path in declared_templates and not data['WebDevMode']:
        template = declared_templates[path]
    else:
        template = env.get_template(path)
        declared_templates[path] = template

    hvac_units = data['Web']['HVAC']
    
    embeds = {}
    
    for unit in hvac_units:
        if unit['plotly']['enabled']:
            try:
                embeds[unit['Address']] = tls.get_embed(unit['plotly']['url'])
            except Exception:
                logging.exception('')
    
    html = template.render(data=data, embeds=embeds)

    return html
