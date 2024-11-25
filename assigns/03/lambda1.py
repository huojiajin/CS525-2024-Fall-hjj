############################################################
#
# Assign03 for CS525, Fall, 2024
# It is due the 2nd of October, 2024
# Note that the due time is always 11:59pm of
# the due date unless specified otherwise.
#
############################################################
#
# HX: This part is worth 50 points
#
# Please extend the closure based evaluator
# in the following file
# ./../../lambdas/lambda1/XATS/lambda1.dats
# More specifically, please also handle the additional
# language constructs in the following datatype definition
# Also, please introduce three operators: nilq, pfst, psnd:
#
# nilq: testing if a value is DVnil0()
# pfst: takes DVcons(dv1, dv2) and returns dv1
# psnd: takes DVcons(dv1, dv2) and returns dv2
#
############################################################
#
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
# |TMfix of (tvar, tvar, term)
#
# |TMnil0 of () // nil(): empty tuple
# |TMcons of (term, term) // cons(t1, t2): tuple of length 2 (pair)
# |TMlet0 of (tvar, term, term) // TMlet0(x, t1, t2): let x = t1 in t2 end
#

TM0int = 0
TM0btf = 1

TM0var = 2
TM0lam = 3
TM0app = 4
#

TM0opr = 5
TM0if0 = 6
TM0fix = 7

TM0nil0 = 9
TM0cons = 10
TM0let0 = 11


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
        return f"TMvar({self.arg1})"


# end-of-class(term_var(term))
#
class term_lam(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = TM0lam

    def __str__(self):
        return f"TMlam({self.arg1}, {self.arg2})"


# end-of-class(term_lam(term))
#
class term_app(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = TM0app

    def __str__(self):
        return f"TMapp({self.arg1}, {self.arg2})"


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
class term_fix(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = TM0fix

    def __str__(self):
        return f"TMfix({self.arg1}, {self.arg2}, {self.arg3})"


# end-of-class(term_fix(term))

# |TMnil0 of () // nil(): empty tuple
# |TMcons of (term, term) // cons(t1, t2): tuple of length 2 (pair)
# |TMlet0 of (tvar, term, term) // TMlet0(x, t1, t2): let x = t1 in t2 end
#

class term_nil0(term):
    def __init__(self):
        self.ctag = TM0nil0

    def __str__(self):
        return "TMnil0()"


class term_cons(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = TM0cons

    def __str__(self):
        return f"TMcons({self.arg1}, {self.arg2})"


class term_let0(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = TM0let0

    def __str__(self):
        return f"TMlet0({self.arg1}, {self.arg2}, {self.arg3})"


# end-of-class(term_nil0(term))

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


def TM1ifx(tm1: term, tm2: term, tm3: term) -> term:
    return term_fix(tm1, tm2, tm3)


def TM1nil0() -> term:
    return term_nil0()


def TM1cons(tm1: term, tm2: term) -> term:
    return term_cons(tm1, tm2)


def TM1let0(var: str, tm1: term, tm2: term) -> term:
    return term_let0(var, tm1, tm2)


# datatype dval =
#
# | DVint of sint
# | DVbtf of bool
# | DVlam of (term, denv)
# | DVfix of (term, denv)
# | DVnil0 of () // for TMnil0()
# | DVcons of (dval, dval) // for TMcons0()
#
DV0int = 0
DV0btf = 1
DV0lam = 2
DV0fix = 3
DV0nil0 = 4
DV0cons = 5
DV0let0 = 6


############################################################
class dval:
    ctag = -1


# end-of-class(dval)
############################################################
class dval_int:
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = DV0int

    def __str__(self):
        return f"DVint({self.arg1})"


# end-of-class(dval_int)
############################################################
class dval_btf:
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = DV0btf

    def __str__(self):
        return f"DVbtf({self.arg1})"


# end-of-class(dval_btf)
############################################################
class dval_lam:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = DV0lam

    def __str__(self):
        return f"DVlam({self.arg1}, {self.arg2})"


# end-of-class(dval_lam)
############################################################
class dval_fix:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = DV0fix

    def __str__(self):
        return f"DVfix({self.arg1}, {self.arg2})"


# end-of-class(dval_fix)
############################################################
class dval_nil0:
    def __init__(self):
        self.ctag = DV0nil0

    def __str__(self):
        return f"DVnil0()"


# end-of-class(dval_nil0)
############################################################
class dval_cons:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = DV0cons

    def __str__(self):
        return f"DVcons({self.arg1}, {self.arg2})"


# end-of-class(dval_cons)
############################################################
class dval_let0:
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = DV0let0

    def __str__(self):
        return f"DVlet0({self.arg1}, {self.arg2}, {self.arg3})"


# end-of-class(dval_let0)
############################################################

# # nilq: testing if a value is DVnil0()
# def nilq(value):
#     return value.ctag == DV0nil0
#
#
# # pfst: takes DVcons(dv1, dv2) and returns dv1
# def pfst(value):
#     if value.ctag == DV0cons:
#         return value.arg1
#     raise ValueError("pfst expects a DVcons value.")
#
#
# # psnd: takes DVcons(dv1, dv2) and returns dv2
# def psnd(value):
#     if value.ctag == DV0cons:
#         return value.arg2
#     raise ValueError("psnd expects a DVcons value.")


def denv_search2opt(x00, env):
    # print("denv_search2opt: env =", env)
    for xdv in reversed(env):
        if x00 == xdv[0]:
            return xdv[1]
    return None  # HX: x00 is not found


def term_evaluate(tm0):
    def auxeval(tm0, env):
        if tm0.ctag == TM0int:
            return dval_int(tm0.arg1)
        if tm0.ctag == TM0btf:
            return dval_btf(tm0.arg1)
        if tm0.ctag == TM0var:
            return denv_search2opt(tm0.arg1, env)
        if tm0.ctag == TM0lam:
            return dval_lam(tm0, env.copy())
        if tm0.ctag == TM0fix:
            return dval_fix(tm0, env.copy())
        if tm0.ctag == TM0app:
            dv1 = auxeval(tm0.arg1, env)
            dv2 = auxeval(tm0.arg2, env)
            if dv1.ctag == DV0lam:
                tma = dv1.arg1
                x01 = tma.arg1
                tmb = tma.arg2
                env = dv1.arg2
                return auxeval(tmb, env + [(x01, dv2)])
            if dv1.ctag == DV0fix:
                tma = dv1.arg1
                f00 = tma.arg1
                x01 = tma.arg2
                tmb = tma.arg3
                env = dv1.arg2
                return auxeval(tmb, env + [(f00, dv1), (x01, dv2)])
            raise TypeError(tm0)  # HX: should be deadcode!
        if tm0.ctag == TM0opr:
            opr = tm0.arg1
            tms = tm0.arg2
            if opr == "<":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_btf(dv0.arg1 < dv1.arg1)
            if opr == ">":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_btf(dv0.arg1 > dv1.arg1)
            if opr == "=":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_btf(dv0.arg1 == dv1.arg1)
            if opr == "<=":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_btf(dv0.arg1 <= dv1.arg1)
            if opr == ">=":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_btf(dv0.arg1 >= dv1.arg1)
            if opr == "!=":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_btf(dv0.arg1 != dv1.arg1)
            if opr == "+":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_int(dv0.arg1 + dv1.arg1)
            if opr == "-":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_int(dv0.arg1 - dv1.arg1)
            if opr == "*":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_int(dv0.arg1 * dv1.arg1)
            if opr == "/":
                dv0 = auxeval(tms[0], env)
                dv1 = auxeval(tms[1], env)
                return dval_int(dv0.arg1 // dv1.arg1)
            # nilq, pfst, psnd:
            if opr == "nilq":
                dv0 = auxeval(tms[0], env)
                return dval_btf(dv0.arg1 == DV0nil0)
            if opr == "pfst":
                dv0 = auxeval(tms[0], env)
                return dv0
            if opr == "psnd":
                dv1 = auxeval(tms[1], env)
                return dv1
            raise TypeError(tm0)  # HX: unrecognized operator
        if tm0.ctag == TM0if0:
            dv1 = auxeval(tm0.arg1, env)
            return auxeval(tm0.arg2, env) \
                if dv1.arg1 else auxeval(tm0.arg3, env)
        # if tm0.ctag == TM0fix:


# TM0nil0 = 9
# TM0cons = 10
# TM0let0 = 11
        raise TypeError(tm0)  # HX: should be deadcode!

    return auxeval(tm0, [])

############################################################
# end of [HWXI/CS525-2024-Fall/assigns/03/lambda1.py]
############################################################
