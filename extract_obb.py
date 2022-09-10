import json
import time
import extract_file_names # this is one of my scripts, not a module
from func_table import * # same, this is one of my scripts
from time import sleep
#                                                   this was made in python 3.10
#               ==== setup values ====
InputObbDir=input("where is your obb that you want to extract: ")#"main.621.com.ea.game.pvz2_wha.obb"
OutputObbDir=input(r"where should the obb be exrtacted: ")#"D:\coding\python\pvz2_obb_tools\zzzz_dumped_files\\"
DontReadpgsrHead=get_bool_val(input("(for datamining) should the program ignore rspg/pgsr headers? (0 or 1, 0 is faster)"))
print(DontReadpgsrHead)
first_file_offset_offset=12
first_file_offset="gets read in the obb as uint"
next_pgsr_offset_offset=40
next_pgsr_data_offset="not set yet"
this_pgsr_start_offset="not set yet"
pgsr_data_size="not set yet"
list_pos=0
file_type=".rsgp"
#               ==== start of the script ====

has_json_file_names = input("do you have a json list of file names? (y/n)")#dumped_file_names.json
if has_json_file_names == "y":
    user_json_dir=input("where is the json file name list: ")
elif has_json_file_names == "n":
    print("\nthat's fine, i can make one for you")
    json_file_name_dir=input("where should the list of file names be saved (with the file's name): ")
    print("")
    extract_file_names.make_json_file_name_list(InputObbDir = InputObbDir, OutputJsonDir = json_file_name_dir)
    user_json_dir=json_file_name_dir

start_time = time.time()
with open(user_json_dir, "r") as file_name_list:# get file names + remove note made by my tool if it's there
    file_names=json.loads(file_name_list.read())
    if file_names[0] == "*** this list of file names was dumped by j0's pvz2 obb decryption tool ***":
        del file_names[0]

#                   from my data mining notes:
#   next pgsr offset is at current pgsr offset + 44 + where the file data starts 
#   file data offset offset is at 40 + start of the current pgsr header offset

def convert_data_to_32_bit_uint(var_name, offset_to_read_from, opened_file_name):
#    import numpy as np
    opened_file_name.seek(offset_to_read_from)
    var_name=opened_file_name.read(4)
    var_name = int.from_bytes(var_name, "little", signed=False)
    return(var_name)

def go_to_offset_from_current_offset(offset, opened_file_name):
    opened_file_name.seek(opened_file_name.tell()+offset)
def do_X_backspaces(x):
    bstr = ""
    for x in range(0, x):
        bstr = bstr+"\b"
    print(bstr, end="")
        

with open(InputObbDir, "rb") as obb:
    first_file_offset = convert_data_to_32_bit_uint(first_file_offset, first_file_offset_offset, obb)
    print("offset of the file headers is at: "+str(first_file_offset))
    obb.seek(first_file_offset)
    #loop 1, read the header data then start loop 2, write the file data
    print("extracting files, this may take a bit...\n")
    fnameLEN = len(file_names)
    i = -1
    for files in range(0, fnameLEN):
        i += 1
        #print(obb.tell())
        this_pgsr_start_offset = obb.tell()
        go_to_offset_from_current_offset(next_pgsr_offset_offset, obb)
        next_pgsr_data_offset = convert_data_to_32_bit_uint(next_pgsr_data_offset, obb.tell(), obb)
        #get file size
        pgsr_data_size = convert_data_to_32_bit_uint(pgsr_data_size, obb.tell(), obb)
        #setup for loop 2
        obb.seek(this_pgsr_start_offset)
        with open(OutputObbDir+file_names[list_pos]+file_type, "w+b") as current_file:
#            for data in range(0, pgsr_data_size+next_pgsr_data_offset):
            current_file.write(obb.read(pgsr_data_size+next_pgsr_data_offset))
            current_file.close()
        list_pos=list_pos+1

#        print(i)

print("the pgsr files have been exrtacted successfully! extract time: "+str(round(time.time() - start_time, 2)))
input("press enter to exit")
