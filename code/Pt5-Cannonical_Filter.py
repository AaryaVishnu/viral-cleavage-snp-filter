inputFile1 = input("Pathname of Input File (sorted list):   ")
inputFile2 = input("Pathname of Input File (protein numbers):   ")
outputFile = input("Pathname of Output File:  ")

with open(inputFile1, "r") as infile1, open(inputFile2, "r") as infile2, open(outputFile, "w") as outputfile:
    x = infile2.read().strip().split('--')
    protein_set = set(x)
    for line in infile1:
        first_part = line.split(',')[0].strip()
        
        if first_part in protein_set:
                outputfile.write(line)
           
        else:
            continue



print("Done")
