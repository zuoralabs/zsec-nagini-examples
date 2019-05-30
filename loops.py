from nagini_contracts.contracts import *
from nagini_contracts.obligations import MustTerminate


class Mutable:
    def __init__(self, a: int) -> None:
        self.a = a  # type: int
        Ensures(Acc(self.a) and self.a is a)


@Pure
def div(aa: int, bb: int) -> int:
    Requires(bb != 0)
    return int(aa / bb)


@Predicate
def acc_mutable(m: Mutable) -> bool:
    return Acc(m.a)


@Pure
@Ghost
def measure(_i: int) -> int:
    """Termination measure used to prove termination in the while loop"""
    return 2 - _i


@Pure
def Iff(a: bool, b: bool) -> bool:
    """If-and-only-if (double implication)

    This illustrates that you can programmatically specify contracts using pure functions
    """
    return Implies(a, b) and Implies(b, a)


@Pure
def InRange(start: int, xx: int, end: int) -> bool:
    return start <= xx and xx < end


def while_loop(m: Mutable) -> int:
    """Verify a post condition. As a bonus, use a mutable object as input.

    Note that loop invariants hold just before checking the loop entry condition.
    For the loop below, the loop invariants must hold before each entry into the loop, and one last time
    after the final execution of the loop body (when ii == 2).
    """
    Requires(Acc(acc_mutable(m), 1))
    Ensures(Acc(acc_mutable(m), 1))
    Ensures(0 < Result())

    ss = Unfolding(acc_mutable(m), m.a)  # need to unfold permissions to access m.a.

    if ss < 0:
        ss = - ss

    Assert(0 <= ss)

    yy = False

    ii = 0
    while ii < 2:
        Invariant(InRange(0, ii, 3))
        Invariant(0 <= ss)
        Invariant(Implies(1 < ii, 0 < ss))  # post condition
        Invariant(Iff(measure(ii) == 0, yy))  # post condition; could also have just used Implies
        Invariant(MustTerminate(measure(ii)))  # not necessary here

        ss = ss + ii

        if ii == 1:
            yy = True

        ii = ii + 1

    Assert(ii == 2)
    Assert(yy)
    #Assert(False)  # smoke detector

    return ss


def for_loop(m: Mutable) -> int:
    """How to verify the postconditions of a for loop.

    Like the for loop, Invariants must hold after the last execution of the loop.
    Unlike the while loop above, the loop counter `ii` will not change after the last execution,
    so we cannot make use of the value of `ii` to make statements about the post condition.
    Instead, we can use `last in Previous(ii)` where last is the last value of `ii` in the loop.

    """
    Requires(Acc(acc_mutable(m), 1))
    Ensures(Acc(acc_mutable(m), 1))
    Ensures(0 < Result())

    ss = Unfolding(acc_mutable(m), m.a)

    if ss < 0:
        ss = - ss

    yy = False

    last = 1
    for ii in range(0, last+1):
        Invariant(InRange(0, ii, last+1))
        Invariant(0 <= ss)
        Invariant(MustTerminate(measure(ii)))  # not necessary here
        Invariant(Iff(last in Previous(ii), yy))  # post condition; could also have used Implies
        Invariant(Implies(last in Previous(ii), 0 < ss))  # post condition
        Invariant(Implies(1 < ii, 0 < ss))  # 1 < ii is always false; this implication is trivially true.

        ss = ss + ii

        if ii == 1:
            yy = True

    Assert(ii == 1)
    Assert(yy)
    # Assert(False)  # Smoke detector

    return ss


def main() -> None:
    #div(1, 0)  # raises verification error
    mm = Mutable(1)
    Assert(mm.a == 1)
    Fold(acc_mutable(mm))  # fold up the permissions
    div(10, for_loop(mm))

