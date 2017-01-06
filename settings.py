# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json, os, pprint


print 'HERE-A'

API_BASE_URL = unicode( os.environ.get(u'OCRA_TESTS__API_BASE_URL') )

LOG_PATH = unicode( os.environ.get('OCRA_TESTS__LOG_PATH') )
LOGGING_CONF_DCT = json.loads(
    '''
    {
      "handlers": {
        "logfile": {
          "formatter": "standard",
          "class": "logging.FileHandler",
          "filename": "foo",
          "level": "DEBUG"
        },
        "console": {
          "formatter": "standard",
          "class": "logging.StreamHandler",
          "level": "DEBUG"
        }
      },
      "loggers": {
        "": {
          "level": "DEBUG",
          "propagate": true,
          "handlers": [
            "logfile"
          ]
        }
      },
      "version": 1,
      "disable_existing_loggers": false,
      "formatters": {
        "standard": {
          "datefmt": "%d/%b/%Y %H:%M:%S",
          "format": "[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s"
        }
      }
    }
    '''
    )
LOGGING_CONF_DCT['handlers']['logfile']['filename'] = LOG_PATH

print 'LOGGING_CONF_DCT, ```{}```'.format( pprint.pformat(LOGGING_CONF_DCT) )

