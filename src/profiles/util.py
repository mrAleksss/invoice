import random


size = 26
available_numbers = [x for x in range(10)]

def generate_account_number():
            new_number_list = [str(random.choice(available_numbers)) for _ in range(size)]
            new_number_str = "".join(new_number_list)
          
            return new_number_str