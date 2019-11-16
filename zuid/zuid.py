import binascii
import math
import os
import random
import string
import time

import six

CHARSET = string.digits + string.ascii_uppercase + string.ascii_lowercase


class ZUID(object):
    """The ZUID class is a callable factory for identifiers.

    Ideally, one should create one ZUID instance for each entity
    requiring ids, and call the instance to generate ids as needed.

    """

    def __init__(self, prefix="", length=22, timestamped=False, charset=CHARSET):
        """Initializes the id factory

        :param prefix: the desired string prefix
        :type prefix: str

        :param length: the desired id length, in characters.
        :type length: int

        :param timestamped: if True, the first 8 bytes of the id will be
        formed by the current time since epoch in nanoseconds.
        :type timestamped: bool

        :param charset: the charset to use for encoding the
        values. The default is the 62 chars sequence of all digits,
        ASCII uppercase and ASCII lowercase letters, for base 62 URL
        safe ids.
        :type charset: str

        """
        self.prefix = prefix

        self.timestamped = timestamped
        self.charset = charset

        self._base = len(CHARSET)

        self.char_length = length
        self.length = length + len(prefix)

        self._random = random.SystemRandom()

    def __call__(self):
        """Generates a new random id, using the factory's current parameters.

        """

        timestamp = ""
        length = self.char_length

        if self.timestamped:
            timestamp = self.charset_encode(int(time.time() * 1e9)).rjust(11, "0")
            length -= len(timestamp)

        id_ = self._random_chars(length)

        return self.prefix + timestamp + id_

    def _random_chars(self, c):
        chars = [self._random.choice(self.charset) for _ in six.moves.range(c)]
        return "".join(chars)

    def charset_encode(self, num):
        """Encodes the given number with the charset defined for this instance

        """
        chars = []
        while num > 0:
            num, r = divmod(num, self._base)

            chars.append(self.charset[r])

        return "".join(chars[::-1])

    @property
    def bits(self):
        bits_per_char = math.log(self._base, 2)
        return int(self.length * bits_per_char)

    def collision_probability(self, per_second=1000, probability=0.01):
        """Calculate how many ids have to be generated to have the given
        probability of collision

        """

        import humanize

        outputs = 2 ** (self.bytelength * 8)

        num = math.sqrt(2.0 * outputs * -math.log1p(-probability))

        seconds_in_year = 3600 * 24 * 365

        years = humanize.intword(num / (per_second * seconds_in_year))

        message = (
            "If you generate {} ids per second, it would take {} years of work to "
            "have a {}% chance of at least one collision"
        ).format(per_second, years, probability * 100)

        return (message,)
