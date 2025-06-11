# Exercise 1

# Point 1
print('sum of strings')
sum_strings = "Hello" + "world"
print(sum_strings) 
# result: Helloworld


#Point 2
print('sum of string and int')
sum_string_int = "Hello" + 3
print(sum_string_int)
# result: Error, can't add string and int together



#Point 3
print('sum of int and string')
sum_int_string = 3 + "Hello"
print(sum_int_string)
# result: Error, can't add int and string together


#Point 4
print('sum of arrays')
sum_arrays = [1, 2, 3, 4] + [1, 2, 3]
print(sum_arrays)
# result: [1, 2, 3, 4, 1, 2, 3]


#Point 5
print('sum of string and array')
sum_string_array = "Hello" + [1, 2, 3]
print(sum_string_array)
# result: Error, can't add string and array together

#Point 6
print('sum of float and int')
sum_float_int = 3.5 + 3
print(sum_float_int)
# result: 6.5

#Point 7
print('sum de booleans')
sum_boolean = True + True + False
print(sum_boolean)
# result: 2 because true is 1 and false is 0