def swap_odd_even_bits(n):
    odd_bits = n & 0xAAAAAAAA  # 奇數位
    even_bits = n & 0x55555555  # 偶數位
    odd_bits >>= 1  # 奇數位右移
    even_bits <<= 1  # 偶數位左移
    return odd_bits | even_bits  # 合併結果

n = int(input())
print(swap_odd_even_bits(n))