from committee import Committee
import getopt, sys

if __name__ == '__main__':

    iterations = 1
    rounds = 100
    k = 3
    m = 0
    fr = 0.3
    frmax = 5
    size = 100
    greedyMode = True
    simType = "Freeriding"

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

    counts = []
    for k in range(2, 4):
        sumItr = 0
        for itr in range(iterations):
            count = 0
            for i in range(rounds):
                print(str(k) +"-" + str(itr) +"-"+ str(i))
                committee = Committee(size, m, fr, frmax, k, greedyMode, simType)
                canExtract = committee.start()
                if simType == "Byzantine":
                    if canExtract:
                        count += 1
                elif simType == "Freeriding":
                    count += canExtract
                print(canExtract)

            print(count)
            sumItr += count
        counts.append(sumItr / iterations)

    print(counts)

