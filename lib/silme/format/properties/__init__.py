import sys
from .parser import PropertiesParser as Parser
from .serializer import PropertiesSerializer as Serializer

if sys.version_info[0] > 2:
    # for python3
    unichr = chr


class FormatParser(object):
    name = 'properties'
    desc = "Java Properties reader/writer"
    extensions = ['properties']
    encoding = 'utf_8' # allowed encoding
    fallback = ['utf_8_sig']

    @classmethod
    def dump_structure (cls, l10nobject):
        text = Serializer.serialize(l10nobject)
        return text

    @classmethod
    def dump_entitylist (cls, elist):
        text = Serializer.dump_entitylist(elist)
        return text

    @classmethod
    def get_entitylist (cls, text, code='default'):
        # remove the \ufeff character from the beginning of the file, dirty hack for now
        if text and (text[0] == unichr(65279)):
            text = text[1:]
        l10nobject = Parser.parse_to_entitylist(text)
        return l10nobject

    @classmethod
    def get_structure (cls, text, code='default'):
        # remove the \ufeff character from the beginning of the file, dirty hack for now
        if text and (text[0] == unichr(65279)):
            text = text[1:]
        l10nobject = Parser.parse(text, code=code)
        return l10nobject


def register(Manager):
    Manager.register(FormatParser)
