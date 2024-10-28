#!/usr/bin/env python
# coding: utf-8

# In[7]:


'''
Prompt

I notice you mentioned transcribing a file, but I don't see any file shared in our conversation. I'm happy to help with transcription if you share the content you'd like transcribed.

As for a CS50-level programming problem, here's an engaging one:

Write a program that implements a "pyramid printer" that creates a Mario-style pyramid of hashes (#) with the following requirements:

1. Ask the user for a height between 1 and 8 inclusive
2. Print a right-aligned pyramid of that height using hash symbols
3. Each level should have one more hash than the previous level

For example, if the user enters 4, the output should look like:
```
   #
  ##
 ###
####
```

This problem practices:
- User input validation
- Nested loops
- String manipulation
- Pattern recognition
- Basic console output formatting

Would you like me to provide more details or would you prefer a different type of problem?

---
Review
---
I'll review your complete solution from the file:
Your solution is well-structured and shows good understanding of Python concepts. Let's break it down:
Strengths:

Elegant use of list comprehension for building each level of the pyramid
Good documentation by keeping the original problem statement in a docstring
Proper use of if __name__ == "__main__": for script execution
Fixed the input validation to correctly include 8 (using <=8 instead of <8 as in your previous version)

Areas for improvement:

Error Handling: The program will crash if:

User enters non-integer input (ValueError)
User enters any number outside 1-8 (silently fails)


User Experience: Could provide better feedback for invalid inputs

Here's a suggested enhanced version that addresses these points:
pythonCopydef mario(n):
    for layer in range(1, n+1):
        level = ['#' if x >= n-layer else ' ' for x in range(n)]
        print(''.join(level))

if __name__ == "__main__":
    while True:
        try:
            print('Input Pyramid Depth (1-8)')
            input1 = int(input())
            if 1 <= input1 <= 8:
                mario(input1)
                break
            else:
                print("Error: Please enter a number between 1 and 8")
        except ValueError:
            print("Error: Please enter a valid integer")
The core algorithm is very clean and efficient. Your use of list comprehension shows advanced thinking for a CS50-level problem, as many beginners would use nested loops instead.
Would you like to try a more challenging variation of this problem, perhaps creating a double pyramid like this?

'''
def mario(n):
    for layer in range(1,n+1):
        level=['#' if x>=n-layer else ' ' for x in range(n)]
        print(''.join(level))
        
if __name__ == "__main__":
    print('Input Pyramid Depth (1-8)')
    input1=int(input())
    if 1<=input1<=8:
        mario(input1)





