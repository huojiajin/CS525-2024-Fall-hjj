#include "share/atspre_staload.hats"

(* ****** ****** *)
(*
**
** Finding the number
** of bits in int-values
**
*)
(* ****** ****** *)
//
(*
HX: Sample
factorial(n) = 1*2*...*n
*)
//
// extern
// fun factorial : int -> int

//
(* ****** ****** *)
//
// HX: 5 points
// The function int_test should
// return the size of an integer in C
// where the size means the number of bits.
// Note that you should only use comparison
// and addition in the implementation of the
// following function [int_test].
//
extern fun int_test(): int
//

implement int_test (): int =
  let
    fun count_bits_rec (num: int, bits: int): int =
      if num > 0 then count_bits_rec(num * 2, bits + 1) else bits
  in
    count_bits_rec(1, 1)
  end


(* ****** ****** *)
//
// HX: 10 points
// The function [gheep] is defined as follows:
//
fun ghaap(n: int): int =
(
if
(n >= 2)
then n * ghaap(n-1) * ghaap(n-2) else (n+1)
// end of [if]
)
//
// Please implement a tail-recursive function gheep
// such thats gheep(n) = ghaap(n) for all integers n
//
extern fun gheep (n: int): int

implement gheep (n: int): int =
    let
        fun gheep_tailrec (i: int, n: int, acc1: int, acc2: int): int =
            if i > n then acc1
            else gheep_tailrec(i + 1, n, i * acc1 * acc2, acc1)
    in
        if n >= 2 then gheep_tailrec(2, n, 2, 1)
        else n + 1
    end


//
(* ****** ****** *)
//
datatype
intlist =
|intlist_nil of ()
|intlist_cons of (int, intlist)
//
(* ****** ****** *)
//
// HX: 15 points
//
// intlist_append returns the concatenation
// of two given integer lists. For instance,
// given xs=(0,2,4) and ys = (1,3,5), then the
// returned list is (0, 2, 4, 1, 3, 5)
// Please give a tail-recursive implementation
// of intlist_append.
//
extern
fun
intlist_append : (intlist, intlist) -> intlist
//
(* ****** ****** *)

implement intlist_append (xs: intlist, ys: intlist): intlist =
  let
    fun intlist_reverse_append (xs1: intlist, ys1: intlist): intlist =
        case+ xs1 of
        | intlist_nil() => ys1
        | intlist_cons (x, xs1) => intlist_reverse_append(xs1, intlist_cons(x, ys1))
    fun intlist_reverse(xs2: intlist): intlist =
        intlist_reverse_append(xs2, intlist_nil)
  in
    intlist_reverse_append(intlist_reverse(xs), ys)
  end

(* end of [CS525-2024-Fall/assigns/00/assign00.dats] *)

(* Test Code *)



implement main0() =

    let
        val a = int_test()
        val b = gheep(6)
        val xs = intlist_cons(0, intlist_cons(2, intlist_cons(4, intlist_nil())))
        val ys = intlist_cons(1, intlist_cons(3, intlist_cons(5, intlist_nil())))
        fun print_intlist(xs: intlist): void =
          case+ xs of
          | intlist_nil() => ()
          | intlist_cons (x, xs) => (
              println! ("Element:", x);
              print_intlist(xs)
            )
    in
        println!("First Question Result: ", a);
        println!("Second Question Result: ", b);
        println!("Third Question Result: ");
        print_intlist(intlist_append (xs, ys))
    end

(* Test Code End *)