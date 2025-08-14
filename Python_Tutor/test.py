name = '我今年3歲'
name_bytes = name.encode('utf-8')
print(name_bytes)

# -----------------------

tt = name_bytes.decode('utf-8')


print(tt)
# print(name_bytes)         # b'\xe6\x88\x91\xe4\xbb\x8a\xe5\xb9\xb43\xe6\xad\xb2'
# print(len(name_bytes))    # 13
