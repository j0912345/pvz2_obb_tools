import helpful_functions # one of my scripts, not a module 
from func_table import add_extra_slash_to_dir_str
import os

def unpack_rsgp_dir(extra_messages=False):
    import zlib

    current_file_name = input(r"where is the .rsgp file (aka pgsr file) you want to unpack: ")
    global output_file_name
    output_file_name = add_extra_slash_to_dir_str(input(r"where do you want to unpack the .rsgp (aka pgsr) file: "))#r"D:\coding\python\pvz2_obb_tools\zz_testing\test_output\\"
    offset_offset="not set"
    file_offset=20 # 40 also works but only sometimes idk it's werid
    start_of_path_offset_offset=76 # this could be 1000% wrong for other files
    start_of_path_offset="not set yet"
    file_name_in_header="not set yet"
    print("unpacking rsgp (aka pgsr)...")

    with open(current_file_name, "rb") as pgsr:
        file_name_in_header = extract_header_data(pgsr, start_of_path_offset, start_of_path_offset_offset, current_file_name)
        output_file_name = output_file_name + file_name_in_header
        offset_offset=helpful_functions.convert_data_to_uint(offset_offset, file_offset, pgsr)
        pgsr.seek(offset_offset)

        fd = pgsr.read(4)
        pgsr.seek(pgsr.tell()-4)
        print(fd)
        print(offset_offset)
        if fd == b"RTON":
            print("the file isn't compressed, just a raw rton")
            with open(output_file_name, "w+b") as output_file:
                output_file.write(pgsr.read(os.path.getsize(current_file_name)-offset_offset))
        else:
            compressed_data = pgsr.read(os.path.getsize(current_file_name)-offset_offset) 
            zobj = zlib.decompress(compressed_data)

            with open(output_file_name, "w+b") as output_file:
                output_file.write(zobj)
                
    if extra_messages:
        print("extracted the pgsr file(s)")
        input("press enter to exit")

def extract_header_data(file_location, start_of_path_offset, start_of_path_offset_offset, current_file_name):
    passed_backslash=False
#        with open(current_file_name, "rb")
    global temp_byte_read
    file_name_in_header=b""
    path_offset=helpful_functions.convert_data_to_uint(start_of_path_offset, start_of_path_offset_offset, file_location)
    file_location.seek(path_offset)
#        print(path_offset)
    for byte in range(0, os.path.getsize(current_file_name)):
            temp_byte_read=file_location.read(1)
            if temp_byte_read == b'\x00':
                file_name_in_header=str(file_name_in_header, encoding="ascii")
                print("found file name: "+file_name_in_header)
                return(file_name_in_header)
            else:
                helpful_functions.go_to_offset_from_current_offset(3, file_location)
                if passed_backslash == True:
                    file_name_in_header=file_name_in_header + temp_byte_read

                if str.find(str(temp_byte_read, encoding="ascii"), "\\") != -1:
                    passed_backslash=True

if __name__ == '__main__':
    unpack_rsgp_dir(extra_messages=True)
