def textToBinary(msg):
    binaryList = []
    for char in msg:
        asciiNum = ord(char)
        binaryCode = format(asciiNum, '08b')
        binaryList.append(binaryCode)
        finalBinary = ' '.join(binaryList)
        return finalBinary
    
# Example usage:
result = textToBinary("y")
print(result)