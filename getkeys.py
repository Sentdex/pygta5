import keyboard as kb

def key_check():
    key_list = []
    key = kb.get_hotkey_name()
    if key:
        key_list.append(key)
        key_list = list(set(key_list))
    return key_list