def nb_nodes (n):
    if n == 0:
        return 1
    return sum(nb_nodes(i) * nb_nodes(n-1-i) for i in range(0,n) )

def main ():
    print("Number of possible configurations with 5 nodes is ", nb_nodes(5))
    print("Number of possible configurations for 0 to 10 nodes:")
    for i in range(0,10):
        print(i, " : ", nb_nodes(i))

if __name__ == "__main__":
    main()
