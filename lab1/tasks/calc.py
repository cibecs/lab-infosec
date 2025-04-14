from itertools import product

def count_keys_with_total_distance(d, n=8, max_d=5):
    count = 0
    for delta in product(range(max_d+1), repeat=n):
        if sum(delta) == d:
            variations = 1
            for val in delta:
                if val > 0:
                    variations *= 2  # ±delta
            count += variations
    return count
print("Total keys with total distance 13:", count_keys_with_total_distance(1)+count_keys_with_total_distance(2)+count_keys_with_total_distance(3)+count_keys_with_total_distance(4)+count_keys_with_total_distance(5)+count_keys_with_total_distance(6)+count_keys_with_total_distance(7)+count_keys_with_total_distance(8)+count_keys_with_total_distance(9)+count_keys_with_total_distance(10)+count_keys_with_total_distance(11)+count_keys_with_total_distance(12)+count_keys_with_total_distance(13))