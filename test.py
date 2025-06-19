import blockcypher
import random
import time


def get_rand_bytearray(int_for_mb):
    randobj = random.SystemRandom()
    len_bytes = 1024 * 1024 * 8 * int_for_mb
    randarray = bytearray()
    randarray = randarray + randobj.getrandbits(len_bytes).to_bytes((len_bytes // 8), "big")
    return randarray
def check():
    Text = "test1"
    pw = "password"
    blockcypherobj = blockcypher.block_cypher_parts()
    pw_array_liste = blockcypherobj.pw_list_gen(pw)
    first_block = blockcypherobj.get_rand_bytearray(512)
    cyphertext = blockcypherobj.cbc_mode_cypher_verschlüsseln(bytearray(Text,"UTF-8"),first_block,True,blockcypherobj.pw_array_liste)
    print(cyphertext)
    plaintext = blockcypherobj.cbc_mode_cypher_entschlüsseln(cyphertext,first_block,blockcypherobj.pw_array_liste,True)
    print(plaintext)

def benchmark(mb_size_int):
    randtestdata = get_rand_bytearray(mb_size_int)
    time_start = time.time()
    pw = "password"
    blockcypherobj = blockcypher.block_cypher_parts()
    pw_array_liste = blockcypherobj.pw_list_gen(pw)
    first_block = blockcypherobj.get_rand_bytearray(512)
    cyphertext = blockcypherobj.cbc_mode_cypher_verschlüsseln(randtestdata,first_block,True,blockcypherobj.pw_array_liste)
    time_stop = time.time()
    time_spend = time_stop - time_start
    mb_per_s =  mb_size_int  /time_spend
    print("time: " + str(time_spend) + " for " + str(mb_size_int) + "mb or " , str(mb_per_s) + "mb/s")


check()
benchmark(1)
benchmark(10)
benchmark(100)


