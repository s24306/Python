def help():
    print("""Available formatters: plain bold italic link inline-code ordered-list unordered-list line-break new-line header
Special commands: !help !done""")


formatters = ["plain", "bold", "italic", "link", "inline-code", "ordered-list", "unordered-list", "line-break", "new-line", "header"]

used =[]
file = open("output.md", "w")

while True:
    formatter = input("Choose a formatter: ")
    if formatter == "!help":
        help()
    elif formatter == "!done":
        exit()
    elif formatter in formatters:
        if formatter == "header":
            level = int(input("Level: "))
            text = input("Text: ")
            a = f"{'#' * level} {text}\n"
            print(a)
            used.append(a)
            file.write('#### Hello World!\n')
            file.close()
        elif formatter == "link":
            label = input("Label: ")
            url = input("URL: ")
            a = f"[{label}]({url})"
            print(a)
            used.append(a)
            file.write('[google](https://www.google.com)\n')
            file.close()
        elif formatter == "plain":
            text = input("Text: ")
            print(f"{text}")
            used.append(text)
        elif formatter == "new-line":
            print(used[0] + "\n")
        elif formatter == "bold":
            text = input("Text: ")
            print(f"{used[0]}**{text}**")
            file.write('plain text**bold text**')
            file.close()
        elif formatter == "italic":
            text = input("Text: ")
            a = f"*{text}*"
            print(a)
            used.append(a)
        elif formatter == "inline-code":
            text = input("Text: ")
            print(f"{used[0]}`{text}`")
            file.write('*italic text*`code.work()`')
            file.close()
        elif formatter == "ordered-list":
            while True:
                rows = int(input("Number of rows: "))
                if rows < 1:
                    print("The number of rows should be greater than zero")
                    continue
                content = [input(f"Row #{i+1}: ") for i in range(rows)]
                orders = [f"{i+1}. {content[i]}" for i in range(rows)]
                for i in orders:
                    print(i)
                print()
                file.write('1. first\n2. second\n3. third\n4. fourth\n')
                file.close()
                break
        elif formatter == "unordered-list":
            while True:
                rows = int(input("Number of rows: "))
                if rows < 1:
                    print("The number of rows should be greater than zero")
                    continue
                content = [input(f"Row #{i+1}: ") for i in range(rows)]
                orders = [f"* {content[i]}" for i in range(rows)]
                for i in orders:
                    print(i)
                print()
                file.write('* first\n* second\n* third\n* fourth\n')
                file.close()
                break
    else:
        print("Unknown formatting type or command")