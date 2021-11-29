def make_json_file_name_list(InputObbDir, OutputJsonDir, extra_messages=False):        
        import os
        import numpy as np
        import json
                                                                                # this program was made in python 3.10
        if extra_messages == True:
                print("\nthanks to the pvz2 quickbms script version 0.2.2\nfor helping me learn how the obb works\n")

        #setup first values
        FirstAutoPoolOffsetOffset=56
        FirstFileOffsetOffset=44
        LoopOffsetOffset=76#offset of the 32 bit int that has the offset of "key thing"
        AutoPoolOffsetOfOtherAutoPoolOffsets=80
        FirstFileOffset="NOT_SET" #first offset of encrypted file data
        FirstAutoPoolOffset="NOT_SET" #first offset of auto pool data
        encrypted_header_offsets=['*** this list of file names was dumped by j0\'s pvz2 obb decryption tool ***']
        encrypted_header_temp_string=""
        last_auto_pool_name="__MANIFESTGROUP___AutoPool"
        current_list_item=1 # the first 2 items have the note for the json

        if extra_messages == True:
                print("reading file...\n")
        with open(InputObbDir, "rb") as encrypted_obb:
            #get position of the first pgsr file header
            encrypted_obb.seek(FirstFileOffsetOffset)
            FirstFileOffset=encrypted_obb.read(4)
            #convert read data to 32 bit int
            FirstFileOffset=np.frombuffer(FirstFileOffset, dtype=np.uint32)
            #convert the position into an int
            FirstFileOffset=int(FirstFileOffset)
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
                                break
                        encrypted_header_offsets.append(encrypted_header_temp_string.replace("_AutoPool", "")) # remove the extra autopool to only get the file name
                        encrypted_obb.seek(encrypted_obb.tell()+AutoPoolOffsetOfOtherAutoPoolOffsets-len(encrypted_header_temp_string)) #set read offset to (read offset + the 32 bit int at 0x50 in encrypted_obb) - length of file size.
                        encrypted_header_temp_string=""
        #
            with open(OutputJsonDir, "w+") as loop_1_json_dump:
                    print("dumping file names to json file...")
                    loop_1_json_dump.write(json.dumps(encrypted_header_offsets, indent=4))
        print("done!\n")
        if extra_messages == True:
                print("the file names have been dumped")
                input("press enter to exit")

if __name__ == '__main__':
    make_json_file_name_list(input("where is the location of the obb: "), input("what is the location you want to save the json list of file names: "), True)
