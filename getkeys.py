# # Citation: Box Of Hats (https://github.com/Box-Of-Hats )
# 
# import win32api as wapi
# 
# keyList = ["\b"]
# for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
#     keyList.append(char)
# 
# def key_check():
#     keys = []
#     for key in keyList:
#         if wapi.GetAsyncKeyState(ord(key)):
#             keys.append(key)
#     return keys
# 
import keyboard as kb
# while True:
def key_check():
    key_list = []
    key = kb.get_hotkey_name()
    if key:
        key_list.append(key)
        key_list = list(set(key_list))
    return key_list