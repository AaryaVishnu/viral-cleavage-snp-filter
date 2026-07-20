inputFile = input("Pathname of Input File:  ")
outputFile = input("Pathname of Output file:  ")

with open(inputFile, "r") as infile, open(outputFile, "w") as outfile:
    curr_entry = ""
    for line in infile:
        if "AC=" in line:
            if curr_entry and "AC=" in curr_entry:
                fields = curr_entry.split("\t")
                if len(fields) > 6 and fields[6].strip() == "PASS":
                    outfile.write(curr_entry)
            curr_entry = line
        else:
            curr_entry += line

    
    if curr_entry and "AC=" in curr_entry:
        fields = curr_entry.split("\t")
        if len(fields) > 6 and fields[6].strip() == "PASS":
            outfile.write(curr_entry)

print("Sorting done!")
