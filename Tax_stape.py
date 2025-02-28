import numpy as np
import matplotlib.pyplot as plt

# Rate of tax brackets 
tax_brackets = {
    7010: 0.1,
    10060: 0.14,
    16150: 0.20,
    22440: 0.31,
    46690: 0.35,
    100000: 0.47,
}

def calculate_tax(income: float) -> tuple:
    """
    this function calculates the tax paid and the net income
    :param income: the gross income
    :return: a tuple of the tax paid and the net income
    """
    tax_paid = 0
    prev_limit = 0  

    # ממיין את מדרגות המס ומחשב אותן בצורה תקינה
    for limit, rate in sorted(tax_brackets.items()):
        if income < limit:
            tax_paid += (income - prev_limit) * rate
            break
        else:
            tax_paid += (limit - prev_limit) * rate
            prev_limit = limit

    net_income = income - tax_paid
    return tax_paid, net_income

def main():
    """
    this function calculates the tax paid and the net income for a range of incomes
    and plots the results
    """
    total_income = np.arange(0, 50000, 1)


    # create a vectorized version of the function
    calculate_tax_vectorized = np.vectorize(calculate_tax)
    # calculate the tax and net income for the range of incomes
    tax, pure_income = calculate_tax_vectorized(total_income)

    # plot the results
    plt.figure(figsize=(10, 5))
    plt.plot(total_income, tax, label='Tax Paid', color='red')
    plt.plot(total_income, pure_income, label='Net Income', color='green')
    plt.xlabel("Gross Income")
    plt.ylabel("Amount")
    plt.title("Income vs Tax & Net Income")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
