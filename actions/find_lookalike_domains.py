if __name__ != "__main__":
    from st2common.runners.base_action import Action
    class CompareDomainsAction(Action):
        def run(self, domain, domain_list, threshold, check_homoglyphs):
            r = compare(domain, domain_list, threshold, check_homoglyphs)
            return r

import jellyfish
import homoglyphs as hg
import sys

def compare(domain, domain_list, threshold, check_homoglyphs):
    result = []
    domain = domain.lower()
    if check_homoglyphs:
        homoglyphs = hg.Homoglyphs(languages={'en'}, strategy=hg.STRATEGY_LOAD)
        print ("loaded homoglyphs")
        variants = homoglyphs.to_ascii(domain)
        print("found {} variants: {}".format(len(variants), variants))
    else:
        variants = [domain]
    for domain_appearance in variants:
        print("checking {}".format(domain_appearance))
        domain_appearance = domain_appearance.lower()
        for good_domain in domain_list:
            good_domain = good_domain.lower()
            score = jellyfish.jaro_winkler(unicode(domain),unicode(good_domain))
            print ("{} matched {} at score: {}".format(domain_appearance,good_domain, score))
            if score >= threshold:
                result.append(good_domain)
        return (True, result)

if __name__ == "__main__":
    r = compare(sys.argv[1],["goodbank.com"],0.9, false)
    print ("returned: {}".format(r))
