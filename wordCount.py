import os, stat, re
from sys import stderr, argv

inFileName=argv[1]
outFileName=argv[2]

words = {}

# method to read a word and check if it exists in words
def wordCheck(wordraw):
    word = wordraw.lower()
    if word == "":
        return
    if word in words:
        words[word] += 1
    else:
        words.update({word: 1})

totalBytesWritten = 0
read_fd = os.open(inFileName, os.O_RDONLY);
write_fd = os.open(outFileName, os.O_WRONLY | os.O_CREAT | os.O_TRUNC);
assert read_fd >= 0
assert write_fd >= 0
read_buffer = os.read(read_fd, 1000000) # wont read more than 1 megabyte worth of byte
write_buffer = b""
wordList = re.split(r"[\W]+", read_buffer.decode()) # splits all words in read_buffer by non-alphanumeric chars
for word in wordList:
    wordCheck(word)
# sort the dict
wordsSorted = {k: v for k, v in sorted(words.items())}

for key in wordsSorted:
    write_buffer += key.encode()
    write_buffer += " ".encode()
    write_buffer += str(wordsSorted[key]).encode()
    write_buffer += "\n".encode()

while len(write_buffer):
    wc = os.write(write_fd, write_buffer)
    write_buffer = write_buffer[wc:]
    totalBytesWritten += wc

os.write(2, f"wrote a total of {totalBytesWritten} bytes\n".encode())
os.fsync(write_fd)
os.close(read_fd)
os.close(write_fd)
