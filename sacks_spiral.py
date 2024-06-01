from numpy import array
from PIL import Image, ImageDraw
import numpy as np
import math

width_of_the_set = 1000

# Segmented variation on the Sieve of Eratosthenes
def prime_sieve(n):
    primes = []
    segment_size = math.floor(math.sqrt(n))

    # Use classical Sieve of Eratosthenes for first segment
    sieve = np.full((segment_size, ), True)
    for i in range(2, segment_size):
        if sieve[i]:
            primes.append(i)

            for j in range(i**2, segment_size, i):
                sieve[j] = False

    for segment_start in range(segment_size+1, n, segment_size):
        sieve = np.full((segment_size, ), True)

        # Pre-sieve previous primes
        for p in primes:
            if p**2 > (segment_start + segment_size):
                break

            prime_start = math.ceil(segment_start/p)*p

            for x in range(prime_start, segment_start + segment_size, p):
                sieve[x - segment_start] = False

        # Sieve out new primes
        for i in range(0, segment_size):
            p = i + segment_start
            if sieve[i] and p <= n:
                primes.append(p)

    return primes

def euler_polynomial(n):
    i = 0
    k = 41

    while k <= n:
        yield k
        i += 1
        k = i**2 + i + 41

def spiral_coords(i, s):
    t = math.sqrt(i)
    theta = 2*math.pi*t
    x = t*math.cos(theta) + s
    y = -t*math.sin(theta) + s

    return x, y

def sacks_spiral(size, scale, marker_size):
    width = 2*size + 1
    image = Image.new('RGB', (scale*width, scale*width), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    primes = prime_sieve(size**2)

    for p in primes:
        x, y = spiral_coords(p, size)
        draw.rectangle((scale*x, scale*y, scale*x + marker_size, scale*y + marker_size), fill=(0, 0, 0))

    for k in euler_polynomial(size**2):
        if k not in primes:
            continue

        x, y = spiral_coords(k, size)
        draw.rectangle((scale*x, scale*y, scale*x + marker_size, scale*y + marker_size), fill=(255, 0, 0))

    image.save("./sacks_spiral.png")

sacks_spiral(120, 2, 4)
