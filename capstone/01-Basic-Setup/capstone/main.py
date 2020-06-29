import aqgFunction


# Main Function
def generate(filename):
    # Create AQG object
    aqg = aqgFunction.AutomaticQuestionGenerator()

    #inputTextPath =r"C:\Users\hp\Downloads\Automatic-Question-Generator-master\AutomaticQuestionGenerator/DB/db.txt"
    inputTextPath=filename
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    #readFile = open(inputTextPath, 'r+', encoding="utf8", errors = 'ignore')

    inputText = readFile.read()
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''

    questionList = aqg.aqgParse(inputText)
    aqg.display(questionList)
    print("**********************")
    print(aqg.filename)
    print("**********************")
    

    #aqg.DisNormal(questionList)

    return 0

def main():
    inputTextPath =r"C:\Users\hp\Downloads\Automatic-Question-Generator-master\AutomaticQuestionGenerator\DB/text.txt"
    generate(inputTextPath)
    return 0;
# Call Main Function
if __name__ == "__main__":
    main()

