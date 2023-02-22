from committee import Committee
import getopt, sys

if __name__ == '__main__':

    iterations = 100
    k = 3
    m = 0.2
    size = 10

    argumentList = sys.argv[1:]
    options = "i:s:m:k:"
    long_options = ["iterations=", "size=", "m=", "k="]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        for currentArgument, currentValue in arguments:

            if currentArgument in ("-i", "--iterations"):
                iterations = int(currentValue)

            elif currentArgument in ("-s", "--size"):
                size = int(currentValue)

            elif currentArgument in ("-m", "--m"):
                m = float(currentValue)

            elif currentArgument in ("-k", "--k"):
                k = int(currentValue)

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    count = 0
    for i in range(iterations):
        committee = Committee(size, m, k)
        canExtract = committee.start()
        if canExtract:
            count += 1
        print(canExtract)

    print(count)

