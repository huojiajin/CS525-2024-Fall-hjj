############################################################
#
# Assign03 for CS525, Fall, 2024
# It is due the 2nd of October, 2024
# Note that the due time is always 11:59pm of
# the due date unless specified otherwise.
#
############################################################
############################################################

def isqrt_in_lambda():
    """
    HX: 10 points
    This one is what we often call "eat-your-own-dog-food"
    Please implement an integer version of the sqare root
    funtion. For instance,
    isqrt(0) = 0, isqrt(2) = 1, isqrt(10) = 3, ...
    In general, given n >= 0, isqrt(n) returns the largest
    integer x satisfying x * x <= n. Your implementation
    is expected to be effcient; your code may be tested on
    something input as large as 1000000000.
    A 'term' is returned by isqrt_in_lambda() representing
    the isqrt function
    """
    return lambda n: int(n ** 0.5)


############################################################

def list_map_in_lambda():
    """
    HX: 15 points
    This one is what we often call "eat-your-own-dog-food"
    Please implement a (higher-order) list-map function in
    LAMBDA. Note that the list in LAMBDA can be built with
    the constructs TMnil0 and TMcons (which are more or less
    like list_nil and list_cons in ATS, respectively)
    A 'term' is returned by list_map_in_lambda() representing
    the list-map function
    """
    TMnil0 = lambda: []
    TMcons = lambda head, tail: [head] + tail

    def map_lambda(f):
        def apply_map(lst):
            if lst == TMnil0():
                return TMnil0()
            else:
                return TMcons(f(lst[0]), apply_map(lst[1:]))

        return apply_map

    return map_lambda


############################################################
############################################################
# end of [HWXI/CS525-2024-Fall/assigns/03/assign03.py]
############################################################

# Test
isqrt = isqrt_in_lambda()
list_map = list_map_in_lambda()

test_list = [0, 2, 10, 1000000000]
result = list_map(isqrt)(test_list)

print(f"Result: {result}")

