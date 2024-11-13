############################################################
#
# Assign04 for CS525, Fall, 2024
# It is due Monday, the 21st of October, 2024
# Note that the due time is always 11:59pm of
# the due date unless specified otherwise.
#
############################################################
############################################################
import sys

sys.setrecursionlimit(20000)


def eight_queen_puzzle():
    """
    HX-2024-10-12: (40 points)
    Please encode in LAMBDA the implementation of the 8-queen puzzle
    in the following page:
    https://ats-lang.sourceforge.net/DOCUMENT/INT2PROGINATS/HTML/x631.html
    And your encoding should pass simple type-checking and/or type-inference
    """
    N = 8

    # Define the printing functions
    print_dots = lambda i: (print(". ", end="") or print_dots(i - 1)) if i > 0 else None
    print_row = lambda i: (print_dots(i), print("Q ", end=""), print_dots(N - i - 1), print())
    print_board = lambda bd: [print_row(bd[i]) for i in range(N)]

    # Checking if two queens attack each other - if two queens are in the same column or diagonal
    could_attack = lambda i0, j0, i1, j1: j0 != j1 and abs(i0 - i1) != abs(j0 - j1)

    # Recursively check if the current queen conflicts with the previous queen
    def has_conflict(i0, j0, bd, max_row):
        for i in range(max_row + 1):
            if not could_attack(i0, j0, i, bd[i]):
                return False
        return True

    # Recursive function to search all possible solutions
    def search(bd, i, j, nsol):
        # print(f"bd:{bd}, i:{i}, j:{j}, sol:{nsol}")
        if j < N:
            test = has_conflict(i, j, bd, i - 1)
            if test:
                bd1 = bd[:i] + [j] + bd[i + 1:]
                if i + 1 == N:
                    print(f"Solution #{nsol + 1}:\n")
                    print_board(bd1)
                    return search(bd, i, j + 1, nsol + 1)
                else:
                    return search(bd1, i + 1, 0, nsol)
            else:
                return search(bd, i, j + 1, nsol)
        else:
            if i > 0:
                return search(bd, i - 1, bd[i - 1] + 1, nsol)
            else:
                return nsol

    total_solutions = search([-1] * N, 0, 0, 0)
    print(f"There are {total_solutions} solutions in total.")


############################################################
############################################################
# end of [HWXI/CS525-2024-Fall/assigns/04/assign04.py]
############################################################

# Test
if __name__ == "__main__":
    eight_queen_puzzle()
