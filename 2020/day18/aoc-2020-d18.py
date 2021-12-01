#!/usr/bin/env python3

# Advent of Code 2020, Day 18 (https://adventofcode.com/2020/day/18)
# Author: Ben Bornstein


class AST (object):
    """An Abstract Syntax Tree (AST) is comprised of one or more AST nodes.
    Each node may have an optional `op`erator and, `left` and `right`
    child nodes.

    Child nodes may be `None`.  If `op` and `right` are `None`, the AST
    node represents a single value, stored in the `left` node.
    """

    def __init__ (self, left, op=None, right=None):
        """Creates a new AST node."""
        self.left  = left
        self.op    = op
        self.right = right

    def evaluate (self):
        """Evaluates the AST and returns the resulting value."""
        result = None

        if self.op is None:
            result = self.left
        elif self.op == '+':
            result = self.left.evaluate() + self.right.evaluate()
        elif self.op == '*':
            result = self.left.evaluate() * self.right.evaluate()

        return result


class AbstractParser (object):
    """An AbstractParser parses the given `formula` string by calling the
    `expr()` method (must be implemented by subclasses).
    """

    def __init__ (self, formula):
        """Creates a new AbstractParser to parse `formula`."""
        self.t      = 0
        self.tokens = list( formula.replace(' ', '') )  # Lexer
        self.ast    = self.expr()

        if self.t != len(self.tokens):
            msg = f'Parse of "{formula}" stopped after {self.t} tokens.'
            raise SyntaxError(msg)

    @property
    def symbol (self):
        """The current symbol being parsed."""
        return self.tokens[ self.t ] if self.t < len(self.tokens) else None

    def expr (self):
        """The start of the grammer to parse.  Subclasses must implement."""
        msg = 'Subclasses must implement expr() to start their grammar.'
        raise NotImplementedError(msg)

    def match (self, token):
        """Matches `token` to the current `symbol` being parsed and advances to
        the next token.  If the current `symbol` does not match `token`,
        raises a `SyntaxError`.
        """
        if self.symbol == token:
            self.t += 1
        else:
            raise SyntaxError(f'Expected token: "{token}".')


class Parser1 (AbstractParser):
    """Parses infix integer addition and multiplication formula strings,
    with both operators having the same precedence, expressed formally
    in the following grammar:

        expr -> expr [ '+' | '*' ] term | term
        term -> '(' expr ')' | integer

    by using recursive descent parsing.  To avoid infinite recursion,
    the production rules above are transformed to eliminate
    left-recursion:

        expr  -> term expr1
        expr1 -> [ '+' | '*' ] term expr1 | (empty)
        term  -> '(' expr ')' | integer
    """

    def expr (self):
        """Rule: expr -> term expr1"""
        left = self.term()
        return self.expr1(left)

    def expr1 (self, left):
        """Rule: expr1 -> [ '+' | '*' ] term expr1 | (empty)"""
        node = left
        op   = self.symbol

        if op == '+' or op == '*':
            self.match(op)
            term = self.term()
            node = self.expr1( AST(left, op, term) )

        return node

    def term (self):
        """Rule: term -> '(' expr ')' | integer"""
        node = None

        if self.symbol == '(':
            self.match('(')
            node = self.expr()
            self.match(')')
        else:
            node = AST( int(self.symbol) )
            self.match(self.symbol)

        return node


class Parser2 (AbstractParser):
    """Parses infix integer addition and multiplication formula strings,
    with addition having higher precedence than multiplication, expressed
    formally in the following grammar:

        expr   -> expr   '*' factor | factor
        factor -> factor '+' term   | term
        term   -> '(' expr ')' | integer

    by using recursive descent parsing.  To avoid infinite recursion,
    the production rules above are transformed to eliminate
    left-recursion:

        expr    -> factor expr1
        expr1   -> '*' factor expr1 | (empty)
        factor  -> term factor1
        factor1 -> '+' term factor1 | (empty)
        term    -> '(' expr ')' | integer
    """

    def expr (self):
        """Rule: expr -> factor expr1"""
        left = self.factor()
        return self.expr1(left)

    def expr1 (self, left):
        """Rule: expr1 -> '*' factor expr1 | (empty)"""
        node = left

        if self.symbol == '*':
            self.match('*')
            factor = self.factor()
            node   = self.expr1( AST(left, '*', factor) )

        return node

    def factor (self):
        """Rule: factor -> term factor1"""
        left = self.term()
        return self.factor1(left)

    def factor1 (self, left):
        """Rule: factor1  -> '+' term factor1 | (empty)"""
        node = left

        if self.symbol == '+':
            self.match('+')
            term = self.term()
            node = self.factor1( AST(left, '+', term) )

        return node

    def term (self):
        """Rule: term -> '(' expr ')' | integer"""
        node = None

        if self.symbol == '(':
            self.match('(')
            node = self.expr()
            self.match(')')
        else:
            node = AST( int(self.symbol) )
            self.match(self.symbol)

        return node


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


eval1       = lambda formula: Parser1(formula).ast.evaluate()
eval2       = lambda formula: Parser2(formula).ast.evaluate()
filename    = 'aoc-2020-d18.txt'
expressions = list( lines(filename, lambda s: s.strip()) )


# Part 1
#
# Before you can help with the homework, you need to understand it
# yourself. Evaluate the expression on each line of the homework.
#
# Q: What is the sum of the resulting values?
# A: Part 1: Sum of homework expressions: 36382392389406

assert eval1('2 * 3 + (4 * 5)') == 26
assert eval1('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert eval1('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert eval1('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

values = [ eval1(expr) for expr in expressions ]
print(f'Part 1: Sum of homework expressions: {sum(values)}')


# Part 2
#
# Q: What do you get if you add up the results of evaluating the homework
# problems using these new rules?
# A: Part 2: Sum of homework expressions: 381107029777968

assert eval2('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert eval2('2 * 3 + (4 * 5)') == 46
assert eval2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
assert eval2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
assert eval2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340

values = [ eval2(expr) for expr in expressions ]
print(f'Part 2: Sum of homework expressions: {sum(values)}')
