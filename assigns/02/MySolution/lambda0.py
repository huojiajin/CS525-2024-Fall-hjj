############################################################
#
# Assign02 for CS525, Fall, 2024
# It is due the 25th of September, 2024
# Note that the due time is always 11:59pm of
# the due date unless specified otherwise.
#
############################################################
# HX-2024-09-19:
# Compiling an extended lambda-calculus to
# Church's pure lambda-calculus
############################################################
# //
# datatype term =
# //
# |TMint of sint
# |TMbtf of bool
# //
# |TMvar of tvar
# |TMlam of (tvar, term)
# |TMapp of (term, term)
# //
# |TMopr of (topr, list(term))
# |TMif0 of (term, term, term)
# //
# #typedef termlst = list(term)
# //
############################################################
#
import sys

TM0var = 0
TM0lam = 1
TM0app = 2
#
TM0int = 3
TM0btf = 4
TM0opr = 5
TM0if0 = 6


#
############################################################
#
class term:
    ctag = -1


# end-of-class(term)
#
class term_var(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = TM0var

    def __str__(self):
        return ("TMvar(" + self.arg1 + ")")


# end-of-class(term_var(term))
#
class term_lam(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = TM0lam

    def __str__(self):
        return ("TMlam(" + self.arg1 + "," + str(self.arg2) + ")")


# end-of-class(term_lam(term))
#
class term_app(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = TM0app

    def __str__(self):
        return ("TMapp(" + str(self.arg1) + "," + str(self.arg2) + ")")


# end-of-class(term_app(term))

class term_int(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = TM0int

    def __str__(self):
        return f"TMint({str(self.arg1)})"


# end-of-class(term_int(term))

#
class term_opr(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1  # opr
        self.arg2 = arg2  # list
        self.ctag = TM0opr

    def __str__(self):
        return f"TMopr({str(self.arg1)}, {str(self.arg2)})"


# end-of-class(term_opr(term))

#
class term_btf(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = TM0btf

    def __str__(self):
        return f"TMbtf({str(self.arg1)})"


# end-of-class(term_btf(term))

#
class term_if0(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = TM0if0

    def __str__(self):
        return f"TMif0({self.arg1}, {self.arg2}, {self.arg3})"


# end-of-class(term_if0(term))

#
############################################################
#
def TM1var(x00):
    return term_var(x00)


def TM1lam(x00, tm1):
    return term_lam(x00, tm1)


def TM1app(tm1, tm2):
    return term_app(tm1, tm2)


def TM1int(i00: int) -> term:
    return term_int(i00)


def TM1opr(opr, tms: list[term]) -> term:
    return term_opr(opr, tms)


def TM1btf(b00: bool) -> term:
    return term_btf(b00)


def TM1if0(tm1: term, tm2: term, tm3: term) -> term:
    return term_if0(tm1, tm2, tm3)


#
############################################################
############################################################
#
# HX-2024-09-19:
# Points: 60
# This assignment asks you to translate
# a given lambda-term in the above extended lambda-calculus
# into Church's pure lambda-calculus.
# More specifically, given a term tm0 (which may contain
# extended constructs like TMint, TMbtf, TMopr, and TMif0),
# the following function assign02_transpile should return a
# term tm1 that contains only constructs TMvar, TMlam, and
# TMapp. In addition, if tm0 evaluates to an integer n, then
# tm1 should evaluate to a lambda-term beta-equivalent to the
# Church numeral representing n.
#
def assign02_transpile(tm0):
    if tm0.ctag == TM0var:
        return TM1var(tm0.arg1)
    if tm0.ctag == TM0lam:
        return TM1lam(tm0.arg1, assign02_transpile(tm0.arg2))
    if tm0.ctag == TM0app:
        return TM1app(assign02_transpile(tm0.arg1), assign02_transpile(tm0.arg2))
    if tm0.ctag == TM0if0:
        condition = assign02_transpile(tm0.arg1)
        then_term = assign02_transpile(tm0.arg2)
        else_term = assign02_transpile(tm0.arg3)
        return TM1app(TM1app(condition, then_term), else_term)
    if tm0.ctag == TM0int:
        # λf.λx. f^n(x)
        f = TM1var("f")
        x = TM1var("x")
        body = x
        for _ in range(tm0.arg1):
            body = TM1app(f, body)
        return TM1lam("f", TM1lam("x", body))
    if tm0.ctag == TM0btf:
        # True: λx.λy.x    False: λx.λy.y
        x = TM1var("x")
        y = TM1var("y")
        return TM1lam("x", TM1lam("y", x if tm0.arg1 else y))
    if tm0.ctag == TM0opr:
        op = tm0.arg1
        args = [assign02_transpile(arg) for arg in tm0.arg2]    # Recurison to convert the variables
        if op == "+":
            # λm.λn.λf.λx. m f (n f x)
            m, n = args
            f = TM1var("f")
            x = TM1var("x")
            return TM1lam("m", TM1lam("n", TM1lam("f", TM1lam("x",
                                                              TM1app(TM1app(m, f), TM1app(TM1app(n, f), x))))))
        if op == "*":
            # λm.λn.λf. m (n f)
            m, n = args
            f = TM1var("f")
            return TM1lam("m", TM1lam("n", TM1lam("f", TM1app(m, TM1app(n, f)))))
        if op == "<":
            # λm.λn. m (λx. false) n true
            m, n = args
            false_expr = TM1lam("x", TM1lam("y", TM1var("y")))
            true_expr = TM1lam("x", TM1lam("y", TM1var("x")))
            return TM1lam("m", TM1lam("n", TM1app(TM1app(m, TM1lam("x", false_expr)), TM1app(n, true_expr))))
        #   TODO other operations? How to implement them?
        #   use fixpoint achieve other operations
    else:
        raise TypeError("Unsupported term type")
############################################################


# def term_subst(tm0, x00, sub):
#     def subst(tm0):
#         return term_subst(tm0, x00, sub)
#
#     if tm0.ctag == TM0var:
#         x01 = tm0.arg1
#         return sub if (x00 == x01) else tm0
#     if tm0.ctag == TM0lam:
#         x01 = tm0.arg1
#         return tm0 if (x00 == x01) else TM1lam(x01, subst(tm0.arg2))
#     if tm0.ctag == TM0app:
#         return TM1app(subst(tm0.arg1), subst(tm0.arg2))
#     if tm0.ctag == TM0int:
#         return tm0
#     if tm0.ctag == TM0opr:
#         return TM1opr(tm0.arg1, list(map(subst, tm0.arg2)))
#     if tm0.ctag == TM0btf:
#         return tm0
#     if tm0.ctag == TM0if0:
#         return TM1if0(subst(tm0.arg1), subst(tm0.arg2), subst(tm0.arg3))
#     raise TypeError(tm0)  # HX: should be deadcode!
#
#
# ############################################################
#
# def term_beta2red(tm1, tm2):
#     assert tm1.ctag == TM0lam
#     return term_subst(tm1.arg2, tm1.arg1, tm2)
#
#
# def term_evaluate(tm0):
#     # print("term_evaluate: tm0 = ", tm0)
#     if (tm0.ctag == TM0var):
#         return tm0
#     if (tm0.ctag == TM0lam):
#         return tm0
#     if (tm0.ctag == TM0app):
#         tm1 = tm0.arg1
#         tm2 = tm0.arg2
#         tm1 = term_evaluate(tm1)
#         if (tm1.ctag == TM0lam):
#             return term_evaluate(term_beta2red(tm1, tm2))
#         else:
#             return TM1app(tm1, term_evaluate(tm2))
#     if tm0.ctag == TM0int:
#         return tm0
#     if tm0.ctag == TM0opr:
#         # Get the operator and operands first
#         op = tm0.arg1
#         operands = [term_evaluate(arg) for arg in tm0.arg2]
#         # Handle basic operators
#         if op == '+':
#             return TM1int(sum(operand.arg1 for operand in operands if operand.ctag == TM0int))
#         if op == '-':
#             # Check the size of operands
#             if len(operands) < 2:
#                 raise ValueError("Calculation requires at least two operands!")
#             result = sys.maxsize
#             for operand in operands:
#                 if operand.ctag == TM0int:
#                     if result == sys.maxsize:
#                         result = operand.arg1
#                     else:
#                         result -= int(operand.arg1)
#             if (result == sys.maxsize):
#                 raise ValueError("There are no integer operands!")
#             else:
#                 return TM1int(result)
#         if op == '*':
#             # Check the size of operands
#             if len(operands) < 2:
#                 raise ValueError("Calculation requires at least two operands!")
#             result = sys.maxsize
#             for operand in operands:
#                 if operand.ctag == TM0int:
#                     if result == sys.maxsize:
#                         result = operand.arg1
#                     else:
#                         result *= int(operand.arg1)
#             if (result == sys.maxsize):
#                 raise ValueError("There are no integer operands!")
#             else:
#                 return TM1int(result)
#         if op == '/':
#             # Check the size of operands
#             if len(operands) < 2:
#                 raise ValueError("Calculation requires at least two operands!")
#             result = sys.maxsize
#             for operand in operands:
#                 if operand.ctag == TM0int:
#                     if result == sys.maxsize:
#                         result = operand.arg1
#                     else:
#                         result //= int(operand.arg1)
#             if (result == sys.maxsize):
#                 raise ValueError("There are no integer operands!")
#             else:
#                 return TM1int(result)
#         if op == '<':
#             if len(operands) != 2:
#                 raise ValueError("comparison requires at least two operands!")
#             return TM1btf(operands[0].arg1 < operands[1].arg1)
#         if op == '>':
#             if len(operands) != 2:
#                 raise ValueError("comparison requires at least two operands!")
#             return TM1btf(operands[0].arg1 > operands[1].arg1)
#         if op == '<=':
#             if len(operands) != 2:
#                 raise ValueError("comparison requires at least two operands!")
#             return TM1btf(operands[0].arg1 <= operands[1].arg1)
#         if op == '>=':
#             if len(operands) != 2:
#                 raise ValueError("comparison requires at least two operands!")
#             return TM1btf(operands[0].arg1 >= operands[1].arg1)
#         if op == '==':
#             if len(operands) != 2:
#                 raise ValueError("comparison requires at least two operands!")
#             return TM1btf(operands[0].arg1 == operands[1].arg1)
#         if op == '!=':
#             if len(operands) != 2:
#                 raise ValueError("comparison requires at least two operands!")
#             return TM1btf(operands[0].arg1 != operands[1].arg1)
#
#         else:
#             raise ValueError(f"Unknown operator: {op}")
#
#     if tm0.ctag == TM0btf:
#         return tm0
#     if tm0.ctag == TM0if0:
#         # Evaluate the condition
#         condition = term_evaluate(tm0.arg1)
#         if condition.ctag == TM0int and condition.arg1 == 0:
#             # Condition is zero, return the second term
#             return term_evaluate(tm0.arg2)
#         else:
#             # Condition is non-zero, return the third term
#             return term_evaluate(tm0.arg3)
#     raise TypeError(tm0)  # HX: should be deadcode!


############################################################
# end of [HWXI/CS525-2024-Fall/assigns/02/lambda0.py]
############################################################
