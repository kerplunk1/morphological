from collections import defaultdict
from operator import attrgetter
import argparse
import pymorphy3


GRAM_CHOICES = ('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen2', 'acc2', 'loc2', 'sing', 'plur')


class PhraseInflector(object):
    class ScoreHelper(object):
        score = 0
        fixed_number_score = 0

        def __init__(self, parsed):
            self.parsed = parsed

    def __init__(self, morph):
        self.morph = morph

    def parse_first(self, word):
        parse = self.morph.parse(word)
        if len(parse) > 0:
            return parse[0]
        else:
            return None

    def select_master(self, phrase):
        versions = []
        for i, word in enumerate(phrase):
            forms = defaultdict(list)
            # If a word identified as noun may also be identified as participle, adjective or adjective
            # it is less likely to be a real noun
            is_derivative = any({'ADJF', 'PRTF', 'GRND'} & version.tag.grammemes for version in self.morph.parse(word))

            for j, parsed in enumerate(self.morph.parse(word)):

                if {'NOUN', 'nomn'} in parsed.tag:
                    version = self.ScoreHelper(parsed)
                    version.fixed_number_score = 1 if ({'Pltm', 'Sgtm'} & set(parsed.tag.grammemes)) else 0
                    version.score = (100.0 * parsed.score / (1.0 + 0.2 * j + (1 if is_derivative else 0))
                                     + 20 / (0.2 * i + 1))
                    forms[parsed.score].append(version)
            # all other things being equal, fixed number forms will score better
            forms_pass = [max(x, key=attrgetter('fixed_number_score')) for x in forms.values()]
            versions.extend(forms_pass)

        if versions:
            return sorted(versions, key=attrgetter('score'), reverse=True)[0]
        else:
            return None

    def inflect(self, phrase, form):
        # phrase = phrase.lower()
        master_word = self.select_master(phrase.lower().split())
        if master_word:
            return self._inflect_with_master(form, phrase, master_word.parsed)
        else:
            return self._inflect_without_master(form, phrase)

    def _inflect_with_master(self, form, phrase, master_word):
        result = []
        if isinstance(form, str):
            form = {form}
        else:
            form = set(form)
        # Do not inflect in numbers if master word is always plur or sing
        if {'Pltm', 'Sgtm'} & set(master_word.tag.grammemes):
            form = form - {'sing', 'plur'}

        infl = form
        inflected_master = master_word.inflect(infl)

        for chunk in phrase.split():
            parsed_chunk = self.morph.parse(chunk)
            if chunk.lower() == master_word.word.lower():
                if inflected_master:
                    result.append(inflected_master.word)
                else:
                    result.append(chunk)
                continue

            dependent = None
            for version in parsed_chunk:
                # If POS should adopt the form AND was in the same case(падеж) which the master word had
                if version.tag.POS in (u'ADJF', u'PRTF') and version.tag.case == master_word.tag.case:
                    infl = form | {inflected_master.tag.number}
                    # If in the single number, adopt the gender of master word
                    if inflected_master.tag.number == 'sing':
                        infl.add(inflected_master.tag.gender)

                    if (u'accs' in form) \
                            and (inflected_master.tag.gender == u'masc' or inflected_master.tag.number == u'plur'):
                        infl.add(master_word.tag.animacy)

                    try:
                        inflected = version.inflect(infl)
                    except ValueError as e:
                        dependent = version
                    else:
                        if inflected:
                            dependent = inflected
                        else:
                            dependent = version
                    break

            if dependent:
                result.append(dependent.word)
            else:
                result.append(chunk)

        return u' '.join(result)

    def _inflect_without_master(self, form, phrase):
        result = []
        if isinstance(form, str):
            form = {form}
        else:
            form = set(form)
        for chunk in phrase.split():
            parsed_chunk = self.parse_first(chunk)
            if not parsed_chunk:
                result.append(chunk)
                continue
            if not any(form in parsed_chunk.tag for form in ({'NOUN', 'nomn'}, {'ADJF', 'nomn'})):
                result.append(chunk)
                continue
            infl = form
            if u'accs' in form:
                infl.add('inan')
            try:
                inflected = parsed_chunk.inflect(infl)
                if inflected:
                    result.append(inflected.word)
                else:
                    result.append(chunk)
            except ValueError:
                result.append(chunk)

        return u' '.join(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inflect input phrase')
    args = parser.parse_args()

    morph = pymorphy3.MorphAnalyzer()
    inflector = PhraseInflector(morph)
    if isinstance(args.word, bytes):
        args.word = args.word.decode('utf8')
    print(inflector.inflect(args.word, args.gram))