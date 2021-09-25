
def display_pictures(attempt_number):
    if attempt_number == 8:
        return """
    |----
    |    
    |
____|________"""
    elif attempt_number == 7:
        return """
    |----|
    |    
    |
____|________"""
    elif attempt_number == 6:
        return """
    |----|
    |    0
    |    
____|________"""
    elif attempt_number == 5:
        return """
    |----|
    |    0
    |    |
    |
____|________"""
    elif attempt_number == 4:
        return """
    |----|
    |    0
    |  --|
    |
____|________"""
    elif attempt_number == 3:
        return """
    |----|
    |    0
    |  --|--
    |
____|________"""
    elif attempt_number == 2:
        return """
    |----|
    |    0
    |  --|--
    |   /
____|________"""
    elif attempt_number == 1:
        return """
    |----|
    |    0
    |  --|--
    |   / \\
____|________
"""


#for i in range(1, 9):
    #print("i = ", i, display_pictures(i))