import fnmatch
import os
import json

print("note: this script will rebuild the obb from scratch, you will need all to have all of your files in this directory")
files_to_pack_dir=r"D:\coding\python\pvz2_obb_tools\test_packing"#input("where is the folder of files you want to repack the obb with? ")
new_obb_location = "packed.obb"
header_len = 70
dir_list_start = 112
header_name = b'\x31\x62\x73\x72'
file_to_pack_list = []
unknown_value_takes_you_to_one_of_the_wems_in_the_dir_list = 450040#this is dif in fir obbs.
#offset list
header_pgsr_offset = 12

def seek_bytes_forward(bytes_to_skip, input_file_name):
    input_file_name.seek(bytes_to_skip + input_file_name.tell())
    

def get_files_in_dir(file_dir, extension=".rsgp"):
    file_to_pack_list = []
    #https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory#comment7714652_3215392
    for file in os.listdir(file_dir):
        if fnmatch.fnmatch(file, '*'+extension):
            file_to_pack_list.append(file)
    return(file_to_pack_list)

def build_basic_header_info(file_name):
    file_name.write(bytes(header_len))
    file_name.seek(0)
    file_name.write(bytes(header_name))
    seek_bytes_forward(8, file_name)
    file_name.write(bytes("PGSR", "utf-8"))# this is a placeholder that gets filled later
    file_name.write((unknown_value_takes_you_to_one_of_the_wems_in_the_dir_list).to_bytes(4, byteorder='little'))
    file_name.write((dir_list_start).to_bytes(4, byteorder='little'))
    seek_bytes_forward(8, file_name)

with open(new_obb_location, "wb") as new_obb:
    file_to_pack_list = get_files_in_dir(files_to_pack_dir, "*")
#    print(file_to_pack_list)
    build_basic_header_info(new_obb)

