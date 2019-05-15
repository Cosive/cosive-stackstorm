import sys

from st2common.runners.base_action import Action
from spam_lists import SPAMHAUS_ZEN #, GoogleSafeBrowsing

class RblLookupAction(Action):
    def run(self, domain):
        result = []
        if domain in SPAMHAUS_ZEN:
            result.append('SPAMHAUS_ZEN')
        #if GoogleSafeBrowsing.lookup(domain):
        #    result.append('GoogleSafeBrowsing')
        return (True, result)
