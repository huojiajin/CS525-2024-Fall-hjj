############################################################
############################################################
# HX-2024-10-12:
# Type-checking for some
# extended lambda-calculus
# This part is worth 60 points
# Please see assign04.py for another 40 points
# The total number of points for Assign04 is 60+40=100
# Please see lambdas/XATS/lambda2.dats
# for a mostly completed implementation of a type-checker 
############################################################
############################################################
# datatype styp =
# | STbas of (snam)
# | STtup of (styp, styp)
# | STfun of (styp, styp)
# | STnone of (   ) // none
# | STpfst of (styp) // nontup
# | STpsnd of (styp) // nontup
# | STfarg of (styp) // nonfun
# | STfres of (styp) // nonfun
############################################################
#
ST0bas = 0
ST0tup = 1
ST0fun = 2
#
ST0none = 3
#
ST0pfst = 4
ST0psnd = 5  # Some error?
ST0farg = 6
ST0fres = 7


#
############################################################

class styp:
    ctag = -1


# end-of-class(styp)

#
class ST_bas(styp):
    def __init__(self, name):
        self.name = name
        self.ctag = ST0bas

    def __str__(self):
        return f"STbas({self.name})"


# end-of-class(ST_bas(styp))

#
class ST_tup(styp):
    def __init__(self, *args):
        self.elements = args
        self.ctag = ST0tup

    def __str__(self):
        return f"STtup({', '.join(str(element) for element in self.elements)})"


# end-of-class(ST_tup(styp))

#
class ST_fun(styp):
    def __init__(self, arg_type, return_type):  # STfun(STtup(arg1, arg2), return_type) fit for multiple variables
        self.arg_type = arg_type  # STtup
        self.return_type = return_type
        self.ctag = ST0fun

    def __str__(self):
        return f"STfun({self.arg_type}, {self.return_type})"


# end-of-class(ST_fun(styp))

#
class ST_none(styp):
    def __init__(self):
        self.ctag = ST0none

    def __str__(self):
        return "STnone"


# end-of-class(ST_none(styp))

#
#  The error when program try to get the first element from the typ
class ST_pfst(styp):
    def __init__(self, typ):
        self.typ = typ
        self.ctag = ST0pfst

    def __str__(self):
        return f"STpfst({self.typ})"


# end-of-class(ST_pfst(styp))

#
#  The error when program try to get the second element from the typ
class ST_psnd(styp):
    def __init__(self, typ):
        self.typ = typ
        self.ctag = ST0psnd

    def __str__(self):
        return f"STpsnd({self.typ})"


# end-of-class(ST_psnd(styp))

#
#  The error when program try to extract the argument type from a non-function type
class ST_farg(styp):
    def __init__(self, typ):
        self.typ = typ
        self.ctag = ST0farg

    def __str__(self):
        return f"STfarg({self.typ})"


# end-of-class(ST_farg(styp))

#
#  The error when program try to extract the return type from a non-function type
class ST_fres(styp):
    def __init__(self, typ):
        self.typ = typ
        self.ctag = ST0fres

    def __str__(self):
        return f"STfres({self.typ})"


# end-of-class(ST_fres(styp))
############################################################

#   Checking if two term has same type
def styp_subeq(st1, st2):
    if st1.ctag != st2.ctag:
        return False
    if st1.ctag == ST0bas:
        return st1.name == st2.name
    elif st1.ctag == ST0tup:
        return styp_subeq(st1.left, st2.left) and styp_subeq(st1.right, st2.right)
    elif st1.ctag == ST0fun:
        return styp_subeq(st1.arg_type, st2.arg_type) and styp_subeq(st1.return_type, st2.return_type)
    elif st1.ctag == ST0none:
        return True
    elif st1.ctag in {ST0pfst, ST0psnd, ST0farg, ST0fres}:
        return styp_subeq(st1.typ, st2.typ)
    return False


############################################################

# datatype dexp =
# | DEvar of strn
# | DElam of (strn, dexp)
# | DEapp of (dexp, dexp)
# | DEint of (sint)
# | DEbtf of (bool)
# | DEopr of (strn, list(dexp))
# | DEif0 of (dexp, dexp, dexp)
# | DEfix of (strn, strn, dexp)
################################################
# | DEnil0 of ()//unit
# | DEcons of (dexp, dexp)//pair
# | DEpfst of (dexp) // 1st project
# | DEpsnd of (dexp) // 2nd project
################################################
# | DElam2 of (strn, styp, dexp)
# | DEfix2 of (strn, strn, styp, dexp, styp)
############################################################
# | DEcast of (dexp, styp) # for type casting
############################################################
# | DEanno of (dexp, styp) # for type annotation
############################################################
#
DE0cst = 0
#
DE0var = 1
DE0lam = 2
DE0app = 3
#
DE0int = 4
DE0btf = 5
#
DE0opr = 6
DE0fix = 7
DE0if0 = 8
#
DE0nil0 = 9
DE0cons = 10
DE0pfst = 11
DE0psnd = 12
#
DE0cast = 13  # for type casting
#
DE0anno = 14  # for type annotation


#
############################################################
class dexp:
    ctag = -1
    styp = None


# end-of-class(dexp)
############################################################
class dexp_cst(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = DE0cst

    def __str__(self):
        return ("DEcst(" + self.arg1 + ")")


# end-of-class(dexp_var(dexp))
############################################################
class dexp_var(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = DE0var

    def __str__(self):
        return ("DEvar(" + self.arg1 + ")")


# end-of-class(dexp_var(dexp))
############################################################
class dexp_lam(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = DE0lam

    def __str__(self):
        return ("DElam(" + self.arg1 + "," + str(self.arg2) + ")")


# end-of-class(dexp_lam(dexp))
############################################################
class dexp_app(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = DE0app

    def __str__(self):
        return ("DEapp(" + str(self.arg1) + "," + str(self.arg2) + ")")


# end-of-class(dexp_app(dexp))
############################################################
class dexp_int(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = DE0int

    def __str__(self):
        return ("DEint(" + str(self.arg1) + ")")


# end-of-class(dexp_int(dexp))
############################################################
class dexp_btf(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = DE0btf

    def __str__(self):
        return ("DEbtf(" + str(self.arg1) + ")")


# end-of-class(dexp_btf(dexp))
############################################################
class dexp_opr(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = DE0opr

    def __str__(self):
        return ("DEopr(" + str(self.arg1) + "," + str(self.arg2) + ")")


# end-of-class(dexp_opr(dexp))
############################################################
class dexp_fix(dexp):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = DE0fix

    def __str__(self):
        return ("DEfix(" + str(self.arg1) + "," + str(self.arg2) + str(self.arg3) + ")")


# end-of-class(dexp_fix(dexp))
############################################################
class dexp_if0(dexp):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = DE0if0

    def __str__(self):
        return ("DEif0(" + str(self.arg1) + "," + str(self.arg2) + str(self.arg3) + ")")


# end-of-class(dexp_if0(dexp))
############################################################
class dexp_cast(dexp):
    def __init__(self, expr, styp):
        self.expr = expr
        self.styp = styp
        self.ctag = DE0cast

    def __str__(self):
        return f"DEcast({self.expr}, {self.styp})"


# end-of-class(dexp_cast(dexp))
############################################################
class dexp_anno(dexp):
    def __init__(self, expr, styp):
        self.expr = expr
        self.styp = styp
        self.ctag = DE0anno

    def __str__(self):
        return f"DEanno({self.expr}, {self.styp})"


# end-of-class(dexp_anno(dexp))
############################################################
#
def DE1cst(c00):
    return dexp_cst(c00)


#
def DE1var(x00):
    return dexp_var(x00)


def DE1lam(x00, de1):
    return dexp_lam(x00, de1)


def DE1app(de1, de2):
    return dexp_app(de1, de2)


#
def DE1int(i00):
    return dexp_int(i00)


def DE1btf(b00):
    return dexp_btf(b00)


#
def DE1opr(opr, des):
    return dexp_opr(opr, des)


#
def DE1fix(f00, x01, deb):
    return dexp_fix(f00, x01, deb)


#
def DE1if0(de1, de2, de3):
    return dexp_if0(de1, de2, de3)


#
############################################################
# Type checking and inferring types for expressions
def dexp_tpcheck(expr):
    env = {}
    return dexp_tpcheck_env(expr, env)


def dexp_tpcheck_env(expr, env):
    # TODO Problem! How to check the DE0cst, DE0fix, DE0if0, DE0cast, DE0anno

    # if expr.ctag == DE0cst:
    #     if expr.arg1 == "int":
    #         return dexp_anno(expr, ST_bas("int"))
    #     elif expr.arg1 == "bool":
    #         return dexp_anno(expr, ST_bas("bool"))
    #     else:
    #         raise TypeError("Unsupported constant type")

    if expr.ctag == DE0var:
        if expr.arg1 in env:
            return dexp_anno(expr, env[expr.arg1])
        else:
            return dexp_anno(expr, ST_none())

    elif expr.ctag == DE0lam:
        env[expr.arg1] = expr.arg2.styp
        body_checked = dexp_tpcheck_env(expr.arg3, env)
        return dexp_anno(expr, ST_fun(env[expr.arg1], body_checked.styp))

    elif expr.ctag == DE0app:
        func_checked = dexp_tpcheck_env(expr.arg1, env)
        arg_checked = dexp_tpcheck_env(expr.arg2, env)
        # Extract argument and return types, or provide error types if func_checked is not a function
        if func_checked.styp.ctag == ST0fun:
            expected_arg_type = func_checked.styp.arg_type
            return_type = func_checked.styp.return_type
        else:
            # Return an error type indicating function argument or result type error
            expected_arg_type = ST_farg(func_checked.styp)
            return_type = ST_fres(func_checked.styp)

        # Check if the argument type matches
        if styp_subeq(arg_checked.styp, expected_arg_type):
            return dexp_anno(dexp_app(func_checked, arg_checked), return_type)
        else:
            # Cast arg_checked to the expected type and annotate the result
            casted_arg = dexp_cast(arg_checked, expected_arg_type)
            return dexp_anno(dexp_app(func_checked, casted_arg), return_type)

    elif expr.ctag == DE0int:
        return dexp_anno(expr, ST_bas("int"))

    elif expr.ctag == DE0btf:
        return dexp_anno(expr, ST_bas("bool"))

    elif expr.ctag == DE0opr:
        op_type = None
        if expr.arg1 == '+':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("int"))
        elif expr.arg1 == '-':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("int"))
        elif expr.arg1 == '*':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("int"))
        elif expr.arg1 == '/':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("int"))
        elif expr.arg1 == '<':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("bool"))
        elif expr.arg1 == '>':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("bool"))
        elif expr.arg1 == '<=':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("bool"))
        elif expr.arg1 == '>=':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("bool"))
        elif expr.arg1 == '==':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("bool"))
        elif expr.arg1 == '!=':
            op_type = ST_fun((ST_bas("int"), ST_bas("int")), ST_bas("bool"))

        checked_args = [dexp_tpcheck_env(arg, env) for arg in expr.arg2]
        for i, arg in enumerate(checked_args):
            expected_type = op_type.arg_type[i] if i < len(op_type.arg_type) else None
            if expected_type is None or not styp_subeq(arg.styp, expected_type):
                return dexp_cast(arg, expected_type)

        return dexp_anno(expr, op_type.return_type)


    elif expr.ctag == DE0nil0:
        return dexp_anno(expr, ST_bas("unit"))

    elif expr.ctag == DE0cons:
        head_checked = dexp_tpcheck_env(expr.arg1, env)
        tail_checked = dexp_tpcheck_env(expr.arg2, env)
        return dexp_anno(expr, ST_tup(head_checked.styp, tail_checked.styp))

    elif expr.ctag == DE0pfst:
        pair_checked = dexp_tpcheck_env(expr.arg1, env)
        if pair_checked.styp.ctag == ST0tup:
            return dexp_anno(expr, pair_checked.styp.left)
        else:
            return dexp_cast(pair_checked, ST_pfst(pair_checked.styp))

    elif expr.ctag == DE0psnd:
        pair_checked = dexp_tpcheck_env(expr.arg1, env)
        if pair_checked.styp.ctag == ST0tup:
            return dexp_anno(expr, pair_checked.styp.right)
        else:
            return dexp_cast(pair_checked, ST_psnd(pair_checked.styp))
    else:
        raise TypeError("Unsupported expression type")

############################################################
# end of [HWXI/CS525-2024-Fall/assigns/04/lambda2.py]
############################################################
