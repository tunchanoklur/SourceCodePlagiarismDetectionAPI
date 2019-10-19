#-----------------------------------------------------------------
# ** ATTENTION **
# This code was automatically generated from the file:
# _c_ast.cfg
#
# Do not modify it directly. Modify the configuration file and
# run the generator again.
# ** ** *** ** **
#
# pycparser: c_ast.py
#
# AST Node classes.
#
# Eli Bendersky [https://eli.thegreenplace.net/]
# License: BSD
#-----------------------------------------------------------------


import sys

def _repr(obj):
    """
    Get the representation of an object, with dedicated pprint-like format for lists.
    """
    if isinstance(obj, list):
        return '[' + (',\n '.join((_repr(e).replace('\n', '\n ') for e in obj))) + '\n]'
    else:
        return repr(obj) 

class Node(object):
    __slots__ = ()
    """ Abstract base class for AST nodes.
    """
    def __repr__(self):
        """ Generates a python representation of the current node
        """
        result = self.__class__.__name__ + '('
        
        indent = ''
        separator = ''
        for name in self.__slots__[:-2]:
            result += separator
            result += indent
            result += name + '=' + (_repr(getattr(self, name)).replace('\n', '\n  ' + (' ' * (len(name) + len(self.__class__.__name__)))))
            
            separator = ','
            indent = '\n ' + (' ' * len(self.__class__.__name__))
        
        result += indent + ')'
        
        return result

    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ Pretty print the Node and all its attributes and
            children (recursively) to a buffer.

            buf:
                Open IO buffer into which the Node is printed.

            offset:
                Initial offset (amount of leading spaces)

            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.

            nodenames:
                True if you want to see the actual node names
                within their parents.

            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """
        lead = ' ' * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__+ ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            buf.write(' (at %s)' % self.coord)
        buf.write('\n')

        for (child_name, child) in self.children():
            child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)


class NodeVisitor(object):
    """ A base NodeVisitor class for visiting c_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.

        For example:

        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []

            def visit_Constant(self, node):
                self.values.append(node.value)

        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:

        cv = ConstantVisitor()
        cv.visit(node)

        Notes:

        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """

    _method_cache = None

    def visit(self, node):
        """ Visit a node.
        """

        if self._method_cache is None:
            self._method_cache = {}

        visitor = self._method_cache.get(node.__class__.__name__, None)
        if visitor is None:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            self._method_cache[node.__class__.__name__] = visitor

        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c in node:
            self.visit(c)

class ArrayDecl(Node):
    __slots__ = ('type', 'dim', 'dim_quals', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, type, dim, dim_quals, coord=None, self_hash = None, recur_hash = None):
        self.type = type
        self.dim = dim
        self.dim_quals = dim_quals
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        if self.dim is not None: nodelist.append(("dim", self.dim))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type
        if self.dim is not None:
            yield self.dim

    attr_names = ('dim_quals', 'self_hash', 'recur_hash', )

class ArrayRef(Node):
    __slots__ = ('name', 'subscript', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, subscript, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.subscript = subscript
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.subscript is not None: nodelist.append(("subscript", self.subscript))
        return tuple(nodelist)

    def __iter__(self):
        if self.name is not None:
            yield self.name
        if self.subscript is not None:
            yield self.subscript

    attr_names = ('self_hash', 'recur_hash', )

class Assignment(Node):
    __slots__ = ('op', 'lvalue', 'rvalue', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, op, lvalue, rvalue, coord=None, self_hash = None, recur_hash = None):
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        if self.lvalue is not None: nodelist.append(("lvalue", self.lvalue))
        if self.rvalue is not None: nodelist.append(("rvalue", self.rvalue))
        return tuple(nodelist)

    def __iter__(self):
        if self.lvalue is not None:
            yield self.lvalue
        if self.rvalue is not None:
            yield self.rvalue

    attr_names = ('op', 'self_hash', 'recur_hash', )

class BinaryOp(Node):
    __slots__ = ('op', 'left', 'right', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, op, left, right, coord=None, self_hash = None, recur_hash = None):
        self.op = op
        self.left = left
        self.right = right
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        if self.left is not None: nodelist.append(("left", self.left))
        if self.right is not None: nodelist.append(("right", self.right))
        return tuple(nodelist)

    def __iter__(self):
        if self.left is not None:
            yield self.left
        if self.right is not None:
            yield self.right

    attr_names = ('op', 'self_hash', 'recur_hash', )

class Break(Node):
    __slots__ = ( 'coord','self_hash', 'recur_hash', '__weakref__')
    def __init__(self, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('self_hash', 'recur_hash', )

class Case(Node):
    __slots__ = ('expr', 'stmts', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, expr, stmts, coord=None, self_hash = None, recur_hash = None):
        self.expr = expr
        self.stmts = stmts
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        for i, child in enumerate(self.stmts or []):
            nodelist.append(("stmts[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        if self.expr is not None:
            yield self.expr
        for child in (self.stmts or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class Cast(Node):
    __slots__ = ('to_type', 'expr', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, to_type, expr, coord=None, self_hash = None, recur_hash = None):
        self.to_type = to_type
        self.expr = expr
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        if self.to_type is not None: nodelist.append(("to_type", self.to_type))
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    def __iter__(self):
        if self.to_type is not None:
            yield self.to_type
        if self.expr is not None:
            yield self.expr

    attr_names = ('self_hash', 'recur_hash', )

class Compound(Node):
    __slots__ = ('block_items', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, block_items, coord=None, self_hash = None, recur_hash = None):
        self.block_items = block_items
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.block_items or []):
            nodelist.append(("block_items[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.block_items or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class CompoundLiteral(Node):
    __slots__ = ('type', 'init', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, type, init, coord=None, self_hash = None, recur_hash = None):
        self.type = type
        self.init = init
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        if self.init is not None: nodelist.append(("init", self.init))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type
        if self.init is not None:
            yield self.init

    attr_names = ('self_hash', 'recur_hash', )

class Constant(Node):
    __slots__ = ('type', 'value', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, type, value, coord=None, self_hash = None, recur_hash = None):
        self.type = type
        self.value = value
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('type', 'value', 'self_hash', 'recur_hash', )

class Continue(Node):
    __slots__ = ('coord','self_hash', 'recur_hash', '__weakref__')
    def __init__(self, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('self_hash', 'recur_hash', )

class Decl(Node):
    __slots__ = ('name', 'quals', 'storage', 'funcspec', 'type', 'init', 'bitsize', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, quals, storage, funcspec, type, init, bitsize, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.quals = quals
        self.storage = storage
        self.funcspec = funcspec
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.type = type
        self.init = init
        self.bitsize = bitsize
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        if self.init is not None: nodelist.append(("init", self.init))
        if self.bitsize is not None: nodelist.append(("bitsize", self.bitsize))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type
        if self.init is not None:
            yield self.init
        if self.bitsize is not None:
            yield self.bitsize

    attr_names = ('name', 'quals', 'storage', 'funcspec', 'self_hash', 'recur_hash', )

class DeclList(Node):
    __slots__ = ('decls', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, decls, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.decls = decls
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.decls or []):
            nodelist.append(("decls[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.decls or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class Default(Node):
    __slots__ = ('stmts', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, stmts, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.stmts = stmts
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.stmts or []):
            nodelist.append(("stmts[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.stmts or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class DoWhile(Node):
    __slots__ = ( 'cond', 'stmt', 'coord','self_hash', 'recur_hash', '__weakref__')
    def __init__(self, cond, stmt, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.stmt is not None: nodelist.append(("stmt", self.stmt))
        return tuple(nodelist)

    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.stmt is not None:
            yield self.stmt

    attr_names = ('self_hash', 'recur_hash', )

class EllipsisParam(Node):
    __slots__ = ('coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('self_hash', 'recur_hash', )

class EmptyStatement(Node):
    __slots__ = ('coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('self_hash', 'recur_hash', )

class Enum(Node):
    __slots__ = ('name', 'values', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, values, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.values = values
        self.coord = coord

    def children(self):
        nodelist = []
        if self.values is not None: nodelist.append(("values", self.values))
        return tuple(nodelist)

    def __iter__(self):
        if self.values is not None:
            yield self.values

    attr_names = ('name', 'self_hash', 'recur_hash', )

class Enumerator(Node):
    __slots__ = ('name', 'value', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, value, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        if self.value is not None: nodelist.append(("value", self.value))
        return tuple(nodelist)

    def __iter__(self):
        if self.value is not None:
            yield self.value

    attr_names = ('name', 'self_hash', 'recur_hash', )

class EnumeratorList(Node):
    __slots__ = ('enumerators', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, enumerators, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.enumerators = enumerators
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.enumerators or []):
            nodelist.append(("enumerators[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.enumerators or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class ExprList(Node):
    __slots__ = ('exprs', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, exprs, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.exprs = exprs
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.exprs or []):
            nodelist.append(("exprs[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.exprs or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class FileAST(Node):
    __slots__ = ('ext', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, ext, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.ext = ext
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.ext or []):
            nodelist.append(("ext[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.ext or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class For(Node):
    __slots__ = ('init', 'cond', 'next', 'stmt', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, init, cond, next, stmt, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.init = init
        self.cond = cond
        self.next = next
        self.stmt = stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.init is not None: nodelist.append(("init", self.init))
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.next is not None: nodelist.append(("next", self.next))
        if self.stmt is not None: nodelist.append(("stmt", self.stmt))
        return tuple(nodelist)

    def __iter__(self):
        if self.init is not None:
            yield self.init
        if self.cond is not None:
            yield self.cond
        if self.next is not None:
            yield self.next
        if self.stmt is not None:
            yield self.stmt

    attr_names = ('self_hash', 'recur_hash', )

class FuncCall(Node):
    __slots__ = ('name', 'args', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, args, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.name = name
        self.args = args
        self.coord = coord

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.args is not None: nodelist.append(("args", self.args))
        return tuple(nodelist)

    def __iter__(self):
        if self.name is not None:
            yield self.name
        if self.args is not None:
            yield self.args

    attr_names = ('self_hash', 'recur_hash', )

class FuncDecl(Node):
    __slots__ = ('args', 'type', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, args, type, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.args = args
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.args is not None: nodelist.append(("args", self.args))
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)

    def __iter__(self):
        if self.args is not None:
            yield self.args
        if self.type is not None:
            yield self.type

    attr_names = ('self_hash', 'recur_hash', )

class FuncDef(Node):
    __slots__ = ('decl', 'param_decls', 'body', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, decl, param_decls, body, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.decl = decl
        self.param_decls = param_decls
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.decl is not None: nodelist.append(("decl", self.decl))
        if self.body is not None: nodelist.append(("body", self.body))
        for i, child in enumerate(self.param_decls or []):
            nodelist.append(("param_decls[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        if self.decl is not None:
            yield self.decl
        if self.body is not None:
            yield self.body
        for child in (self.param_decls or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class Goto(Node):
    __slots__ = ('name', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('name', 'self_hash', 'recur_hash', )

class ID(Node):
    __slots__ = ('name', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('name', 'self_hash', 'recur_hash', )

class IdentifierType(Node):
    __slots__ = ('names', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, names, coord=None, self_hash = None, recur_hash = None):
        self.names = names
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('names', 'self_hash', 'recur_hash', )

class If(Node):
    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, cond, iftrue, iffalse, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.iftrue is not None: nodelist.append(("iftrue", self.iftrue))
        if self.iffalse is not None: nodelist.append(("iffalse", self.iffalse))
        return tuple(nodelist)

    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.iftrue is not None:
            yield self.iftrue
        if self.iffalse is not None:
            yield self.iffalse

    attr_names = ('self_hash', 'recur_hash', )

class InitList(Node):
    __slots__ = ('exprs', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, exprs, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.exprs = exprs
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.exprs or []):
            nodelist.append(("exprs[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.exprs or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class Label(Node):
    __slots__ = ('name', 'stmt', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, stmt, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.stmt = stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.stmt is not None: nodelist.append(("stmt", self.stmt))
        return tuple(nodelist)

    def __iter__(self):
        if self.stmt is not None:
            yield self.stmt

    attr_names = ('name', 'self_hash', 'recur_hash', )

class NamedInitializer(Node):
    __slots__ = ('name', 'expr', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, expr, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.name = name
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        for i, child in enumerate(self.name or []):
            nodelist.append(("name[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        if self.expr is not None:
            yield self.expr
        for child in (self.name or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class ParamList(Node):
    __slots__ = ('params', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, params, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.params = params
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.params or []):
            nodelist.append(("params[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.params or []):
            yield child

    attr_names = ('self_hash', 'recur_hash', )

class PtrDecl(Node):
    __slots__ = ('quals', 'type', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, quals, type, coord=None, self_hash = None, recur_hash = None):
        self.quals = quals
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type

    attr_names = ('quals', 'self_hash', 'recur_hash', )

class Return(Node):
    __slots__ = ('expr', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, expr, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    def __iter__(self):
        if self.expr is not None:
            yield self.expr

    attr_names = ('self_hash', 'recur_hash', )

class Struct(Node):
    __slots__ = ('name', 'decls', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, decls, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.decls = decls
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.decls or []):
            nodelist.append(("decls[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.decls or []):
            yield child

    attr_names = ('name', 'self_hash', 'recur_hash', )

class StructRef(Node):
    __slots__ = ('name', 'type', 'field', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, type, field, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.type = type
        self.field = field
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.field is not None: nodelist.append(("field", self.field))
        return tuple(nodelist)

    def __iter__(self):
        if self.name is not None:
            yield self.name
        if self.field is not None:
            yield self.field

    attr_names = ('type', 'self_hash', 'recur_hash', )

class Switch(Node):
    __slots__ = ('cond', 'stmt', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, cond, stmt, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.stmt is not None: nodelist.append(("stmt", self.stmt))
        return tuple(nodelist)

    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.stmt is not None:
            yield self.stmt

    attr_names = ('self_hash', 'recur_hash', )

class TernaryOp(Node):
    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, cond, iftrue, iffalse, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.iftrue is not None: nodelist.append(("iftrue", self.iftrue))
        if self.iffalse is not None: nodelist.append(("iffalse", self.iffalse))
        return tuple(nodelist)

    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.iftrue is not None:
            yield self.iftrue
        if self.iffalse is not None:
            yield self.iffalse

    attr_names = ('self_hash', 'recur_hash', )

class TypeDecl(Node):
    __slots__ = ('declname', 'quals', 'type', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, declname, quals, type, coord=None, self_hash = None, recur_hash = None):
        self.declname = declname
        self.quals = quals
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type

    attr_names = ('declname', 'quals', 'self_hash', 'recur_hash', )

class Typedef(Node):
    __slots__ = ('name', 'quals', 'storage', 'type', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, quals, storage, type, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.quals = quals
        self.storage = storage
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type

    attr_names = ('name', 'quals', 'storage', 'self_hash', 'recur_hash', )

class Typename(Node):
    __slots__ = ('name', 'quals', 'type', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, quals, type, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.quals = quals
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type

    attr_names = ('name', 'quals', 'self_hash', 'recur_hash', )

class UnaryOp(Node):
    __slots__ = ('op', 'expr', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, op, expr, coord=None, self_hash = None, recur_hash = None):
        self.op = op
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    def __iter__(self):
        if self.expr is not None:
            yield self.expr

    attr_names = ('op', 'self_hash', 'recur_hash', )

class Union(Node):
    __slots__ = ('name', 'decls', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, name, decls, coord=None, self_hash = None, recur_hash = None):
        self.name = name
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.decls = decls
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.decls or []):
            nodelist.append(("decls[%d]" % i, child))
        return tuple(nodelist)

    def __iter__(self):
        for child in (self.decls or []):
            yield child

    attr_names = ('name', 'self_hash', 'recur_hash', )

class While(Node):
    __slots__ = ('cond', 'stmt', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, cond, stmt, coord=None, self_hash = None, recur_hash = None):
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.stmt is not None: nodelist.append(("stmt", self.stmt))
        return tuple(nodelist)

    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.stmt is not None:
            yield self.stmt

    attr_names = ('self_hash', 'recur_hash', )

class Pragma(Node):
    __slots__ = ('string', 'coord', 'self_hash', 'recur_hash', '__weakref__')
    def __init__(self, string, coord=None, self_hash = None, recur_hash = None):
        self.string = string
        self.self_hash = self_hash
        self.recur_hash = recur_hash
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('string', 'self_hash', 'recur_hash', )

