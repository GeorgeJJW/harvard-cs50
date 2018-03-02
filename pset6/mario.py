def main():
    
    # ask user for height variable
    h = int(input("Height: "))
    
    # ensure proper height input, such that 0 < h < 23
    while (h < 0 or h > 23):
        h = int(input("Height: "))
        
    # draw pyramid
    draw(h)

# define draw function
def draw(n):
    for i in range(1, n + 1, 1):
        padding(n - i)
        pyramid(i)
        space()
        pyramid(i)
        print("\n", end="")
        
# define padding
def padding(n):
    for i in range(n, 0, -1):
        print(" ", end="")

# define pyramid hash blocks
def pyramid(n):
    for i in range(n):
        print("#", end="")
        
# define space
def space():
    print("  ", end="")
    
# initiate main function as default
if __name__ == "__main__":
    main()