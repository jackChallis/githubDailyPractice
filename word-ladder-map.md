# Word Ladder Distance Mapping

This project implements a word ladder distance metric and creates a 2D visualization where Euclidean distances approximate word ladder distances between words.

## Problem Description

A word ladder is a word game where the objective is to transform one word into another through a sequence of valid words, changing one letter at a time. This project:

1. Implements a distance metric between words based on minimal word ladder length
2. Creates a 2D visualization where similar words appear closer together
3. Shows connectivity between words, highlighting how words relate through transformations

For example:
- cat -> cut (distance 1: single letter change)
- cat -> coat (distance 1: single letter addition)
- cart -> bone (distance 4: cart -> care -> core -> bore -> bone)

## Features

- Handles multiple types of word transformations:
  - Adding one letter
  - Removing one letter
  - Changing one letter
  - Special handling of possessive forms ("'s")
- Finds shortest paths between words
- Visualizes word relationships in 2D space
- Shows connected components in different colors
- Displays connectivity between words

## Requirements

```
python 3.8+
numpy
matplotlib
scikit-learn (for MDS)
```

## Usage

```python
# Basic distance calculation
distance('cat', 'cut')  # Returns 1
distance('cart', 'bone')  # Returns 4

# Generate full visualization
plot_word_map()
```

## Sample Input/Output

### Word List
```python
WORD_LIST = {
    'cat', 'bat', "bat's", 'beat', 'boat', "cat's", 'chat', 'coat', 'cut', 'curt', 'cute',
    'cart', 'care', 'core', 'bore', 'bone', 'bare', 'care', 'cars', 'arts', 'part',
    'carts', 'parts'
}
```

### Example Paths
```
cat -> cut -> cute
cart -> care -> core -> bore -> bone
arts -> parts -> part
```

### Visualization
The output creates a 2D plot where:
- Words that can be transformed into each other in one step appear closer together
- Different connected components are shown in different colors
- Distance between points approximates the word ladder distance
- Lines show direct connections between words (distance = 1)

## Implementation Details

### Distance Metric
The distance between two words is defined as the minimum number of transformations needed to change one word into the other. Each transformation must result in a valid word from the word list.

### Visualization Method
1. Creates a distance matrix using word ladder distances
2. Uses Multidimensional Scaling (MDS) to create a 2D embedding
3. Positions words so Euclidean distances approximately match word ladder distances
4. Colors connected components differently
5. Shows direct connections between words

### Connectivity Handling
- Disconnected components are identified and colored differently
- Bridge words (like 'carts' and 'parts') connect otherwise isolated words
- The visualization makes it easy to spot isolated words or groups

## Example Code
```python
# Calculate distance between two words
print(f"Distance 'cat' to 'cut': {distance('cat', 'cut')}")
print(f"Distance 'cart' to 'bone': {distance('cart', 'bone')}")

# Show all connections for a word
print("\nConnections from 'cat':")
valid_transforms = {w for w in generate_transformations('cat') if w in WORD_LIST}
print(valid_transforms)

# Create visualization
plot_word_map()
```

## Contributing
Feel free to contribute by:
- Adding more words to create interesting paths
- Improving visualization features
- Adding new transformation types
- Optimizing distance calculations

## Notes
- The visualization is an approximation - Euclidean distances in 2D cannot perfectly represent all word ladder distances
- Adding or removing words can significantly change the connectivity of the graph
- Some words may appear isolated if no valid transformations exist in the word list
