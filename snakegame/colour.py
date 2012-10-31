import hashlib

def hash_colour(data):
    data = map(ord, hashlib.md5(data).digest())
    colour = data[::3], data[1::3], data[2::3]
    colour = map(sum, colour)
    return (colour[0] % 255, colour[1] % 255, colour[2] % 255)

