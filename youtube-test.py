import os  

for directory_Element in os.listdir(r"./"):
    if directory_Element.endswith(".m4a"):
        oldName = directory_Element
        #newName = directory_Element.split("[")[0].strip() + ".m4a"
        #newName = directory_Element.split("(")[0].strip() + ".m4a"
        #os.rename(oldName,newName)
        #print(oldName, "\n", newName,  "\n")
        newName = directory_Element.split("[")[0].split("(")[0].strip() + ".m4a"
#os.rename('guru99.txt','career.guru99.txt')