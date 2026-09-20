#text file work
def encrypt(input_file, output_file, key):
    smallstring = "abcdefghijklmnopqrstuvwxyz"
    capstring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    keypoint=0
    with open(input_file,"r") as readtxtfile:
        with open(output_file,"w") as writetxtfile:
            for line in readtxtfile:
                writeline=""
                for letter in line:
                    if letter in smallstring:
                        letterindex=smallstring.index(letter)
                        keyindex=smallstring.index(key[keypoint])
                        keypoint+=1
                        keypoint=keypoint%len(key)
                        mainindex=(letterindex+keyindex)%26
                        writeline+=smallstring[mainindex]
                    elif letter in capstring:
                        letterindex=capstring.index(letter)
                        keyindex=smallstring.index(key[keypoint])
                        keypoint+=1
                        keypoint=keypoint%len(key)
                        mainindex=(letterindex+keyindex)%26
                        writeline+=capstring[mainindex]
                    else:
                        writeline+=letter
                writetxtfile.write(writeline)
                        
def decrypt(input_file, output_file, key):
    smallstring = "abcdefghijklmnopqrstuvwxyz"
    capstring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    keypoint=0
    with open(input_file,"r") as readtxtfile:
        with open(output_file,"w") as writetxtfile:
            for line in readtxtfile:
                writeline=""
                for letter in line:
                    if letter in smallstring:
                        letterindex=smallstring.index(letter)
                        keyindex=smallstring.index(key[keypoint])
                        keypoint+=1
                        keypoint=keypoint%len(key)
                        mainindex=(letterindex-keyindex)%26
                        writeline+=smallstring[mainindex]
                    elif letter in capstring:
                        letterindex=capstring.index(letter)
                        keyindex=smallstring.index(key[keypoint])
                        keypoint+=1
                        keypoint=keypoint%len(key)
                        mainindex=(letterindex-keyindex)%26
                        writeline+=capstring[mainindex]
                    else:
                        writeline+=letter
                writetxtfile.write(writeline)

#encrypt/decrypt non-text file
def encrypt_binary(input_file, output_file, key):
    keylen=len(key)
    key=key.encode()
    keyindex=0
    with open(input_file,"rb") as readbinfile:
        with open(output_file,"wb") as writebinfile:
            fdata=readbinfile.read()
            for byte in fdata:
                writebinfile.write(bytes([byte ^ key[keyindex]]))
                keyindex+=1
                keyindex=keyindex%keylen


def decrypt_binary(input_file, output_file, key):
    keylen=len(key)
    key=key.encode()
    keyindex=0
    with open(input_file,"rb") as readbinfile:
        with open(output_file,"wb") as writebinfile:
            fdata=readbinfile.read()
            for byte in fdata:
                writebinfile.write(bytes([byte ^ key[keyindex]]))
                keyindex+=1
                keyindex=keyindex%keylen


text_or_non_text = input("Enter file type: text file [T] or non-text file [N]: ")
EorD = input("For encrypt [E] or decrypt [D]: ")

if text_or_non_text.upper() == "T":
    input_file = input("Enter input file: ")
    output_file = input("Enter output file: ")
    key = input("Enter key: ")

    if EorD.upper() == "E":
        encrypt(input_file, output_file, key)
    elif EorD.upper() == "D":
        decrypt(input_file, output_file, key)
    else:
        print("Invalid choice")

elif text_or_non_text.upper() == "N":
    input_file = input("Enter input file: ")
    output_file = input("Enter output file: ")
    key = input("Enter key: ")

    if EorD.upper() == "E":
        encrypt_binary(input_file, output_file, key)
    elif EorD.upper() == "D":
        decrypt_binary(input_file, output_file, key)
    else:
        print("Invalid choice")

else:
    print("Invalid file type")
