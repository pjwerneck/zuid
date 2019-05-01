# zuid

Generates URL-safe random ids with a prefix and optional timestamp.


## Installing

```
pip install zuid
```

## Usage

The `ZUID` class works as a callable id factory for a given prefix:

```
>>> from zuid import ZUID
>>> generator = ZUID(prefix='user_')
>>> generator()
'user_03QewpfEIpPWUICXdgtvdR'
>>> generator()
'user_1LJSXMoyH6p7VsiL8wwIm1'
```

The factory generates ids that are 22 chars long by default, which in
base 62 corresponds to 131 random bits. For comparison, a v4 UUID has
122 random bits. It can be changed with the `length` parameter:

```
>>> generator = ZUID(prefix='user_', length=27)
>>> generator()
'user_X5fSIStIKpYWcg07nqEfPbMvmME'
```

With the `timestamped` parameter, the factory uses the current nanoseconds since epoch as the first 8 bytes, preserving the order when sorting by id.

```
>>> generator = ZUID(prefix='user_', timestamped=True)
>>> generator()
'user_1qzuvBwgHdQVO2gA4GelYX'
>>> generator()
'user_1qzuvCscVyClzGaqakgvsl'
>>> generator()
'user_1qzuvDb0TuCuIJJON103Of'
>>> generator()
'user_1qzuvES4mTQ7fWykywvjNb

```
