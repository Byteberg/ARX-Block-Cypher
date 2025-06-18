import blockcypher

Text = "test1"
pw = "password"
blockcypher = blockcypher.block_cypher_parts()
pw_array_liste = blockcypher.pw_list_gen(pw)
first_block = blockcypher.get_rand_bytearray(512)
cyphertext = blockcypher.cbc_mode_cypher_verschlüsseln(bytearray(Text,"UTF-8"),first_block,True,blockcypher.pw_array_liste)
print(cyphertext)
plaintext = blockcypher.cbc_mode_cypher_entschlüsseln(cyphertext,first_block,blockcypher.pw_array_liste,True)
print(plaintext)