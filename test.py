def leading_zero(number):
    return f"{int(number):02d}"  # add a leading zero to the number if it is less than 10

for i in range(-15, 15):
    print(leading_zero(i))

