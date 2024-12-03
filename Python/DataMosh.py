
'''
DataMosh v1.0.0

Developed by Owen Davis-Bower
OwenDavisBower.com

https://github.com/OwenDavisBower/DataMosh




MIT License

Copyright (c) 2018 Owen Davis-Bower

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


'''




import random, sys, os, shutil, string 

# Generate a random string of characters
def randString(size=1, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def main():
    # Number of glitches to make in process
    glitchAmount = 500
    # Number of characters to change each glitch
    glitchSize = 150
    # Position in text to start glitching
    startPos = 500
    # Choose whether to copy characters or use random characters
    copy = True

    # Accept optional arguments from commandline (glitchAmount, glitchSize, and startPos)
    if len(sys.argv) >= 3:
        if sys.argv[2] != '_':
            glitchAmount = int(sys.argv[2])

        if len(sys.argv) >= 4:
            if sys.argv[3] != '_':
                glitchSize = int(sys.argv[3])
                # Prevent error from occurring with glitchSize 1
                glitchSize = max(glitchSize, 2)

            if len(sys.argv) >= 5:
                if sys.argv[4] != '_':
                    startPos = int(sys.argv[4])

    # Extract filename and file extension from commandline argument
    fileName, fileExtension = os.path.splitext(sys.argv[1])
    # Print informational messages at start
    print("Glitching " + fileName + fileExtension)
    print("Amount: " + str(glitchAmount) + ", Size: " + str(glitchSize) + ", Starting Point: " + str(startPos))
    # Generate a new file name to save glitched file to
    newFileName = fileName + '_Glitched'

    # Copy file to new file
    shutil.copyfile(fileName + fileExtension, newFileName + fileExtension)

    # Open the image file in binary mode
    with open(newFileName + fileExtension, 'rb') as openedFile:
        # Read the binary content
        fileData = openedFile.read()

    # Convert file data to a mutable list (bytearray)
    fileDataList = bytearray(fileData)

    # Count the number of bytes in file
    byteCount = len(fileDataList)

    # Ensure that there are enough bytes
    if byteCount > startPos:
        # Modify the file the specified number of times
        for i in range(glitchAmount):
            # Select a random position to modify the file
            position = random.randrange(startPos, byteCount - 1)
            # Select a random size to modify (how many bytes)
            # Confines size to within the existing bytes, as to 
            # not change file size which causes corruption.
            size = random.randrange(1, min(glitchSize, byteCount - position))
            # Read whether to copy from data or generate new characters
            if copy:
                # Select a random position to copy from
                copyPosition = random.randrange(startPos, byteCount - 1)
                # Copy bytes from copy position
                newBytes = fileDataList[copyPosition:copyPosition + size]
            else:
                # Generate random bytes for replacement
                newBytes = bytearray(random.getrandbits(8) for _ in range(size))
            # Replace bytes in location, this is what causes the glitches
            fileDataList[position:position + size] = newBytes

    # Create new file to copy finished version to
    with open(newFileName + fileExtension, 'wb') as writeFile:
        # Write the modified binary data to the new file
        writeFile.write(fileDataList)

    # Print informational message upon completion
    print("Saved to: " + newFileName + fileExtension)

if __name__ == "__main__":
    main()
