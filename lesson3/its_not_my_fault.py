import hashlib
import gmpy2
from itertools import product
from multiprocessing import Pool, cpu_count
import string

# ------------------------------
# MD5 suffix brute-forcer (Made by ChatGPT)
# ------------------------------
def find_matching_md5_suffix(prefix, target_suffix, max_length=8):
    chars = string.ascii_letters + string.digits
    attempt = 0

    for length in range(1, max_length + 1):
        for suffix_tuple in product(chars, repeat=length):
            suffix = ''.join(suffix_tuple)
            test_string = prefix + suffix
            md5_hash = hashlib.md5(test_string.encode()).hexdigest()
            attempt += 1
            if md5_hash.endswith(target_suffix):
                print(f"[+] Match found after {attempt} attempts!")
                return test_string, md5_hash

    print("[-] No MD5 match found.")
    return None, None

# ------------------------------
# Finding p+q
# ------------------------------
def recover_q(n, p):
    return n // p

def compute_p_plus_q(n, p):
    q = recover_q(n, p)
    return p + q

# ------------------------------
# dp-based GCD factor attack (Made by ChatGPT)
# ------------------------------
def check_dp(dp_tuple):
    dp, m, e, n = dp_tuple
    try:
        exponent = e * dp
        power = gmpy2.powmod(m, exponent, n)
        diff = m - power
        f = gmpy2.gcd(diff, n)
        if f > 1 and f < n:
            return (dp, f)
    except Exception:
        pass
    return None

def find_factor_with_dp(m, e, n, dp_max=2**20):
    m = gmpy2.mpz(m)
    e = gmpy2.mpz(e)
    n = gmpy2.mpz(n)

    with Pool(processes=cpu_count()) as pool:
        tasks = ((dp, m, e, n) for dp in range(1, dp_max))
        for result in pool.imap_unordered(check_dp, tasks, chunksize=1000):
            if result:
                pool.terminate()
                print(f"[+] Found: dp = {result[0]}, factor = {result[1]}")
                return result
    print("[-] No factor found with dp scan.")
    return None


def main():
    print(find_matching_md5_suffix('95193', '24b3a8')) # 95193laj0 (Enter this into netcat)

    # Copy Public_Modulus and Clue from netcat
    Public_Modulus = 69379440985050052608739726974415505934522696961979391224375897548283233575743935970658350141560735544344697937958991455250057769991261071085278014158460877773295028510327950736815527937871704670700155979596884465071527880716023023658693428781379486185310174710121456682480658505005700951648475019921591121471
    Clue = 8965564218677236874075217182953408583482972248440927148073036831090833107328662174587878859010137015097621054688163305589516057729296646784379200669815251400030214988546046006831282552320791303348061985155448178238595548625451057929582751972280848615342018819044849363154539683579353200984891667370901964927
    m = 950914839705029 # Enter a random large PRIME number
    dp, factor = find_factor_with_dp(m, Clue, Public_Modulus)

    # Enter following p+q output to get flag
    print(compute_p_plus_q(Public_Modulus, factor)) # p+q

# Entry point
if __name__ == "__main__":
    main()

''' Terminal
Enter a string that starts with "95193" (no quotes) which creates an md5 hash that ends in these six hex digits: 24b3a8
95193laj0

Public Modulus :  69379440985050052608739726974415505934522696961979391224375897548283233575743935970658350141560735544344697937958991455250057769991261071085278014158460877773295028510327950736815527937871704670700155979596884465071527880716023023658693428781379486185310174710121456682480658505005700951648475019921591121471
Clue :  8965564218677236874075217182953408583482972248440927148073036831090833107328662174587878859010137015097621054688163305589516057729296646784379200669815251400030214988546046006831282552320791303348061985155448178238595548625451057929582751972280848615342018819044849363154539683579353200984891667370901964927
16662627794857816346806611642411271053443748943034774232990491780437107110472575256143213246916626577664644757131230559701760741178480286901781295780987128

picoCTF{1_c4n'7_b3l13v3_17'5_n07_f4ul7_4774ck!!!}
'''
# Public Mod = n
# Clue = e