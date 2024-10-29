#!/usr/bin/env python3
"""
Word Ladder Path Finder
======================

This program finds all possible shortest paths between words in a word ladder puzzle.
A word ladder is a sequence of words where each word differs from the previous word by:
- Adding one letter (cat -> chat)
- Removing one letter (chat -> cat)
- Changing one letter (cat -> bat)

The program finds and displays all possible shortest paths up to a specified maximum depth.

Example:
    For the word 'cat' with depth 2, it might show:
    cat
      cut (paths: cat -> cut)
      bat (paths: cat -> bat)
        cute (paths: cat -> cut -> cute)

Features:
- Finds all shortest paths between words
- Breadth-first search ensures minimum path lengths
- Handles multiple equivalent-length paths
- Supports apostrophe-s ('s) transformations
"""

import string
from collections import defaultdict, deque

# Sample word list with paths up to length 4
# Includes the path cart -> care -> core -> bore -> bone
WORD_LIST = {
    'cat', 'bat', "bat's", 'beat', 'boat', "cat's", 'chat', 'coat', 'cut', 'curt', 'cute',
    'cart', 'care', 'core', 'bore', 'bone', 'bare', 'care', 'cars', 'arts', 'part'
}

class WordLadderFinder:
    """A class to find all shortest word ladder paths between words."""
    
    def __init__(self, dictionary, valid_additions=None):
        """
        Initialize the word ladder finder.
        
        Args:
            dictionary (set): Set of valid words
            valid_additions (list): List of valid letter additions (default: lowercase letters + "'s")
        """
        self.dictionary = dictionary
        self.valid_additions = valid_additions or (list(string.ascii_lowercase) + ["'s"])
        
    def _generate_transformations(self, word):
        """
        Generate all possible one-step transformations of a word.
        
        Args:
            word (str): The word to transform
            
        Returns:
            set: All possible transformations
        """
        transformations = set()
        
        # 1. Adding a letter
        for position in range(len(word) + 1):
            for letter in self.valid_additions:
                transformations.add(word[:position] + letter + word[position:])
        
        # 2. Removing a letter
        for position in range(len(word)):
            transformations.add(word[:position] + word[position+1:])
        
        # 3. Changing a letter
        for position in range(len(word)):
            for letter in self.valid_additions:
                transformations.add(word[:position] + letter + word[position+1:])
                
        return transformations
    
    def find_paths(self, starting_word, max_depth):
        """
        Find all shortest word ladder paths from the starting word up to max_depth.
        
        Args:
            starting_word (str): The word to start from
            max_depth (int): Maximum transformation depth to explore
            
        Returns:
            None: Prints paths to stdout
        """
        # Queue stores (word, path) pairs
        queue = deque([(starting_word, [starting_word])])
        # Track all paths to each word and their lengths: (min_length, paths_set)
        paths = defaultdict(lambda: (float('inf'), set()))
        paths[starting_word] = (1, {tuple([starting_word])})
        
        while queue:
            current_word, current_path = queue.popleft()
            current_depth = len(current_path)
            min_depth, _ = paths[current_word]
            
            # Only process if this is a shortest path
            if current_depth > min_depth:
                continue
                
            depth = len(current_path) - 1
            if depth > 0:  # Don't print paths for starting word
                current_paths = " OR ".join([" -> ".join(path) for path in paths[current_word][1]])
                print("  " * depth + current_word + f" (paths: {current_paths})")
            else:
                print(current_word)
            
            if depth >= max_depth:
                continue
                
            # Process valid transformations
            for new_word in self._generate_transformations(current_word):
                if new_word in self.dictionary:
                    new_path = tuple(current_path + [new_word])
                    new_depth = len(new_path)
                    min_existing_depth, existing_paths = paths[new_word]
                    
                    if new_depth < min_existing_depth:
                        # Found a shorter path, clear existing paths
                        paths[new_word] = (new_depth, {new_path})
                        queue.append((new_word, list(new_path)))
                    elif new_depth == min_existing_depth:
                        # Found another path of same length
                        existing_paths.add(new_path)
                        paths[new_word] = (min_existing_depth, existing_paths)

def main():
    """Main program entry point with example usage."""
    finder = WordLadderFinder(WORD_LIST)
    
    print("Word Ladder Path Finder")
    print("======================")
    print("\nExample 1: Short transformation (depth 2)")
    print("-----------------------------------------")
    finder.find_paths("cat", 2)
    
    print("\nExample 2: Longer transformation (depth 4)")
    print("-----------------------------------------")
    finder.find_paths("cart", 4)
    
    print("\nInteractive Mode")
    print("-----------------------------------------")
    while True:
        try:
            print('\nStarting Word (or press Ctrl+C to exit): ')
            starting_word = input().strip()
            print('Max Depth: ')
            max_depth = int(input().strip())
            finder.find_paths(starting_word, max_depth)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except ValueError:
            print("Please enter a valid number for depth")

if __name__ == "__main__":
    main()