inputFile = input("Pathname of Input File:  ")
outputFile = input("Pathname of Output file:  ")

with open(inputFile, "r") as infile, open(outputFile, "w") as outfile:
    curr_entry = ""
    for line in infile:
        if "AC=" in line:
            # Check if previous entry contains 'missense'
            if "missense" in curr_entry:
                outfile.write(curr_entry)
            curr_entry = line  # Start a new entry
        else:
            curr_entry += line

    if "missense" in curr_entry:
        outfile.write(curr_entry)

print("Sorting done!")
