s = "dhruv chauhan"
print("Character | Positive Index | Negative Index")
print("-" * 40)
for i in range(len(s)):
    print(f"    {s[i]}     |       {i:2d}       |       {i-len(s):3d}")