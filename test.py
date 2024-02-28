import re

# texts = """vlan batch 3 16 19 24 32 to 44 61 to 70 73 83 99 271 to 280"""
# # """vlan batch 341 to 350 900 920 to 921 925 927 1053 1253 1453 1518 to 1519 1522 to 1523
# # vlan batch 1653 1853 2001 2007 2009 2019 2025 2035 2040 2043
# # vlan batch 2050 2101 2104 2500 to 2502 2504 to 2506 2508 2514 2525 2560 2639
# # vlan batch 2892 2905 3003 to 3004 3006 3012 3015 3024 3181 to 3190 3229 3483
# # vlan batch 3506 3631 to 3632"""

# pat = re.compile(r'(\d+)(?:\s+to\s+(\d+))?')
# nums = pat.findall(texts)
# numbers = []
# for num in nums:
#     if num[1] == '':
#         numbers.append(int(num[0]))
#     else:
#         numbers.extend(range(int(num[0]), int(num[1])+1))

# print(numbers)

numbers = [3, 16, 19, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 73, 83, 99, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280]
# convert to "3 16 19 24 32 to 44 61 to 70 73 83 99 271 to 280"
ranges = []
start = numbers[0]
end = numbers[0]
for i in range(1, len(numbers)):
    if numbers[i] == numbers[i-1] + 1:
        end = numbers[i]
    else:
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start} to {end}")
        start = numbers[i]
        end = numbers[i]
if start == end:
    ranges.append(str(start))
else:
    ranges.append(f"{start} to {end}")
print(' '.join(ranges))

