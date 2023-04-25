
# def decorate(func):
#     def wrapper(a):
#         print(a * 5)
#         #func(a)
#     return wrapper

# @decorate # test = decorate(test)
# def test(a):
#     x =
#     print(f"Основная функция a = {a}")


# test("b")

def dec(func):
    def wrapper(*args, **kwargs):
        original_result = func(*args, **kwargs)
        modified_result = original_result * 100
        return modified_result
    return wrapper

@dec
def sum(a, b):
    return a + b # sum = dec(sum)

print(sum(1, 2))

# sum = dec(sum)
# print(sum((1, 2)))








#print("Основная функция x = a + b = ", test(1, 2))
