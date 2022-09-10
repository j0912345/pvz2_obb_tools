# for getting a bool val from input()
def get_bool_val(v: str, perferance=False):
    iv = bool(int(v))
    if iv == (not perferance):
        return not perferance
    else:
        return perferance