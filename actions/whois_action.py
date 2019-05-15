#!/usr/bin/env python
# Based on https://github.com/yaleman/st2-whois but with the engine swapped out.
import re
from datetime import datetime
from utils import *
if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action
else:
    Action = Object

import pythonwhois

from urlparse import urlparse


class Whois(Action):
    def run(self, query, *args):
        # rip out newlines and gibberish
        query = query.strip()
        # replace the misp-style de-fanging
        query = query.replace("[", "")
        query = query.replace("]", "")

        parsed_uri = urlparse(query)
        try:
            if parsed_uri.netloc == '' and re.match('^\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}$', query):
                self.logger.debug("whois on ip '{}'".format(query))
                return (False, "Only domains are supported for this action currently")
            elif parsed_uri.netloc == '' and parsed_uri.path != '':
                self.logger.debug("whois on domain '{}'".format(parsed_uri.path))
                w = pythonwhois.get_whois(parsed_uri.path)
            else:
                self.logger.debug("whois on domain '{}'".format(parsed_uri.netloc))
                w = pythonwhois.get_whois(parsed_uri.netloc)
        except pythonwhois.shared.WhoisException as e:
            return (False, {'error' : e})

        if w.get('status', False) == False:
            return (False, {'error' : "No result returned"})

        result = clean_dict(w)
        return (True, result)