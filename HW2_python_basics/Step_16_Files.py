with open('Step_16_Files_exmple.txt', 'w') as f:
    f.write("Hello, World!")

with open('Step_16_Files_exmple.txt', 'r') as f:
    text = f.read()
    print(text)
     
