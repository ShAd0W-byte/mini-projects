import sys
import os
import os.path
import shutil
import hashlib

def scan_directory(path):
    mydict={}
    try:
        folderdata=os.listdir(path)
    except FileNotFoundError as e:
        print("enter the correct absolute folder path")
        sys.exit()
    for filename in folderdata:
        if os.path.isfile(os.path.join(path, filename)):
            fileformat=filename.split(".")[-1]
            if fileformat in mydict:
                mydict[fileformat].append(filename)
            elif fileformat not in mydict:
                mydict[fileformat]=[filename]
    return mydict


def organise(path):
    os.mkdir(os.path.join(path, "Images"))
    os.mkdir(os.path.join(path, "Documents"))
    os.mkdir(os.path.join(path, "Videos"))
    os.mkdir(os.path.join(path, "Code"))
    os.mkdir(os.path.join(path, "Others"))
    image_formats = ["jpg", "jpeg", "png", "gif", "svg"]
    document_formats = ["pdf", "txt", "docx", "xlsx", "pptx", "csv"]
    video_formats = ["mp4", "mkv", "avi", "mov"]
    code_formats = ["py", "c", "cpp", "java", "js", "html", "css", "sh"]
    try:
        folderdata=os.listdir(path)
    except FileNotFoundError as e:
        print("enter the correct absolute folder path")
        sys.exit()
    with open("logsoffile.txt","w") as rememberlast:
        for filename in folderdata:
            if os.path.isfile(os.path.join(path, filename)):
                fileformat=filename.split(".")[-1]
                if fileformat in image_formats:
                    shutil.move(os.path.join(path, filename),os.path.join(path, "Images"))
                    prevpath=os.path.join(path, filename)+" "+os.path.join(path, "Images")
                    rememberlast.write(prevpath+"\n")
                elif fileformat in document_formats:
                    shutil.move(os.path.join(path, filename),os.path.join(path, "Documents"))
                    prevpath=os.path.join(path, filename)+" "+os.path.join(path, "Documents")
                    rememberlast.write(prevpath+"\n")
                elif fileformat in video_formats:
                    shutil.move(os.path.join(path, filename),os.path.join(path, "Videos"))
                    prevpath=os.path.join(path, filename)+" "+os.path.join(path, "Videos")
                    rememberlast.write(prevpath+"\n")
                elif fileformat in code_formats:
                    shutil.move(os.path.join(path, filename),os.path.join(path, "Code"))
                    prevpath=os.path.join(path, filename)+" "+os.path.join(path, "Code")
                    rememberlast.write(prevpath+"\n")
                else:
                    shutil.move(os.path.join(path, filename),os.path.join(path, "Others"))
                    prevpath=os.path.join(path, filename)+" "+os.path.join(path, "Others")
                    rememberlast.write(prevpath+"\n")


def generate_report(path, output_file):
    nooffiles=0
    maxfilesize=0
    maxfilename=""
    newestfilename=""
    newestfiletime=None
    oldestfilename=""
    oldestfiletime=None
    categories = {
    "Images": [],
    "Documents": [],
    "Videos": [],
    "Code": [],
    "Others": []
    }
    image_formats = ["jpg", "jpeg", "png", "gif", "svg"]
    document_formats = ["pdf", "txt", "docx", "xlsx", "pptx", "csv"]
    video_formats = ["mp4", "mkv", "avi", "mov"]
    code_formats = ["py", "c", "cpp", "java", "js", "html", "css", "sh"]
    try:
        folderdata=os.listdir(path)
    except FileNotFoundError as e:
        print("enter the correct absolute folder path")
        sys.exit()
    for filename in folderdata:
        if os.path.isfile(os.path.join(path, filename)):
            nooffiles+=1
            fileformat=filename.split(".")[-1]
            if fileformat in image_formats:
                categories["Images"].append(filename)
            elif fileformat in document_formats:
                categories["Documents"].append(filename)
            elif fileformat in video_formats:
                categories["Videos"].append(filename)
            elif fileformat in code_formats:
                categories["Code"].append(filename)
            else:
                categories["Others"].append(filename)
    with open(output_file,"w") as reportdata:
        reportdata.write(f"Directory: {path}"+"\n")
        reportdata.write(f"Total Files: {nooffiles}"+"\n")
        for i , j in categories.items():
            totalsize=0
            for filename in j:
                abpath=path+"/"+filename
                totalsize+=os.path.getsize(abpath)
                if newestfilename == "":
                    newestfilename = filename
                    newestfiletime = os.path.getmtime(abpath)
                    oldestfilename = filename
                    oldestfiletime = os.path.getmtime(abpath)
                if maxfilesize < os.path.getsize(abpath):
                    maxfilename=filename
                    maxfilesize=os.path.getsize(abpath)
                if os.path.getmtime(abpath) > newestfiletime:
                    newestfiletime=os.path.getmtime(abpath)
                    newestfilename=filename
                if os.path.getmtime(abpath) < oldestfiletime:
                    oldestfiletime=os.path.getmtime(abpath)
                    oldestfilename=filename
            reportdata.write(f"{i} : {totalsize} Bytes"+"\n")
        reportdata.write(f"Largest file: {maxfilename}: {maxfilesize} Bytes"+"\n")
        reportdata.write(f"Newest file: {newestfilename}: {newestfiletime}"+"\n")
        reportdata.write(f"Oldest file: {oldestfilename}: {oldestfiletime}"+"\n")
            

def find_duplicates(path):
    sizedict={}
    samefiles={}
    try:
        folderdata=os.listdir(path)
    except FileNotFoundError as e:
        print("enter the correct absolute folder path")
        sys.exit()
    for filename in folderdata:
        if os.path.isfile(os.path.join(path, filename)):
            abpath=path+"/"+filename
            filesize=os.path.getsize(abpath)
            if filesize in sizedict:
                sizedict[filesize].append(filename)
            else:
                sizedict[filesize]=[filename]
    for key,value in sizedict.items():
        if len(value)>1:
            for file in value:
                fullfilename=path+"/"+file
                with open(fullfilename,"rb") as readfile:
                    filedata=readfile.read()
                    hashobj=hashlib.sha256(filedata)
                    filehash=hashobj.hexdigest()
                    if filehash in samefiles:
                        samefiles[filehash].append(file)
                    else:
                        samefiles[filehash]=[file]
    for key,value in samefiles.items():
        if len(value) > 1:
            print(f"Duplicate files: {value}")


def undo():
    dirs=[
    "Images",
    "Documents",
    "Videos",
    "Code",
    "Others"
    ]
    path=None
    with open("/home/cracker/python-practice/logsoffile.txt","r") as logsdata:
        for line in logsdata:
            line=line.rstrip("\n")
            sour,dest=line.split()
            sourfilename=sour.split("/")[-1]
            fileplace=dest+"/"+sourfilename
            path=os.path.dirname(sour)
            if os.path.isfile(fileplace):
                try:
                    shutil.move(fileplace,path)
                except:
                    continue
    for dir in dirs:
        try:
            os.rmdir(path+"/"+dir)
        except:
            continue


choicelist=["1","2","3","4"]
print("1. Scan directory")
print("2. Organise directory")
print("3. Generate report")
print("4. Find duplicates")
print("5. Undo")
choice = input("Enter your choice: ")
if choice in choicelist:
    path = input("Enter absolute directory path: ")
elif choice == "5":
    pass
else:
    print("invalid choice")
    sys.exit()


if choice == "1":
    print(scan_directory(path))

elif choice == "2":
    organise(path)

elif choice == "3":
    output_file = input("Enter report output file: ")
    generate_report(path, output_file)

elif choice == "4":
    print(find_duplicates(path))

elif choice == "5":
    undo()
