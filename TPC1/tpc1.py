import sys

def counter(text):
    i = 0
    add = True
    digits = "0123456789"
    counter = 0

    while(i < len(text)):
        if(text[i].lower() == 'o'):
            if(text[i+1].lower() == 'n'):
                add = True
                i+=1
            elif(text[i+1].lower() == 'f' and text[i+2].lower() == 'f'):
                add = False
                i+=2
        if(text[i] == '='):
            print(counter)
        if(text[i] in digits and add):
            numberToAdd = int(text[i])
            i+=1
            while(text[i] in digits):
                numberToAdd = numberToAdd*10 + int(text[i])
                i+=1

            counter += numberToAdd
        else:
            i+=1

    print("Total counted: ", counter)

def main():
    
    #text = "oN 123 oFF 456 = oN 789 oFF 321 ="  
    text = "Agabdvsu06sisvh2025=Off24dhsia1ondgaiak34=1="
    counter(text) 

if __name__ == "__main__":
    main()