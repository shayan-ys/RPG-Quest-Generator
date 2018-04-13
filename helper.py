from actions import T


def list_to_str(actions_flatten: list) -> str:
    flt_str_list = []
    for flt in actions_flatten:
        flt_str_list.append(flt.name if type(flt) == T else "<" + flt.name + ">")

    return ", ".join(flt_str_list)
