from l20n.parser import L20nParser as Parser
from l20n.ast import LOL as Entity
from l20n.serializer import Serializer
from l20n.compiler.js import Compiler as JsCompiler
from .compiler.python import Compiler as PyCompiler
from silme.core import EntityList

class FormatParser():
    name = 'l20n'
    desc = "L20n reader/writer"
    extensions = ['lol']
    encoding = 'utf_8' # allowed encoding
    fallback = None

    @classmethod
    def dump_structure(cls, l10nobject):
        text = Serializer.serialize(l10nobject)
        return text

    @classmethod
    def dump_entitylist(cls, elist):
        text = Serializer.dump_entitylist(elist)
        return text

    @classmethod
    def get_entitylist(cls, text):
        l10nobject = cls.get_structure(text)
        entitylist = EntityList()
        for i in l10nobject:
            if isinstance(i, Entity):
                entitylist.add(i)
        return entitylist

    @classmethod
    def get_structure(cls, text):
        l10nobject = Parser().parse(text)
        return l10nobject
    
    @classmethod
    def compile(cls, structure, format='js'):
        if format=='js':
            c = JsCompiler()
        else:
            c = PyCompiler()
        j20n = c.compile(structure)
        return j20n

def register(Manager):
    Manager.register(FormatParser)
