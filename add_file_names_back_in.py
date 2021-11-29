def reinsert_filenames():
    import os
    import numpy as np
    import json
    import shutil
                                                                            # this program was made in python 3.10

    print("credits:\nthanks to the plants vs zombies 2 quickbms script version 0.2.2\nfor helping with finding the first offset for the pgsr headers of any pvz2 obb.\n")

    #input("WARNING!! this is may use a TON of ram to run!")
    InputObbDir=input("file location for input encrypted obb: ")
    OutputObbDir=input("file location for output decrypted obb: ")

    #setup first values
    dump_found_offsets_to_json=1
    FirstAutoPoolOffsetOffset=56
    FirstFileOffsetOffset=44
    OffsetOfNextKeyThing=76                 #this WILL break if it's not 100% correct 
    LoopOffsetOffset=76#offset of the 32 bit int that has the offset of "key thing"
    AutoPoolOffsetOfOtherAutoPoolOffsets=80
    FirstFileOffset="NOT_SET" #first offset of encrypted file data
    FirstAutoPoolOffset="NOT_SET" #first offset of auto pool data
    encrypted_header_offsets=['*** this list of file names was dumped by j0\'s pvz2 obb decryption tool ***']
    encrypted_header_temp_string=""
    last_auto_pool_name="__MANIFESTGROUP___AutoPool"
    current_list_item=1 # the first 2 items have the note for the json

    with open(InputObbDir, "rb") as encrypted_obb:
        #get position of the first pgsr file header
        encrypted_obb.seek(FirstFileOffsetOffset)
        FirstFileOffset=encrypted_obb.read(4)
        #convert read data to 32 bit int
        FirstFileOffset=np.frombuffer(FirstFileOffset, dtype=np.uint32)
        #convert the position into an int
        FirstFileOffset=int(FirstFileOffset)
        print("found start of the pgsr header offsets at: "+str(FirstFileOffset))
        #get current 128 length string
        encrypted_obb.seek(FirstFileOffset)
        key_thing=encrypted_obb.read(128)
        key_thing=key_thing.decode("ascii")
        #get file names
        #get the position of header
        encrypted_obb.seek(FirstAutoPoolOffsetOffset)
        FirstAutoPoolOffset=encrypted_obb.read(4)
        FirstAutoPoolOffset=np.frombuffer(FirstAutoPoolOffset, dtype=np.uint32)
        FirstAutoPoolOffset=int(FirstAutoPoolOffset)
        #start the read loop
        #setup values for loop 1
        encrypted_obb.seek(AutoPoolOffsetOfOtherAutoPoolOffsets)
        AutoPoolOffsetOfOtherAutoPoolOffsets=encrypted_obb.read(4)
        AutoPoolOffsetOfOtherAutoPoolOffsets=int(np.frombuffer(AutoPoolOffsetOfOtherAutoPoolOffsets, dtype=np.uint32))
        encrypted_obb.seek(LoopOffsetOffset)
        LoopOffset=encrypted_obb.read(4)
        LoopOffset=int(np.frombuffer(LoopOffset, dtype=np.uint32))
        encrypted_obb.seek(LoopOffset)
        for x in range(0, os.path.getsize(InputObbDir)):# loop 1, get all of the offsets of the encrypted headers
                encrypted_header_temp_string=encrypted_header_temp_string+encrypted_obb.read(1).decode('ascii')
                if str.find(encrypted_header_temp_string, "_AutoPool") != -1:
                    if str.find(encrypted_header_temp_string, last_auto_pool_name) != -1:
                            encrypted_header_offsets.append(encrypted_header_temp_string.replace("_AutoPool", ""))
                            print("\n***end of loop 1***\n")
                            break
                    encrypted_header_offsets.append(encrypted_header_temp_string.replace("_AutoPool", "")) # remove the extra autopool to only get the file name
                    encrypted_obb.seek(encrypted_obb.tell()+AutoPoolOffsetOfOtherAutoPoolOffsets-len(encrypted_header_temp_string)) #set read offset to (read offset + the 32 bit int at 0x50 in encrypted_obb) - length of file size.
                    encrypted_header_temp_string=""
#
        if dump_found_offsets_to_json == 1:
            with open("dumped_file_names.json", "w+") as loop_1_json_dump:
                    print("dumping file names list to json file...")
                    loop_1_json_dump.write(json.dumps(encrypted_header_offsets, indent=4))

        # setup things for loop 2.
        print("building decrypted file, this may take a bit...")
        shutil.copy(InputObbDir, OutputObbDir) #copy file
        with open(OutputObbDir, "r+b") as decrypted_obb:
                decrypted_obb.seek(FirstFileOffset-OffsetOfNextKeyThing)
                for x in range(0, os.path.getsize(OutputObbDir)): # loop 2
                        current_list_item=current_list_item+1
                        decrypted_obb.seek(decrypted_obb.tell()+OffsetOfNextKeyThing)
                        if decrypted_obb.tell() > FirstAutoPoolOffset and len(encrypted_header_offsets) > current_list_item:
                            decrypted_obb.write(bytes(encrypted_header_offsets[current_list_item], encoding='ascii'))
                            repeat_amount=128-len(encrypted_header_offsets[current_list_item])#+OffsetOfNextKeyThing  128 is the length of key thing. this may be broken in new encryption
                            for x in range(0, repeat_amount):
                                decrypted_obb.write(b'\x00')
                        else:
                            print("\n*** end of loop 2 ***\n")
                            break

    input("\npress enter to exit")


if __name__ == "__main__":
    reinsert_filenames()
