import os, sys
tbw = 40
try:
    import pdftotext
except ImportError:
    available1 = False
else:
    available1 = True

try:
    import cv2
except ImportError:
    available2 = False
else:
    available2 = True

try:
    import pytesseract
except ImportError:
    available3 = False
else:
    available3 = True

def help():
    print("\nGrades a set of pdfs against an assignment list by converting pdf to text and searching for a string.\n")
    print("REQUIRES:")
    print("\tModule 'pdftotext'")
    print("\tWrite permission to current directory")
    print("\tWrite permission to output file directory/output file")
    print("\tRead permission to submissions directory")
    print("\tRead permission to assignments file\n")
    print("ADDTIONAL REQUIREMENTS:")
    print("\tModuld 'opencv-python")
    print("\tModule 'pytesseract'\n")
    print("External Tesseract support also required.")
    print("Tested on WSL Debian, Kernel 5.10.16")
    print("Packages 'tesseract-ocr' and 'libtesseract-dev' installed through apt\n")
    print("OPTIONS:")
    print("\t-h\t--help\t\t: display this message")
    print("\t-a\t--assignments\t: specify path to assignments file. required to grade")
    print("\t-s\t--submissions\t: specify path to submissions directory. required to grade")
    print("\t-o\t--output\t: specify path to output file. output format .csv, required to grade")
    print("\nUSAGE: (assumes 'python3' is your python executable)")
    print("\tpython3 autograde.py 'path to assignments' 'path to submissions dir' 'path to output'")
    print("\tpython3 autograde.py --assignments 'path to assignments' --submissions 'path to submissions dir' --output 'path to output'")
    print("\tpython3 autograde.py -a 'path to assignments' -s 'path to submissions dir' -o 'path to output'")
    print("\nAssingments file format:\n")
    print("A:AA\nA:AB\nA:AC\nB:AD\n")
    print("example:")
    print("3.09\n3.01\n1.26\n3.13\n4.02\n4.03\n")    

def twarning():
    print("\nPYTHON AUTOGRADING SCRIPT UTLIZING IMAGE RECGONITION")
    print("Utlizes opencv-python and pytesseract to attempt to read text from image submissions")
    print("\nRESULTS MAY BE SUFFICENTLY UNRELAIBLE, CONSIDER HUMAN VERIFICATION OF SCORES\n")

def improper_args():
    print("\nImproper arguments")
    print("\tpython3 autograde.py --help")
    print("\tpy autograde.py --help")

def argc(args):
    if (("--assignments" in args) or ("-a" in args)) and (("--submissions" in args) or ("-s" in args)) and (("--output" in args) or ("-o" in args)):
        return True
    else:
        return False

def argcheck(arg):
    if arg == "-a" or arg == "-o" or arg == "-s" or arg == "--assignments" or arg == "--submissions" or arg == "--output":
        return True
    else:
        return False

def chkarg(i, args):
    for n in args:
        if i == n-1:
            return False
    return True

def main():
    twarning()
    if (not(available1)):
        print("\nModule 'pdftotext' is required")
        print("It can be installed via pip:")
        print("\tpython3 -m pip install pdftotext")
        print("\tpip install pdftotext\n")
        return
    if (not(available2)):
        print("\nModule 'opencv-python' (cv2) is required")
        print("It can be installed via pip:")
        print("\tpython3 -m pip install opencv-python")
        print("\tpip install opencv-python\n")
        return
    if (not(available3)):
        print("\nModule 'pytesseract' is required")
        print("It can be installed via pip:")
        print("\tpython3 -m pip install pytesseract")
        print("\tpip install pytesseract\n")
        print("Tesseract may need to be installed on the host system\n")
        return
    leng = len(sys.argv)
    if "--help" in sys.argv or "-h" in sys.argv:
        help()
        if (argc(sys.argv)):
            grade()
        return
    if leng == 4:
        do_score(sys.argv[1], sys.argv[2], sys.argv[3])
        return
    if leng > 7:
        improper_args()
        return
    if argc(sys.argv):
        grade()
    else:
        improper_args()
        
def grade():
    leng = len(sys.argv)
    args = []
    argi = [0,0,0]
    for i in range(1, leng):
        i = leng - i
        arg = sys.argv[i]
        if argcheck(arg) and (i < (leng-1) or chkarg(i, args)):
            args.append(i)
            if arg == "-a" or arg == "--assignments":
                argi[0] = i 
            elif arg == "-s" or arg == "--submissions":
                argi[1] = i
            elif arg == "-o" or arg == "--output":
                argi[2] = i
            else:
                improper_args()
                return
    argn = [sys.argv[argi[0]+1], sys.argv[argi[1]+1], sys.argv[argi[2]+1]]
    print("\nAssignments at:\t ./" + argn[0] + "\nSubmissions in:\t ./" + argn[1] + "/\nOutputs to:\t ./" + argn[2] + "\n")
    do_score(argn[0], argn[1], argn[2])

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor
spinner = spinning_cursor()

def do_score(problems, subdir, fout): #if the file or folder is not in the same location, specify the path from where the script is run to there.
    #txtdir and fout will create a file if no such director or file exists
    txtdir = 'temp'
    os.mkdir(txtdir)
    score_against = assignments(problems)
    print("Converting files to txt ...")
    sys.stdout.flush()
    sys.stdout.write('\b')
    totxt(subdir, txtdir)
    print("Done")
    files = os.listdir(txtdir)
    print("Writing scores to " + fout + ' ...')
    sys.stdout.flush()
    sys.stdout.write('\b')
    scores = ''
    ascore = 0
    nentries = 0
    scored = 0
    for file in files:
        sys.stdout.write(next(spinner))
        nentries+=1
        path = txtdir + '/' + file
        outs = score(path, score_against)
        scores += outs[0]
        ascore += outs[1]
        scored += outs[2]
        os.remove(path)
        sys.stdout.flush()
        sys.stdout.write('\b')
    os.rmdir(txtdir)
    final = fmt(scores, ascore, nentries, scored, score_against)
    with open(fout, "w") as o:
        o.write(final)
    print("Done\n")
    oof = len(score_against)
    avg = round(ascore/scored, 2)
    strasg = ''
    for i in score_against:
        strasg += i + ' '
    print("Assignments Scored For:\t\t{}".format(strasg))
    print("Number of Submissions:\t\t{}".format(nentries))
    print("Number of Submissions Scored:\t{}".format(scored))
    print("Average Score:\t\t\t{}/{}\n".format(avg,oof))

def fmt(scorestr, scoresum, sms, nscored, astlist):
    out = "Scoring assignments: "
    for i in astlist:
        out += i + " "
    oof = len(astlist)
    average = round(scoresum / nscored, 2)
    out+='\nNumber of Submissions,Number Scored, Average Score\n{},{},{}/{}\n'.format(sms,nscored,average,oof)
    return out + scorestr

def assignments(filename): #returns a list of the assignments to search for
    tem = open(filename, 'r').readlines()
    out = []
    for i in tem:
        if i[-1:] == "\n":
            out.append(i[:-1])
        else:
            out.append(i)
    return out

def totxt(sourcedir, outdir):
    files = os.listdir(sourcedir)
    for i in files:
        sys.stdout.write(next(spinner))
        parts = splt(i)
        last4 = parts[1]
        tname = outdir + '/' + parts[0]+'.txt'
        name = tname.replace(',','')
        os.mknod(name)
        file = sourcedir + '/' + i
        if last4 == ".pdf":
            with open(file, "rb") as f:
                pdf = pdftotext.PDF(f)
            with open(name, 'w') as o:
                o.write("\n\n".join(pdf))
        if last4 == ".txt":
            with open(file, "rb") as f:
                with open(name, 'w') as o:
                    o.write(f.read())
        if image(last4):
            with open(name, 'w') as o:
                o.write(pytesseract.image_to_string(cv2.imread(file)))
        sys.stdout.flush()
        sys.stdout.write('\b')

def image(extn):
    ext = extn.lower()
    if ext==".png" or ext==".jpg":
        return True
    return False

'''
def totxt(sourcedir, outdir): #reads each file in sourcedir, in outdir makes a plaintext file with the same name. If file in sourcedir is pdf, writes its contents to outdir 
    files = os.listdir(sourcedir) #must be accesible from where the script is run
    for i in files:
        parts = splt(i)
        tname = outdir + '/' + parts[0]
        varx = parts[1]=='.pdf'
        if varx:
            tname += ".txt"
        name = tname.replace(',','')
        os.mknod(name)
        if varx:
            with open(sourcedir + '/' + i, "rb") as f:
                pdf = pdftotext.PDF(f)
            with open(name, 'w') as o:
                o.write("\n\n".join(pdf))
'''

def splt(name): #split the filename into a list of header and extenstion
    header = name[:-4]
    extension = name[-4:]
    return [header, extension]

def score(filename, qlist): #opens a plaintext file filename, seacches for each string in qlist in filenane, and writes filename total found and missing strings to out
    out = []
    file = filename[5:]
    if filename[-4:]=='.txt':
        scr = len(qlist)
        miss = []
        with open(filename) as f:
            content = f.read()
            for i in qlist:
                if not(i in content):
                    scr-=1
                    miss.append(i)
        out.append(formout(file, scr, miss))
        out.append(scr)
        out.append(1)
    else:
        out.append(formout(file, "", []))
        out.append(0)
        out.append(0)
    return out


def formout(name, score, missing): #formats the output of score as filename, score, missing0 missing1 missing2;
    out = "{},{},".format(name, score)
    for i in missing:
        out = out + i + ' '
    out = out + '\n'
    return out

main()
