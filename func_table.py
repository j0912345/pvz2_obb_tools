# for getting a bool val from input()
def get_bool_val(v: str, perferance=False):
    iv = bool(int(v))
    if iv == (not perferance):
        return not perferance
    else:
        return perferance
def add_extra_slash_to_dir_str(s: str):
    if s[-1] != "/":
        s = s + "/"
    return s


def read_dir_list(f):
    import os
    current_file_name = f.name
    datalist = {}
    for byte in range(0, os.path.getsize(current_file_name)):
            temp_byte_read=f.read(1)
            if temp_byte_read == b'\x00':
                file_name_in_header=str(file_name_in_header, encoding="ascii")
                print("found file name: "+file_name_in_header)
                return(datalist[2][file_name_in_header])
            else:
                # i don't know why they appear to have a 27 bit (3 byte) int inbtween each letter in the file name. (i.e. A(0x00,0x00,0x00)B)
                # (in pgsrs it's usualy just empty space but not in the obb so I'll keep the value)
                f.read(3)
                if passed_backslash == True:
                    file_name_in_header=file_name_in_header + temp_byte_read

                if str.find(str(temp_byte_read, encoding="ascii"), "\\") != -1:
                    passed_backslash=True