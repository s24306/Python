import math
import sys
import argparse



def calculate_months():
    nominal_i_r = credit_i
    number_o_m = math.ceil(math.log((annuity_m_p / (annuity_m_p - nominal_i_r * c_p)), (1 + nominal_i_r)))
    if number_o_m == 1:
        print("You need 1 month to repay this credit!")
    elif 12 > number_o_m > 1:
        print(f"You need {number_o_m} months to repay this credit!")
    else:
        years = number_o_m // 12
        leftover_months = number_o_m % 12
        if leftover_months != 0:
            if years > 1:
                if leftover_months > 1:
                    print(f"You need {years} years and {leftover_months} months to repay this credit!")
                else:
                    print(f"You need {years} years and {leftover_months} month to repay this credit!")
            else:
                print(f"You need {years} year to repay this credit!")
        else:
            print(f"You need {years} years to repay this credit!")
    overall = (number_o_m * annuity_m_p) - c_p
    print(f"Overpayment =  {overall}")
            
def calculate_annuity_payment():
    annuity_m_p = c_p * ((credit_i * ((1 + credit_i) ** number_o_m)) / (((1 + credit_i) ** number_o_m) - 1))
    print(f"Your annuity payment = {math.ceil(annuity_m_p)}!")

def calculate_credit_principal():
    c_p = annuity_m_p / (((credit_i * (1 + credit_i) ** number_o_m)) / ((1 + credit_i) ** number_o_m - 1))
    print(f"Your credit principal = {round(c_p)}!")

def calculate_differentiated_payment():
    i = 0
    overall = 0
    while i < number_o_m:
        i += 1
        differentiated_payment = math.ceil(float((c_p / number_o_m) + credit_i * (c_p - (c_p * (i - 1)) / number_o_m)))
        overall += differentiated_payment
        print(f"Month {i}: paid out {differentiated_payment}")
    print(f"Overpayment = {overall - c_p}")

parser = argparse.ArgumentParser()
parser.add_argument('--type', type=str, help="increase output verbosity")
parser.add_argument('--principal', type=int, help="increase output verbosity", default=0)
parser.add_argument('--payment', type=int, help="increase output verbosity", default=0)
parser.add_argument('--periods', type=int, help="increase output verbosity", default=0)
parser.add_argument('--interest', type=float, help="increase output verbosity", default=0.0)
args = parser.parse_args()

c_p = args.principal
number_o_m = args.periods
credit_i = args.interest / 1200
annuity_m_p = args.payment
command = args.type

if command == 'diff':
    if (c_p or number_o_m or credit_i) < 0:
        print("Incorrect parameters.")
    else:
        calculate_differentiated_payment()
elif command == 'annuity':
    if credit_i == 0.0:
        print("Incorrect parameters.")
    elif c_p is 0:
        calculate_credit_principal()
    elif number_o_m is 0:
        calculate_months()
    elif annuity_m_p is 0:
        calculate_annuity_payment()
else:
    print("Incorrect parameters.")