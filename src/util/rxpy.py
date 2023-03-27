import reactivex as rx
from reactivex import operators as ops


def _snd(t):
    return t[1]


def compact():
    def _compact(source):
        return source.pipe(ops.filter(lambda x: x is not None))
    return _compact


def throttle_emissions(delay):
    """
    Delay events from source:  X...500ms..Y..1000ms..Z...1500ms..T
    """

    i = rx.interval(delay)

    def _throttle(source):
        return rx.zip(i, source).pipe(ops.map(_snd))

    return _throttle


def buffer_chunks(predicate):
    """
    [1,2,3,4] : 'lambda x: x < 2' => [1] [2,3,4]
    """
    def run(source):
        return source.pipe(
            # Multicast is deprecated in rxjs7.
            # Rxpy doesn't have alternative.
            # No clue how this works, seems complicated.
            ops.multicast(
                subject_factory=lambda _: rx.Subject(),
                mapper=lambda s: s.pipe(
                    ops.buffer(s.pipe(ops.filter(predicate))),
                    ops.filter(lambda x: len(x) > 0)
                )
            )
        )
    return run
