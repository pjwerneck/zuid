

import math
import os
import string
import time
import binascii

CHARSET = string.digits + string.ascii_uppercase + string.ascii_lowercase


class ZUID(object):
    """The ZUID class is a callable factory for identifiers.

    Ideally, one should create one ZUID instance for each entity
    requiring ids, and call the instance to generate ids as needed.

    """

    def __init__(self, prefix='', bytelength=16, length=None, timestamped=False, charset=CHARSET):
        """Initializes the id factory

        :param prefix: the desired string prefix
        :type prefix: str

        :param bytelength: how many bytes to use for the id, not including
        the prefix. Default is 16 bytes, like UUIDs.
        :type bytelength: int

        :param length: the desired id length, in characters. The final id
        will be padded with zeroes if necessary. If `None`, a value large
        enough to fit the given bytelength and prefix will be
        calculated. ValueError is raised if a value is provided and it's
        less than the mininum required for the given bytelength and
        prefix.
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
        if timestamped and bytelength < 9:
            raise ValueError("Timestamps use 8 bytes, therefore timestamped ids must be at least 9 bytes long.")

        self.prefix = prefix
        self.bytelength = bytelength

        self.timestamped = timestamped
        self.charset = charset

        self._base = len(CHARSET)

        if length is None:
            self.length = self.max_length

        else:
            if length < self.max_length:
                raise ValueError("The desired length is shorter than needed for the largest id number. "
                                 "Either increase length or decrease bytelength")

            self.length = length

    def __call__(self):
        """Generates a new random id, using the factory's current parameters.

        """

        timestamp = ''
        bytelength = self.bytelength
        charlength = self.length - len(self.prefix)

        if self.timestamped:
            timestamp = self.charset_encode(int(time.time() * 1e9)).rjust(11, '0')
            bytelength -= 8
            charlength -= len(timestamp)

        num = self.charset_encode(self._random_int(bytelength))

        num = num.rjust(charlength, '0')

        return self.prefix + timestamp + num

    def _random_int(self, n):
        ba = bytearray(os.urandom(n))
        return int(binascii.hexlify(ba), 16)

    def charset_encode(self, num):
        """Encodes the given number with the charset defined for this instance

        With the default charset, this results in base 62 encoded
        strings

        """
        chars = []
        while num > 0:
            num, r = divmod(num, len(self.charset))

            chars.append(self.charset[r])

        return ''.join(chars[::-1])

    @property
    def max_length(self):
        """Calculates the max length of ids generated by this factory

        """
        chars_per_id = int(math.ceil(self.bytelength * 8 / math.log(self._base, 2)))

        return len(self.prefix) + chars_per_id

    def collision_probability(self, per_second=1000, probability=0.01):
        """Calculate how many ids have to be generated to have the given
        probability of collision

        """

        import humanize
        outputs = 2 ** (self.bytelength * 8)

        num = math.sqrt(2.0 * outputs * -math.log1p(-probability))

        seconds_in_year = 3600 * 24 * 365

        years = humanize.intword(num / (per_second * seconds_in_year))

        message = ("If you generate {} ids per second, it would take {} years of work to "
                   "have a {}% chance of at least one collision").format(per_second, years, probability * 100)

        return message
