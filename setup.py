from distutils.core import setup
import py2exe

setup(console=['extract_obb.py', 'extract_file_names.py', 'convert_data_from_file_to_32_bit_uint.py'])
