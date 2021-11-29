def convert_data_to_uint(var_name, offset_to_read_from, opened_file_name):
    import numpy as np
    opened_file_name.seek(offset_to_read_from)
    var_name=opened_file_name.read(4)
    var_name=np.frombuffer(var_name, dtype=np.uint32)
    var_name=int(var_name)
    return(var_name)
