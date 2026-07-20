inputFile = input("Pathname of Input File:  ")
outputFile = input("Pathname of Output file:  ")
with open(inputFile, "r") as infile, open(outputFile, "w") as outfile:
    curr_entry = ""
    for line in infile:
        if "AC=" in line:
            if curr_entry and "AC=" in curr_entry:
                ac_val = curr_entry.split("AC=")[1].split(";")[0]
                if ac_val.isdigit() and int(ac_val) >= 10:
                    outfile.write(curr_entry)
            curr_entry = line
        else:
            curr_entry += line
    #final entry
    if curr_entry and "AC=" in curr_entry:
        ac_val = curr_entry.split("AC=")[1].split(";")[0]
        if ac_val.isdigit() and int(ac_val) >= 10:
            outfile.write(curr_entry)

print("Sorting done!")
