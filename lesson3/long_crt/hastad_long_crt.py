from Crypto.Util.number import inverse, long_to_bytes
import gmpy2

n_list = []
c_list = []

file_path = 'lesson3/long_crt/long_crt.txt'

with open(file_path, 'r') as f:
    for line_number, line in enumerate(f, 1):
        idx = line.index('=') # Get index of equal sign

        # line[idx+1:] to exclude everything before "=" 
        value = int(line[idx+1:])

        if line[0] == 'n':
            n_list.append(value)
        elif line[0] == 'c':
            c_list.append(value)

def crt(n_list, c_list):
    N = 1
    for n in n_list:
        N *= n

    summation = 0
    for i in range(len(n_list)):
        Ni = N // n_list[i]
        Mi = inverse(Ni, n_list[i])
        summation += Ni*Mi*c_list[i]
    return summation%N

m, exact = gmpy2.iroot(crt(n_list, c_list), len(n_list))
if exact:
    msg = str(long_to_bytes(m))[2:-1]
    print(msg.strip()) # NYRCS{br4dyn_hashbrown_attack}