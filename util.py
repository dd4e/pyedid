def hex2bytes( hex ):
    numbers = []
    for i in range( 0, len(hex), 2 ):
        pair = hex[i:i+2]
        numbers.append(int(pair, 16))
    return bytes(numbers)
