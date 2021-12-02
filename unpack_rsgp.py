def unpack_rsgp_dir(json_dir, extra_messages=False):
    import zlib
    import helpful_functions # one of my scripts, not a module 
    import os
    import json


    with open(json_dir, "r") as json_file_list:
        file_name_list=json.loads(json_file_list.read())
    current_file_name = input(r"where is the .rsgp file (aka pgsr file) you want to unpack: ")
    temp_file_name="temp_file_with_header_removed.zlib"
    global output_file_name
    output_file_name = input(r"where do you want to unpack the .rsgp (aka pgsr) file: ")#r"D:\coding\python\pvz2_obb_tools\zz_testing\test_output\\"
    offset_offset="not set"
    file_offset=40 # maybe wrong in other people's files
    image_size_1_offset=248 # same with this one.
    image_size_2_offset=248 + 4 # same with this one.
    start_of_path_offset_offset=76 # this could be 1000% wrong for other files
    start_of_path_offset="not set yet"
    file_name_in_header="not set yet"
    print("unpacking rsgp (aka pgsr)...")

    def extract_header_data(file_location):
        passed_backslash=False
#        with open(current_file_name, "rb")
        global temp_byte_read
        file_name_in_header=b""
        path_offset=helpful_functions.convert_data_to_uint(start_of_path_offset, start_of_path_offset_offset, pgsr)
        file_location.seek(path_offset)
#        print(path_offset)
        for byte in range(0, os.path.getsize(current_file_name)):
                temp_byte_read=file_location.read(1)
                if temp_byte_read == b'\x00':
                    file_name_in_header=str(file_name_in_header, encoding="ascii")
                    print("found file name: "+file_name_in_header)
                    return(file_name_in_header)
                    break
                else:
                    helpful_functions.go_to_offset_from_current_offset(3, file_location)
                    if passed_backslash == True:
                        file_name_in_header=file_name_in_header + temp_byte_read

                    if str.find(str(temp_byte_read, encoding="ascii"), "\\") != -1:
                        passed_backslash=True


    with open(current_file_name, "rb") as pgsr:
        file_name_in_header = extract_header_data(pgsr)
        output_file_name = output_file_name + file_name_in_header
        offset_offset=helpful_functions.convert_data_to_uint(offset_offset, file_offset, pgsr)
        pgsr.seek(offset_offset)
        with open(temp_file_name, "w+b") as temp:
            for x in range(0, os.path.getsize(current_file_name)-offset_offset):
                temp.write(pgsr.read(1))
    #       === decompress data ===
        with open(temp_file_name, "r+b") as temp:
            zobj = zlib.decompress(temp.read())
            with open(output_file_name, "w+b") as output_file:
                output_file.write(zobj)
    os.remove(temp_file_name)
    if extra_messages:
        print("extracted the pgsr file(s)")
        input("press enter to exit")

if __name__ == '__main__':
    unpack_rsgp_dir(json_dir=input(r"where is the json file name list (use extract_file_names.py if you don't have one): "), extra_messages=True)
