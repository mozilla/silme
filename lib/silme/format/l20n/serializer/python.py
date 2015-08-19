from ..ast import py
import re

class Serializer(object):
    @classmethod
    def dump_element(cls, element):
        if isinstance(element, py.Str):
            string = cls.dump_str(element)
        elif isinstance(element, py.Function):
            string = cls.dump_function(element)
        elif isinstance(element, py.Script):
            string = cls.dump_script(element)
        elif isinstance(element, py.Return):
            string = cls.dump_return(element)
        elif isinstance(element, py.Idref):
            string = cls.dump_idref(element)
        elif isinstance(element, py.Assignment):
            string = cls.dump_assignment(element)
        else:
            print(type(element))
        return string

    @classmethod
    def dump_script(cls, script):
        string = ''
        lines = []
        for elem in script:
            lines.append(cls.dump_element(elem))
        string += '\n'.join(lines)
        return string

    @classmethod
    def dump_str(cls, s, var_name=None):
        if isinstance(s.data, py.OperatorExpression):
            string = cls.dump_expression(s.data)
        else:
            string = '"%s"' % s
        return string

    @classmethod
    def dump_function(cls, s):
        code = map(cls.dump_element, s)
        string = 'def %s(%s):\n%s\n' % (s.name,
                                          ', '.join(s.args),
                                          cls._indent('\n'.join(code)))
        return string

    @classmethod
    def dump_return(cls, elem):
        string = 'return %s' % cls.dump_element(elem.entry)
        return string

    @classmethod
    def dump_index(cls, elem):
        if elem.arg is not None:
            arg = cls.dump_element(elem.arg)
        else:
            arg = ''
        string = '%s[%s]' % (cls.dump_element(elem.idref), arg)
        return string

    @classmethod
    def dump_assignment(cls, elem):
        name = cls.dump_element(elem.left)
        string = '%s = %s' % (name,
                              cls.dump_element(elem.right))
        
        if hasattr(elem.right, 'properties'):
            if 'attrs' in elem.right.properties:
                params = cls.dump_object_properties(elem.right, in_struct=False, var_name=name) 
                if params:
                    string += '\n'+params
        return string

    @classmethod
    def dump_idref(cls, exp):
        for i,e in enumerate(exp):
            if isinstance(e, py.Call):
                exp[i] = cls.dump_call(e)
        return '.'.join(exp)

    @classmethod
    def dump_expression(cls, exp):
        if isinstance(exp, py.ConditionalExpression):
            return cls.dump_conditional_expression(exp)
        if isinstance(exp, py.OperatorExpression):
            return cls.dump_operator_expression(exp)
        if isinstance(exp, py.BraceExpression):
            return '(%s)' % cls.dump_expression(exp[0])
        if isinstance(exp, py.Index):
            return cls.dump_index(exp)
        if isinstance(exp, py.Idref):
            return cls.dump_idref(exp)
        if isinstance(exp, py.Str):
            return cls.dump_str(exp)
        if isinstance(exp, py.Int):
            return int(exp)
        if isinstance(exp, py.Call):
            return cls.dump_call(exp)

    @classmethod
    def dump_operator_expression(cls, e):
        s = cls.dump_expression(e[0])
        for i in range(0,1+int((len(e)-3)/2)):
            s = '%s%s%s' % (s, e[(i*2)+1], cls.dump_expression(e[2+(i*2)]))
        return s

    @classmethod
    def _indent(cls, code, val=4):
        pattern = re.compile(r'^(\s*)')
        lines = code.split('\n')
        lines = [pattern.sub('\\1%s' % ' '*val, i) for i in lines]
        return '\n'.join(lines)
