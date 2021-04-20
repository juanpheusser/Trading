p = 1000
number_of_digits_to_check = 3
prime_numbers = [2]
for i in range(3, p):
    is_prime = True
    for number in prime_numbers:
        if i % number == 0:
            is_prime = False

    if is_prime:
        prime_numbers.append(i)

number = input('Ingrese un numero: ')

primes_in_number = []

for i in range(len(number)):
    for j in range(1, number_of_digits_to_check + 1):
        check_num = number[i: i + j]
        if int(check_num) in prime_numbers:
            primes_in_number.append(check_num)

primes_in_number = set(primes_in_number)
print(len(primes_in_number))