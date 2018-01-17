import sys

b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def encode(b):
    """Encode bytes to a base58-encoded string"""
    # Convert big-endian bytes to integer
    n = int(b, 16)
    # Divide that integer into bas58
    res = []
    while n > 0:
        n, r = divmod (n, 58)
        res.append(b58_digits[r])
    res = ''.join(res[::-1])

    # Encode leading zeros as base58 zeros
    czero = "00"

    pad = 0
    for i in range(0,len(b),2):
        if b[i:i+2] == czero: pad += 1
        else: break
    return b58_digits[0] * pad + res


s = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

if len(sys.argv) < 2:
    print("Please pass a string argument to this script")
    exit(1)

addr = sys.argv[1]

if addr[0] != s[0]:
    print("First letter must be q")
else:
    if addr[1] not in s[:4]:
        print("Second letter must be one of q|p|z|r")
    else:
        allValid = True;
        for letter in addr:
            if letter not in s:
                print("All letters must be one of " + s)
                allValid = False
                break
        if allValid:

            if len(addr) > 42:
                print("Address too long")
            else:
                # Good to go
                binaryString = ""
                for letter in addr:
                    binaryString += format(s.find(letter),'05b')

                #print("Binary: " + binaryString)

                if len(binaryString) % 4 != 0:
                    # If not divisable by four we need to append in binary instead
                    bmin = binaryString + "0"*(200-len(binaryString))
                    bmax = binaryString + "1"*(200-len(binaryString))

                    # To hex string (https://stackoverflow.com/a/2072384)
                    hmin = '%0*X' % ((len(bmin) + 3) // 4, int(bmin, 2))
                    hmax = '%0*X' % ((len(bmax) + 3) // 4, int(bmax, 2))
                else:
                    h = '%0*X' % ((len(binaryString) + 3) // 4, int(binaryString, 2))
                    #print("Hex: " + h)

                    hmin = h + "0"*(50-len(h))
                    hmax = h + "F"*(50-len(h))

                #print("Min: " + hmin)
                #print("Max: " + hmax)

                emin = encode(hmin)
                #print(emin)
                emax = encode(hmax)
                #print(emax)

                for i in range(0,len(emin)+1):
                    if emin[i] != emax[i]:
                        idif = i
                        #print(emin[i])
                        #print(emax[i])
                        break

                ecut = emin[:idif]
                #print(ecut)

                #im = min(ord(emin[idif]),ord(emax[idif]))
                ind1 = b58_digits.find(emin[idif])
                ind2 = b58_digits.find(emax[idif])
                im = min(ind1,ind2)

                d = abs(ind2-ind1)

                letters = ""
                for i in range(im+1,im+d):
                    letters += b58_digits[i]
                #print(letters)

                print("Have vanitygen search for:")

                if len(letters) != 0:
                    for letter in letters:
                        print ecut + letter,
                else:
                    #print("Need to look at next letter")
                    ind1 = b58_digits.find(emin[idif+1])
                    ind2 = b58_digits.find(emax[idif+1])

                    sol = []
                    for i in range(ind1+1,len(b58_digits)):
                        print ecut + emin[idif] + b58_digits[i],

                    for i in range(1,ind2):
                        print ecut + emax[idif] + b58_digits[i],
