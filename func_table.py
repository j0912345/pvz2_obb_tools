global free_program_message_shown
free_program_message_shown = False
if not free_program_message_shown:
    print("\nthis program is free under the gpl-3 license. if you paid for this, you got scammed.\nhttps://github.com/j0912345/pvz2_obb_tools\n")
free_program_message_shown = True

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
    passed_backslash = False
    file_name_in_header = b""
    folder_name = b""
    for byte in range(0, os.path.getsize(current_file_name)):
            temp_byte_read=f.read(1)
            if temp_byte_read == b'\x00':
                file_name_in_header = str(file_name_in_header, encoding="ascii")
                print("found file name: "+file_name_in_header)
                return [file_name_in_header, str(folder_name, encoding="ascii")]
            else:
                # so it looks like the 24 bit (3 byte) int inbtween each letter in the file names (i.e. A(0x00,0x00,0x00)B) point to the extenctions (.rton/whatever)
                # of random files in the list. why? -\(:->)/-
                f.seek(f.tell()+3)
                if passed_backslash == True:
                    file_name_in_header=file_name_in_header + temp_byte_read
                else:
                    folder_name = folder_name+temp_byte_read

                if str(temp_byte_read, encoding="ascii") == "\\":
                    print("backslash")
                    passed_backslash=True