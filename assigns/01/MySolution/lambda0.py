############################################################
#
# Assign01 for CS525, Fall, 2024
# It is due the 18th of September, 2024
# Note that the due time is always 11:59pm of
# the due date unless specified otherwise.
#
############################################################
# HX-2024-09-10:
# A substitution-based reference
# implementation of lambad-calculus
############################################################
# datatype term =
# | TMvar of strn
# | TMlam of (strn, term)
# | TMapp of (term, term)
# | TMint of (term)
# | TMopr of (strn, term)
############################################################
#
import sys

TM0var = 0
TM0lam = 1
TM0app = 2
TM0int = 3
TM0opr = 4

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

#
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


#
############################################################
#
def I_():
    x = TM1var("x")
    return TM1lam("x", x)


def K_():
    x = TM1var("x")
    return TM1lam("x", TM1lam("y", x))


def S_():
    x = TM1var("x")
    y = TM1var("y")
    z = TM1var("z")
    return TM1lam("x", TM1lam("y", TM1lam("z", TM1app(TM1app(x, z), TM1app(y, z)))))


#
_ = print("I =", I_())
_ = print("K =", K_())
_ = print("S =", S_())


#
############################################################
#
# HX: [sub] should be closed!
#
def term_subst(tm0, x00, sub):
    def subst(tm0):
        return term_subst(tm0, x00, sub)

    if (tm0.ctag == TM0var):
        x01 = tm0.arg1
        return sub if (x00 == x01) else tm0
    if (tm0.ctag == TM0lam):
        x01 = tm0.arg1
        return tm0 if (x00 == x01) else TM1lam(x01, subst(tm0.arg2))
    if (tm0.ctag == TM0app):
        return TM1app(subst(tm0.arg1), subst(tm0.arg2))
    if tm0.ctag == TM0int:
        return tm0
    if tm0.ctag == TM0opr:
        return TM1opr(tm0.arg1, list(map(subst, tm0.arg2)))
    raise TypeError(tm0)  # HX: should be deadcode!


############################################################

def term_beta2red(tm1, tm2):
    assert tm1.ctag == TM0lam
    return term_subst(tm1.arg2, tm1.arg1, tm2)


def term_evaluate(tm0):
    # print("term_evaluate: tm0 = ", tm0)
    if (tm0.ctag == TM0var):
        return tm0
    if (tm0.ctag == TM0lam):
        return tm0
    if (tm0.ctag == TM0app):
        tm1 = tm0.arg1
        tm2 = tm0.arg2
        tm1 = term_evaluate(tm1)
        if (tm1.ctag == TM0lam):
            return term_evaluate(term_beta2red(tm1, tm2))
        else:
            return TM1app(tm1, term_evaluate(tm2))
    if tm0.ctag == TM0int:
        return tm0
    if tm0.ctag == TM0opr:
        # Get the operator and operands first
        op = tm0.arg1
        operands = [term_evaluate(arg) for arg in tm0.arg2]
        # Handle basic operators
        if op == '+':
            return TM1int(sum(operand.arg1 for operand in operands if operand.ctag == TM0int))
        if op == '-':
            # Check the size of operands
            if len(operands) < 2:
                raise ValueError("Subtraction requires at least two operands!")
            result = sys.maxsize
            for operand in operands:
                if operand.ctag == TM0int:
                    if result == sys.maxsize:
                        result = operand.arg1
                    else:
                        result -= int(operand.arg1)
            if (result == sys.maxsize):
                raise ValueError("There are no integer operands!")
            else:
                return TM1int(result)
        if op == '*':
            # Check the size of operands
            if len(operands) < 2:
                raise ValueError("Subtraction requires at least two operands!")
            result = sys.maxsize
            for operand in operands:
                if operand.ctag == TM0int:
                    if result == sys.maxsize:
                        result = operand.arg1
                    else:
                        result *= int(operand.arg1)
            if (result == sys.maxsize):
                raise ValueError("There are no integer operands!")
            else:
                return TM1int(result)
        if op == '/':
            # Check the size of operands
            if len(operands) < 2:
                raise ValueError("Subtraction requires at least two operands!")
            result = sys.maxsize
            for operand in operands:
                if operand.ctag == TM0int:
                    if result == sys.maxsize:
                        result = operand.arg1
                    else:
                        result //= int(operand.arg1)
            if (result == sys.maxsize):
                raise ValueError("There are no integer operands!")
            else:
                return TM1int(result)
        else:
            raise ValueError(f"Unknown operator: {op}")

    raise TypeError(tm0)  # HX: should be deadcode!


############################################################
#
def SKKx():
    S = S_()
    K = K_()
    x = TM1var("x")
    return TM1app(TM1app(TM1app(S, K), K), x)


#
print("evaluate(SKKx) =", term_evaluate(SKKx()))


#
############################################################
############################################################
#
# HX-2024-09-12:
# Points: 10
# Please first extend lambda0 with TMint and TMopr
# For instance, some details can be found in the code
# stored in the directory ./../../lambdas/lambda0/XATS
#
############################################################

def term_free2vars(tm0):
    """
    Points: 10
    This function takes a term [tm0] and returns the set of
    free variables in [tm0]. The set returned should be the
    built-in set in Python
    """
    if tm0.ctag == TM0var:  # If tm0 is a single variable, it's a free variable
        return {tm0.arg1}
    elif tm0.ctag == TM0lam:  # If tm0 is a lambda, the variable of arg2 exclude the variable of arg1 are free variables
        return term_free2vars(tm0.arg2) - {tm0.arg1}
    elif tm0.ctag == TM0app:  # If tm0 is an application, take the union of free variables in both terms
        return term_free2vars(tm0.arg1) | term_free2vars(tm0.arg2)
    elif tm0.ctag == TM0int:  # Integers don't contain variables, so they have no free variables
        return set()
    elif tm0.ctag == TM0opr:  # Integers and operators don't contain variables, so they have no free variables
        return set()
    else:
        raise TypeError("Unknown term type in term_free2vars")


############################################################

def term_gsubst(tm0, x00, sub):
    """
    Points: 20
    This function implements the (general) substitution
    function on terms that should correctly handle an open
    [sub] (that is, [sub] containing free variables)
    """

    def gsubst(tm0):
        return term_gsubst(tm0, x00, sub)

    if tm0.ctag == TM0var:  # If tm0 is the variable we want to replace, return sub
        x01 = tm0.arg1
        return sub if (x00 == x01) else tm0
    if tm0.ctag == TM0lam:
        x01 = tm0.arg1
        if x00 == x01:  # If x01 matches x00, no substitution is needed
            return tm0
        else:
            # Check if `sub` contains the lambda variable `x01` as a free variable
            free_vars_in_sub = term_free2vars(sub)
            if x01 in free_vars_in_sub:
                # Rename `x01` to a new variable
                new_var = x01 + "_rn"
                rn_func = term_gsubst(tm0.arg2, x01, TM1var(new_var))
                return TM1lam(new_var, gsubst(rn_func))
            else:
                return TM1lam(x01, gsubst(tm0.arg2))
    if tm0.ctag == TM0app:
        return TM1app(gsubst(tm0.arg1), gsubst(tm0.arg2))
    if tm0.ctag == TM0int:
        return tm0
    if tm0.ctag == TM0opr:
        return TM1opr(tm0.arg1, list(map(gsubst, tm0.arg2)))
    raise TypeError(tm0)  # HX: should be deadcode!

############################################################
# end of [HWXI/CS525-2024-Fall/assigns/01/lambda0.py]
############################################################

