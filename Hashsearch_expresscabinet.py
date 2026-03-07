hash_table = [[] for _ in range(10)]

def hash_function(express_num):
    return int(str(express_num)[-1])
def store_express(express_num):
    cabinet_num = hash_function(express_num)
    hash_table[cabinet_num].append(express_num)
def find_express(target_num):
    cabinet_num = hash_function(target_num)
    cabinet = hash_table[cabinet_num]
    for num in cabinet:
        if num == target_num:
            return f"finded！express is in{cabinet_num}cabinet，express_number：{target_num}"
    return "no express found"

store_express(87654)   
store_express(12399)   
store_express(55554)   


print(find_express(55554))  
print(find_express(12399))  
print(find_express(11111))  
