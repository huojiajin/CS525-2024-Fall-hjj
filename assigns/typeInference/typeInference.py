ST0ref = 1


class tvar:
    count = 0

    def __init__(self):
        self.styp = None
        self.stamp = self.count
        self.count += 1


class styp:
    ctag = -1


class ST_ref(styp):
    def __init__(self, tvar1):
        self.tvar = tvar1  # TODO What to do?
        self.ctag = ST0ref


def styp_norm(t0):
    if t0.ctag == ST0ref:
        t1 = t0.tavr
        if t1 is None:
            return t0
        else:
            return styp_norm(t1)
    else:
        return t0
