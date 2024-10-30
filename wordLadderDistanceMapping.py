#!/usr/bin/env python3
"""
Word Ladder Distance Mapping
===========================
This module implements a word ladder game with distance calculations and visualization.
A word ladder is a sequence of words where each word differs from the previous word by
one transformation (adding, removing, or changing one letter).
"""

from collections import deque
import string
from typing import Set, Dict, List, Tuple, Optional
import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

class WordTransformer:
    """Handles word transformation operations and rules."""
    
    def __init__(self, allow_possessives: bool = True):
        """
        Initialize the transformer with specified rules.
        
        Args:
            allow_possessives (bool): Whether to allow "'s" transformations
        """
        self.alphabet = list(string.ascii_lowercase)
        self.allow_possessives = allow_possessives

    def generate_transformations(self, word: str) -> Set[str]:
        """
        Generate all possible one-step transformations of a word.
        
        Args:
            word (str): The word to transform
            
        Returns:
            Set[str]: All possible transformations
        """
        transformations = set()
        
        # Handle possessive form if allowed
        if self.allow_possessives:
            if word.endswith("'s"):
                transformations.add(word[:-2])
            else:
                transformations.add(word + "'s")
        
        # Add a letter
        for position in range(len(word) + 1):
            for letter in self.alphabet:
                transformations.add(word[:position] + letter + word[position:])
        
        # Remove a letter
        for position in range(len(word)):
            transformations.add(word[:position] + word[position+1:])
        
        # Change a letter
        for position in range(len(word)):
            for letter in self.alphabet:
                transformations.add(word[:position] + letter + word[position+1:])
                
        return transformations

class WordLadderGraph:
    """Represents the graph of words and their connections."""
    
    def __init__(self, word_list: Set[str], transformer: WordTransformer):
        """
        Initialize the word ladder graph.
        
        Args:
            word_list (Set[str]): Set of valid words
            transformer (WordTransformer): Word transformation handler
        """
        self.words = word_list
        self.transformer = transformer
        self._distance_cache: Dict[Tuple[str, str], int] = {}

    def distance(self, word1: str, word2: str) -> float:
        """
        Calculate the shortest word ladder distance between two words.
        
        Args:
            word1 (str): Starting word
            word2 (str): Target word
            
        Returns:
            float: Minimum number of transformations needed (inf if no path exists)
        """
        # Check cache
        cache_key = tuple(sorted([word1, word2]))
        if cache_key in self._distance_cache:
            return self._distance_cache[cache_key]
        
        if word1 == word2:
            return 0
        if word1 not in self.words or word2 not in self.words:
            return float('inf')
        
        # BFS for shortest path
        queue = deque([(word1, 0)])
        seen = {word1}
        
        while queue:
            current_word, current_distance = queue.popleft()
            
            for new_word in self.transformer.generate_transformations(current_word):
                if new_word == word2:
                    self._distance_cache[cache_key] = current_distance + 1
                    return current_distance + 1
                    
                if new_word in self.words and new_word not in seen:
                    seen.add(new_word)
                    queue.append((new_word, current_distance + 1))
        
        self._distance_cache[cache_key] = float('inf')
        return float('inf')

class WordLadderVisualizer:
    """Handles visualization of word ladder relationships."""
    
    def __init__(self, graph: WordLadderGraph):
        """
        Initialize the visualizer.
        
        Args:
            graph (WordLadderGraph): The word ladder graph to visualize
        """
        self.graph = graph
        self.components = None
        self.coords = None
        self.word_list = None

    def _create_distance_matrix(self) -> Tuple[np.ndarray, List[str]]:
        """
        Create a distance matrix for all words.
        
        Returns:
            Tuple[np.ndarray, List[str]]: Distance matrix and corresponding word list
        """
        words = list(self.graph.words)
        n = len(words)
        matrix = np.zeros((n, n))
        
        # Calculate distances
        disconnected_pairs = []
        for i in range(n):
            for j in range(i+1, n):
                d = self.graph.distance(words[i], words[j])
                if d == float('inf'):
                    disconnected_pairs.append((words[i], words[j]))
                matrix[i,j] = min(d, 100)  # Cap distances for visualization
                matrix[j,i] = matrix[i,j]
        
        # Report disconnected words
        if disconnected_pairs:
            print("\nDisconnected word pairs:")
            for w1, w2 in disconnected_pairs:
                print(f"No path between '{w1}' and '{w2}'")
        
        return matrix, words

    def _find_components(self) -> List[Set[str]]:
        """
        Find connected components in the word graph.
        
        Returns:
            List[Set[str]]: List of connected components
        """
        def find_component(word: str, visited: Set[str]) -> Set[str]:
            component = {word}
            queue = deque([word])
            while queue:
                current = queue.popleft()
                for other in self.graph.words:
                    if other not in visited and self.graph.distance(current, other) != float('inf'):
                        visited.add(other)
                        component.add(other)
                        queue.append(other)
            return component

        visited = set()
        components = []
        for word in self.graph.words:
            if word not in visited:
                visited.add(word)
                component = find_component(word, visited)
                components.append(component)

        return components

    def plot(self, show_connections: bool = True) -> None:
        """
        Create and show the visualization.
        
        Args:
            show_connections (bool): Whether to show direct connections between words
        """
        # Get distance matrix and components
        dist_matrix, self.word_list = self._create_distance_matrix()
        self.components = self._find_components()
        
        # Create 2D embedding
        mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
        self.coords = mds.fit_transform(dist_matrix)
        
        # Plot
        plt.figure(figsize=(12, 8))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(self.components)))
        word_to_component = {word: i for i, comp in enumerate(self.components) for word in comp}
        
        # Plot points and labels
        for i, word in enumerate(self.word_list):
            color = colors[word_to_component[word]]
            plt.scatter(self.coords[i, 0], self.coords[i, 1], color=color, alpha=0.5)
            plt.annotate(word, (self.coords[i, 0], self.coords[i, 1]))
        
        # Show direct connections if requested
        if show_connections:
            for i, word1 in enumerate(self.word_list):
                for j, word2 in enumerate(self.word_list[i+1:], i+1):
                    if self.graph.distance(word1, word2) == 1:
                        plt.plot([self.coords[i,0], self.coords[j,0]], 
                               [self.coords[i,1], self.coords[j,1]], 
                               'gray', alpha=0.2)
        
        plt.title('Word Ladder Distance Map')
        plt.xlabel('Dimension 1')
        plt.ylabel('Dimension 2')
        plt.grid(True)
        plt.show()

def main():
    """Main program entry point with example usage."""
    # Sample word list
    WORD_LIST = {
        'cat', 'bat', "bat's", 'beat', 'boat', "cat's", 'chat', 'coat', 'cut', 'curt', 'cute',
        'cart', 'care', 'core', 'bore', 'bone', 'bare', 'care', 'cars', 'arts', 'part',
        'carts', 'parts'  # Bridge words
    }
    
    # Create objects
    transformer = WordTransformer(allow_possessives=True)
    graph = WordLadderGraph(WORD_LIST, transformer)
    visualizer = WordLadderVisualizer(graph)
    
    # Show some example distances
    print("Example distances:")
    print(f"'cat' to 'cut': {graph.distance('cat', 'cut')}")
    print(f"'cart' to 'bone': {graph.distance('cart', 'bone')}")
    
    # Create visualization
    visualizer.plot(show_connections=True)

if __name__ == "__main__":
    main()