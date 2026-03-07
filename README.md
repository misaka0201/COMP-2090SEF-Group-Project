# TASK 2 Self Study Report
## New data structure: bytearray <br>
Bytearray is a mutable sequence of bytes. It's elements are from 0 - 255 and it can be modified after creation. <br>
Comparing to bytes, bytearray is mutable. You can change the elements by some useful methods, like append(), extend() and insert(). <br>
Bytearray is useful when working with binary data , such as network communication, file processing and binary protocols.

### Introduction
First, converts the string into a bytearray object. Then the for loop goes through every byte in the bytearray.<br>
For each byte, the program adds 4. After encryption the output might look difficult to understand. <br>
Then use another for loop to reverses the encryption. At last decode() converts the bytearray back into a readable string.
