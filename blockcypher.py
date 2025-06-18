import hashlib
import random
version = "v2025.06.18_22:07"
class block_cypher_parts():
    first_block = ""

    def checksumm_anhängen_sha256(self,zu_verarbeitendes_array):
        #assert type(zu_verarbeitendes_array) == bytearray
        if type(zu_verarbeitendes_array) != bytearray:
            raise Exception("type zu_verarbeitendes_array is not Bytearray. it is ",type(zu_verarbeitendes_array))
        shaobj = hashlib.sha3_256()
        shaobj.update(zu_verarbeitendes_array)
        checksum = shaobj.digest()
        zu_verarbeitendes_array = zu_verarbeitendes_array + checksum
        return zu_verarbeitendes_array

    def checksumm_prüfen_sha256(self,zu_verarbeitendes_array):
        #assert type(zu_verarbeitendes_array) == bytearray
        if type(zu_verarbeitendes_array) != bytearray:
            raise Exception("type zu_verarbeitendes_array is not Bytearray. it is ",type(zu_verarbeitendes_array))
        erzugte_prüfsumme = bytearray()
        shaobj = hashlib.sha3_256()
        shaobj.update(zu_verarbeitendes_array[0:-32])
        erzugte_prüfsumme = shaobj.digest()


        if zu_verarbeitendes_array[-32:] == erzugte_prüfsumme:
            return True
        else:
            return False

    def festel_struktur_verschlüsseln(self, liste_pw_aray, aray_input_block):


        blockobj = block_cypher_parts()
        return blockobj.ARX_cypher_one_round_encyption(aray_input_block, liste_pw_aray)

    def festel_struktur_entschlüsseln(self, liste_pw_aray, aray_input_block):

        blockobj = block_cypher_parts()
        return blockobj.ARX_cypher_one_round_decyption(aray_input_block, liste_pw_aray)
        #aray_input_block = blockobj.ARX_cypher_one_round_decyption(aray_input_block, liste_pw_aray[8:])

    def pw_list_gen(self,pw_text_string):
        hashobj_for_konst = hashlib.sha3_512()
        """ranobj = random.SystemRandom()"""
        start_array = bytearray(pw_text_string, "UTF-8")
        rundencounter = 0
        pw_deriv_counter = 0
        pw_list = []
        konstant_start = bytearray("start","UTF-8")


        list_of_konstanst = []
        hashobj = hashlib.sha3_512()
        while rundencounter != 36:
            while pw_deriv_counter != 30000:
                pw_deriv_counter = pw_deriv_counter + 1
                hashobj_for_konst.update(konstant_start)
                konstant_start = hashobj_for_konst.digest()
                hashobj_for_konst = hashlib.sha3_512()
                """print(rundencounter," ",pw_deriv_counter)"""
            list_of_konstanst.append(konstant_start)
            rundencounter += 1
            pw_deriv_counter = 0
        """PW liste hat anzahl einträge rundencounter und jeweils eine länge von 512bit oder 64 byte"""

        rundencounter = 0
        pw_deriv_counter = 0
        pw_list = []
        while rundencounter != 36:
            while pw_deriv_counter != 30000:
                pw_deriv_counter = pw_deriv_counter + 1
                hashobj.update(start_array + list_of_konstanst[rundencounter])
                start_array = hashobj.digest()
                hashobj = hashlib.sha3_512()
                """print(rundencounter," ",pw_deriv_counter)"""
            pw_list.append(start_array)
            rundencounter += 1
            pw_deriv_counter = 0
        """PW liste hat anzahl einträge rundencounter und jeweils eine länge von 512bit oder 64 byte"""
        self.pw_array_liste = pw_list

        #return pw_list

    def xor(self,a, b):
        if len(a) != len(b):
            raise Exception("array lengh for xor is uneven ",len(a)," ",len(b))
        #assert len(a) == len(b)
        output_array = []
        index_counter = 0
        integer_a = int.from_bytes(a,"big")
        integer_b = int.from_bytes(b,"big")

        xoredint = integer_a ^ integer_b
        return bytearray(int.to_bytes(xoredint,len(a),"big"))



    def get_rand_bytearray(self,length_in_bits):
        #assert length_in_bits % 8 == 0
        if length_in_bits % 8 != 0:
            raise Exception("can not get a random array with lenght ",length_in_bits)
        randobj = random.SystemRandom()
        randarray = bytearray()
        randarray = randarray + randobj.getrandbits(length_in_bits).to_bytes((length_in_bits // 8), "big")
        return randarray

    def modular_addition_of_two_arrays_with_len_32(self,array_01,array_02):
        if len(array_01) != 32 or len(array_02) != 32:
            raise Exception("input lengh error")
        if type(array_01) != bytearray or type(array_02) != bytearray:
            raise Exception("input type error")


        #modulo_size = pow(2, 256)
        modulo_size = 115792089237316195423570985008687907853269984665640564039457584007913129639936
        array_03 = bytearray()
        array_01_int = int.from_bytes(array_01, "big")
        array_02_int = int.from_bytes(array_02, "big")
        array_03_int = (array_01_int + array_02_int) % modulo_size
        array_03 = int.to_bytes((array_03_int), 32, "big")

        return bytearray(array_03)

    def reverse_modular_addition_of_two_arrays_with_len_32(self,array_01,array_02):
        if len(array_01) != 32 or len(array_02) != 32:
            raise Exception("input lengh error")
        if type(array_01) != bytearray or type(array_02) != bytearray:
            raise Exception("input type error")

        #modulo_size = pow(2, 256)
        modulo_size = 115792089237316195423570985008687907853269984665640564039457584007913129639936
        array_03 = bytearray()
        array_01_int = int.from_bytes(array_01, "big")
        array_02_int = int.from_bytes(array_02, "big")

        # weil ist x + y wahr kleiner als mod bei der addition
        array_03_int = (array_01_int - array_02_int)
        if array_03_int >= 0:
            array_03 = int.to_bytes((array_03_int % modulo_size ), 32, "big")
            #print("is bigger")


        elif array_03_int == 0:
            array_03 = int.to_bytes(array_03_int,32,"big")

        else:
            array_03_int = modulo_size + (array_01_int - array_02_int)
            array_03 = int.to_bytes((array_03_int % modulo_size ) , 32, "big")
            #print("zweig 2")
        return bytearray(array_03)

    def test_for_mod_addition(self):
        array_01 = bytearray("test", "UTF-8")
        array_02 = bytearray("00000000TEST2", "UTF-8")

        #test_array_big = int.to_bytes((pow(2, 256) - 1 ), 32, "big")
        test_array_big = int.to_bytes(0,32,"big")
        print("test array big : ",test_array_big)
        while len(array_01) != 32:
            array_01 = bytearray("0", "UTF-8") + array_01
        while len(array_02) != 32:
            array_02 = array_02 + bytearray("0", "UTF-8")
        blockobj = block_cypher_parts()
        array_test = blockobj.modular_addition_of_two_arrays_with_len_32(array_01, array_02)
        print("after addition ",array_test)
        array_test = blockobj.reverse_modular_addition_of_two_arrays_with_len_32(array_test, array_02)
        print("after reverse ",array_test)
        print("")
        array_test = blockobj.modular_addition_of_two_arrays_with_len_32(array_01, bytearray(test_array_big))
        print("after addition ", array_test)
        array_test = blockobj.reverse_modular_addition_of_two_arrays_with_len_32(array_test, bytearray(test_array_big))
        print("after reverse ",array_test)

    def bytearray_shift_right(self,array_01,shiftnummber):
        if type(shiftnummber) != int or type(array_01) != bytearray:
            raise Exception("input type error")
        array_shifted = bytearray()
        array_shifted = array_01[(shiftnummber):] + array_01[0:(shiftnummber)]

        return array_shifted

    def bytearray_shift_left(self,array_01,shiftnummber):
        if type(shiftnummber) != int or type(array_01) != bytearray:
            raise Exception("input type error")

        array_shifted = bytearray()
        array_shifted = array_01[-shiftnummber:] + array_01[0:-shiftnummber]

        return array_shifted

    def ARX_cypher_one_round_encyption(self,array_01,roundkey_array_in_list):
        if len(array_01) != 64:
            raise Exception("len array is not 64")
        #roundkey size musst be 256
        #for i in roundkey_array_in_list:
        #    if len(i) != 64:
        #        raise Exception("falsche round key leght. die funktion geht von nem 65 byte sha3 input aus")
            #den schrit vileicht ibn der nachsten zeile auslase und unten zwei mal abschnitt mit i[0:32] und i[32:]
        array_links = array_01[0:32]
        array_rechts = array_01[32:]



        for i in roundkey_array_in_list:
            array_links = self.bytearray_shift_right(array_links, 7)
            array_links = self.modular_addition_of_two_arrays_with_len_32(array_links, array_rechts)
            array_links = self.xor(array_links, i[0:32])
            array_rechts = self.bytearray_shift_left(array_rechts, 3)
            array_rechts = self.xor(array_rechts, array_links)

            array_links = self.bytearray_shift_right(array_links, 7)
            array_links = self.modular_addition_of_two_arrays_with_len_32(array_links, array_rechts)
            array_links = self.xor(array_links, i[32:])
            array_rechts = self.bytearray_shift_left(array_rechts, 3)
            array_rechts = self.xor(array_rechts, array_links)

        return bytearray(array_links) + bytearray(array_rechts)

    def ARX_cypher_one_round_decyption(self,array_01,roundkey_array_in_list):
        if len(array_01) != 64:
            raise Exception("len array is not 64")
        for i in roundkey_array_in_list:
            if len(i) != 64:
                raise Exception("falsche round key leght. die funktion geht von nem 65 byte sha3 input aus")
        # roundkey size musst be 256
        array_links = array_01[0:32]
        array_rechts = array_01[32:]
        neue_liste_roundkeys = []
        #for i in roundkey_array_in_list:
        #    neue_liste_roundkeys.append(i[0:32])
        #    neue_liste_roundkeys.append(i[32:])
        #roundkey_array_in_list = neue_liste_roundkeys

        for i in roundkey_array_in_list[::-1]:
            array_rechts = self.xor(array_rechts,array_links)
            array_rechts = self.bytearray_shift_right(array_rechts,3)
            array_links = self.xor(array_links,i[32:])
            array_links = self.reverse_modular_addition_of_two_arrays_with_len_32(array_links,array_rechts)
            array_links = self.bytearray_shift_left(array_links,7)

            array_rechts = self.xor(array_rechts, array_links)
            array_rechts = self.bytearray_shift_right(array_rechts, 3)
            array_links = self.xor(array_links, i[0:32])
            array_links = self.reverse_modular_addition_of_two_arrays_with_len_32(array_links, array_rechts)
            array_links = self.bytearray_shift_left(array_links, 7)

        return bytearray(array_links) + bytearray(array_rechts)

    def cbc_mode_cypher_verschlüsseln(self,plaintext_aray,xor_vorheriger_cyphertext_block,braucht_es_padding,pw_array_liste):
        #diese funktion fügt das xor_array_nicht dem return array zu_der erste block muss manuel dem file vor dem funktionsaufruf hinugefügt werden

        #assert type(plaintext_aray) == bytearray
        if type(plaintext_aray) != bytearray:
            raise Exception("type plaintext_array is not bytearray. It is ",type(plaintext_aray))
        #assert type(xor_vorheriger_cyphertext_block) == bytearray
        if type(xor_vorheriger_cyphertext_block) != bytearray:
            raise Exception("type xor_vorherriger_cyphertext_block is not bytearray. It is ",type(xor_vorheriger_cyphertext_block))
        #assert type(braucht_es_padding) == bool
        if type(braucht_es_padding) != bool:
            raise Exception("braucht_es_padding is not type bool. It is type ",type(braucht_es_padding))
        #assert type(pw_array_liste) == list
        if type(pw_array_liste) != list:
            raise Exception("type pw_array_list is not list. It is ",type(pw_array_liste))
        if braucht_es_padding == False:
            # assert len(plaintext_aray) % 64 == 0 fehler datei braucht padding
            if len(plaintext_aray) % 64 != 0:
                raise Exception("can only not be padded if len plaintext array is a multible of blocklengh")

        if braucht_es_padding == True:
            plaintext_aray.append(1)
            plaintext_aray.append(0)

            while len(plaintext_aray) % 64 != 0:
                plaintext_aray.append(0)

        #mache eine schleife mit del[index] fur die verschlüsselungsrotine
        cyphertext_array = bytearray()
        #cyphertext_array = cyphertext_array + xor_vorheriger_cyphertext_block
        vorheriger_cypher_block = xor_vorheriger_cyphertext_block
        local_xor = self.xor
        local_festel_struktur_verschlüsseln = self.festel_struktur_verschlüsseln
        while len(plaintext_aray) != 0:
            #encryption loop
            zu_xorender_plaintext_block = plaintext_aray[:64]
            zu_verschusselnder_plaintext_block_xored = local_xor(zu_xorender_plaintext_block,vorheriger_cypher_block)
            cyphertext_block = local_festel_struktur_verschlüsseln(pw_array_liste,zu_verschusselnder_plaintext_block_xored)
            #print("xor block verschlsseln :",vorheriger_cypher_block)
            vorheriger_cypher_block = cyphertext_block
            #fehler ling irgentwo beim xor
            del plaintext_aray[:64]
            #plaintext_aray = plaintext_aray[64:]
            cyphertext_array += cyphertext_block




        return cyphertext_array


    def cbc_mode_cypher_entschlüsseln(self,cyphertext_array,xor_vorheriger_cyphertext_block,pw_array_liste,padding_zu_entfernen):
        #assert len(cyphertext_array) % 64 == 0
        if len(cyphertext_array) % 64 != 0:
            raise Exception("len cyphertext_array must be multible of 64 bytes. It has a lenght of  ",len(cyphertext_array)," ")
        #assert len(xor_vorheriger_cyphertext_block) % 64 == 0
        if len(xor_vorheriger_cyphertext_block) % 64 != 0:
            raise Exception("len xor_vorheriger_cyphertext_block must be multible of 64 bytes. It has a lenght of  ",len(cyphertext_array)," ",)
        #assert type(cyphertext_array) == bytearray
        if type(cyphertext_array) != bytearray:
            raise Exception("type cyphertext_array is not bytearray. It is ",type(cyphertext_array))
        #assert type(xor_vorheriger_cyphertext_block) == bytearray
        if type(xor_vorheriger_cyphertext_block) != bytearray:
            raise Exception("type xor_vorheriger_cyphertext_block is not bytearray. It is ",type(xor_vorheriger_cyphertext_block))
        #assert type(pw_array_liste) == list
        if type(pw_array_liste) != list:
            raise Exception("type pw_array_liste is not list. It is ",type(pw_array_liste))
        #assert type(padding_zu_entfernen) == bool
        if type(padding_zu_entfernen) != bool:
            raise Exception("type padding_zu_entfernen is not bool. It is ",type(padding_zu_entfernen))
        output_plaintext_aray = bytearray()
        block_counter = 0
        gesammt_array_fur_xor = xor_vorheriger_cyphertext_block + cyphertext_array
        cyphertext_array_1 = cyphertext_array


        vorherriger_block = xor_vorheriger_cyphertext_block
        while len(cyphertext_array_1) != 0:
            cyphertext_block = cyphertext_array_1[:64]
            plaintext_block_xored = self.festel_struktur_entschlüsseln(pw_array_liste,cyphertext_block)
            plaintext_block = self.xor(plaintext_block_xored,gesammt_array_fur_xor[:64])
            output_plaintext_aray = output_plaintext_aray + plaintext_block
            #print("xor block entschlüsseln : ",gesammt_array_fur_xor[:64])
            vorherriger_block = cyphertext_block
            del cyphertext_array_1[:64]
            del gesammt_array_fur_xor[:64]



        if padding_zu_entfernen == True:
            output_plaintext_aray = output_plaintext_aray[::-1]
            index_counter_zum_entfernen = 0
            for i in output_plaintext_aray:
                if i == 0:
                    index_counter_zum_entfernen += 1
                if i == 1:
                    index_counter_zum_entfernen += 1
                    break
            output_plaintext_aray = output_plaintext_aray[::-1]
            output_plaintext_aray = output_plaintext_aray[:-index_counter_zum_entfernen]

        return output_plaintext_aray

