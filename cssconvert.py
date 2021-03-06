
import argparse
"""
Input a file which contains Python code.
Return a file which contains the same content, just updated with the correct CSS tags for each part of the code 

Basically, take the file, go line-by-line, and match the keywords with that line and replace the keywords with the CSS tags wrapped around it.
"""

keywordDict = {"def":"\"def-code\">",
               "class":"\"class-code\">",
               "self":"\"self-code\">",
               "None":"\"other-code\">",
               "True":"\"other-code\">",
               "False":"\"other-code\">",
               "if":"\"ifelse-code\">",
               "else":"\"ifelse-code\">",
               "elif":"\"ifelse-code\">",
               "continue":"\"continue-code\">",
               "break":"\"continue-code\">",
               "for":"\"loop-code\">",
               "while":"\"loop-code\">",
               "return":"\"return-code\">",
               "pass":"\"pass-code\">",
               "is":"\"isin-code\">",
               "in":"\"isin-code\">",
               "or":"\"isin-code\">",
               "and":"\"isin-code\">",
               "not":"\"isin-code\">",
               "as":"\"isin-code\">",
               "import":"\"import-code\">",
               "from":"\"import-code\">",
               "object":"\"object-code\">"}

func_code = "\"func-code\">"
const_code = "\"const-code\">"
string_code = "\"string-code\">"

endtag = "</span>"
starttag = "<span class="

parser = argparse.ArgumentParser(description='Color code your Python code')
parser.add_argument('--filename', '-f', help="name of the input python file")

args = parser.parse_args()
fullpath = args.filename
filename = fullpath.split('\\')[-1]
fname = filename.split('.py')[0]
outpath = "Results/"
f = open(fullpath, "r")
template = open("template.html", "r")
website_code = open(outpath+fname+"_websnippet.html", "w")

keywords = list(keywordDict.keys())
stopcharacters = [' ', ':', '(', ')', '.', '[', ']', '{', '}', ',', '\n', '#']
iscommand = False
commands = ["#newtext", "#strikeout"]


numlines = 0
for template_line in template:
    #print(template_line.strip() + str(len(template_line.strip())))
    if template_line.strip() == "<<<Enter filename tag>>>":
        print("First line found")
        break
    else:
        website_code.write(template_line)

website_code.write("<span class=\"fileformat\">" + filename + "</span>")

print("Continue............")
for template_line in template:
    if template_line.strip() == "<<<Enter line numbers here>>>":
        print("Count how many lines first")
        for line in f:
            numlines += 1
            website_code.write(str(numlines)+"\n")
        print(numlines)
        f.close()
    elif template_line.strip() == "<<<Enter the code here>>>":
        print("Second line found")
        break
    else:
        website_code.write(template_line)
        

f = open(fullpath, "r")
for line in f: #line by line
    #First check to see if this line has a special command
    strippedline = line.strip()
    if len(strippedline) > 0:
        if strippedline[0] == '#': #Commands start with a '#'
            temp = strippedline.split("::")
            numspaces = len(line) - len(line.strip()) - 1
            spaces = ""
            for i in range(numspaces):
                spaces += " "
            
            if len(temp) == 1: #Can use for comments
                lineaccumulator = spaces+"<span class=\"comment-code\">"+line.strip()+"</span>"
            elif len(temp) == 2:
                command, text = temp
            
                if command == "#newtext":
                    lineaccumulator = spaces+"<span class=\"newtext\">"+text+"</span>"
                elif command == "#strikeout":
                    lineaccumulator = spaces+"<span class=\"strikeout\">"+text+"</span>"
            
            website_code.write(lineaccumulator+'\n')
            lineaccumulator = ""
            s = ""
            continue

    
    linelist = [] #Get a list of all of the characters in this line
    for i in range(len(line)):
        linelist.append(line[i])
    
    s = "" #Accumulator for each word in the line.  Becomes "" when reaching a stop character
    lineaccumulator = "" #Accumulating result for each line.  Starts as "" for each line
    isastring = False

    
    
    for c in linelist: #loop through each character in the line one at a time
        addChar = True

        if '\"' == c:
            if '\"' not in s: #if " is not already in s
                isastring = True
            else:
                isastring = False
                addChar = False
                lineaccumulator += starttag+string_code+s+c+endtag
                s = ""

        if '\'' == c:
            if '\'' not in s: #if " is not already in s
                isastring = True
            else:
                isastring = False
                addChar = False
                lineaccumulator += starttag+string_code+s+c+endtag
                s = ""

        if isastring:
            s += c
            
        else:
            if c in stopcharacters:
                if s in keywords:
                    lineaccumulator += starttag+keywordDict[s]+s+endtag
                else:
                    if c == '(':
                        #print(s)
                        lineaccumulator += starttag+func_code+s+endtag
                    elif s.isalnum():
                        if s.isupper():
                            lineaccumulator += starttag+const_code+s+endtag
                            #print(s)
                        else:
                            lineaccumulator += s
                    else:
                        #print(s)
                        lineaccumulator += s
                
                if c != '\n':
                    lineaccumulator += c
                s = ""
                    
            else: #c is not in stopcharacters
                if addChar:
                    s += c

    website_code.write(lineaccumulator+'\n')
    lineaccumulator = ""
    s = ""

for template_line in template:
    website_code.write(template_line)


f.close()
#ff.close()
template.close()
website_code.close()
    


