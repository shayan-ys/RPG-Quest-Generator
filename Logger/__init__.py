from os import path, remove
import logging
import logging.config
import json

with open("Logger/python_logging_configuration.json", 'r') as logging_configuration_file:
    config_dict = json.load(logging_configuration_file)


# If applicable, delete the existing log file to generate a fresh log file during each execution
if 'handlers' in config_dict:
    for key, handler in config_dict['handlers'].items():
        if 'filename' in handler:
            filename = handler['filename']
            if path.isfile(filename):
                remove(filename)

logging.config.dictConfig(config_dict)

# Log that the logger was configured
logger = logging.getLogger(__name__)
logger.info('Completed configuring logger()!')
