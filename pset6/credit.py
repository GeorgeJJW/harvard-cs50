def main():
    
    # obtain credit card number
    n = int(input("Number: "))
    
    # determine if the card number is valid
    validate(n)
    
    # determine the associated credit card company
    company(n)

# define validate function
def validate(n):
    
    sumcard = 0;
    
    i = 10
    while i <= n:
        one = ((n // i) % 10) * 2
        i *= 100
        
        j = 1
        while j <= one + 1:
            two = (one // j) % 10
            sumcard += two
            j *= 10
    
    k = 1
    while k <= n:
        three = ((n // k) % 10)
        sumcard += three
        k *= 100
    
    if ((int(sumcard) % 10) != 0):
        print("Invalid")
        
# define company function
def company(n):            
    # Amex
    if (n >= 340000000000000 and n < 1000000000000000):
        print("AMEX")
        
    # MasterCard
    elif (n >= 5100000000000000):
        print("MASTERCARD")
        
    # VISA
    elif (n >= 4000000000000 or n >= 4000000000000000):
        print("VISA")
        
# initiate main function
if __name__ == "__main__":
    main()