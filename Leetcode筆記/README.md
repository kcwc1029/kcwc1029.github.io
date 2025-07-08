## Array

-   [26. Remove Duplicates from Sorted Array](./Array/26.remove-duplicates-from-sorted-array.md)
-   [80. Remove Duplicates from Sorted Array II](./Array/80.remove-duplicates-from-sorted-array-ii.md)
-   [27. Remove Element](./Array/27.remove-element.md)
-   [66. Plus One](./Array/66.plus-one.md)

## Binary Search

-   [69. Sqrt(x)](./Binary-Search/69.sqrt.md)
-   [35. Search Insert Position](./Binary-Search/35.search-insert-position.md)

## Matrix

-   [36. Valid Sudoku](./Matrix/36.valid-sudoku.md)
-   [48. Rotate Image](./Matrix/48.rotate-image.md)
-   [54. Spiral Matrix](./Matrix/54.spiral-matrix.md)
-   [59. Spiral Matrix II](./Matrix/59.spiral-matrix-ii.md)

## Hash Table

-   [1. Two Sum](./Hash-Table/1.two-sum.md)
-   [49. Group Anagrams](./Hash-Table/49.group-anagrams.md)
-   [73. Set Matrix Zeroes](./Hash-Table/73.set-matrix-zeroes.md)

## Sort

-   [75. Sort Colors](./Sort/75.sort-colors.md)
-   [88. Merge Sorted Array](./Sort/88.merge-sorted-array.md)

## DFS

-   [94. Binary Tree Inorder Traversal](./DFS/94.binary-tree-inorder-traversal.md)
-   [100. Same Tree](./DFS/100.same-tree.md)
-   [101. Symmetric Tree](./DFS/101.symmetric-tree.md)
-   [104. Maximum Depth of Binary Tree](./DFS/104.maximum-depth-of-binary-tree.md)
-   [112. Path Sum](./DFS/112.path-sum.md)
-   [114. Flatten Binary Tree to Linked List](./DFS/114.flatten-binary-tree-to-linked-list.md)

## Binary-Tree

-   [108. Convert Sorted Array to Binary Search Tree](./Binary-Tree/108.convert-sorted-array-to-binary-search-tree.md)
-   [109. Convert Sorted List to Binary Search Tree](./Binary-Tree/109.convert-sorted-list-to-binary-search-tree.md)
-   [105. Construct Binary Tree from Preorder and Inorder Traversal(困難)](./Binary-Tree/105.construct-binary-tree-from-preorder-and-inorder-traversal.md)
-   [106. Construct Binary Tree from Inorder and Postorder Traversal(困難)](./Binary-Tree/106.construct-binary-tree-from-inorder-and-postorder-traversal.md)
-   [110. Balanced Binary Tree](./Binary-Tree/110.balanced-binary-tree.md)
-   [111. Minimum Depth of Binary Tree](./Binary-Tree/111.minimum-depth-of-binary-tree.md)

## Stack

-   [20. Valid Parentheses](./Stack/20.valid-parentheses.md)

## BFS

-   [102. Binary Tree Level Order Traversal](./BFS/102.binary-tree-level-order-traversal.md)
-   [107. Binary Tree Level Order Traversal II](./BFS/107.binary-tree-level-order-traversal-ii.md)
-   [103. Binary Tree Zigzag Level Order Traversal](./BFS/103.binary-tree-zigzag-level-order-traversal.md)
-   [116. Populating Next Right Pointers in Each Node](./BFS/116.populating-next-right-pointers-in-each-node.md)

## Linked List

-   [2. Add Two Numbers](./Linked-List/2.add-two-numbers.md)
-   [19. Remove Nth Node From End of List](./Linked-List/19.remove-nth-node-from-end-of-list.md)
-   [21. Merge Two Sorted Lists](./Linked-List/21.merge-two-sorted-lists.md)
-   [24. Swap Nodes in Pairs](./Linked-List/24.swap-nodes-in-pairs.md)
-   [83. Remove Duplicates from Sorted List](./Linked-List/83.remove-duplicates-from-sorted-list.md)
-   [86. Partition List](./Linked-List/86.partition-list.md)

## Sliding Window

-   [3. Longest Substring Without Repeating Characters](./Sliding-Window/3.longest-substring-without-repeating-characters.md)

## String

-   [6. Zigzag Conversion](./String/6.zigzag-conversion.md)
-   [38. Count and Say](./String/38.count-and-say.md)
-   [58. Length of Last Word](./String/58.length-of-last-word.md)
-   [67. Add Binary](./String/67.add-binary.md)

### 前墜合

-   [14. Longest Common Prefix](./String/14.longest-common-prefix.md)

## Math

### 判斷回文

-   [9. Palindrome Number](./Math/9.palindrome-number.md)

### 羅馬數字互轉

-   [12. Integer to Roman](./Math/12.integer-to-roman.md)
-   [13. Roman to Integer](./Math/13.roman-to-integer.md)

## Greddy

-   [11. Container With Most Water](./Greddy/11.container-with-most-water.md)

## Bit Manipulation

-   [89. Gray Code](./Bit-Manipulation/89.gray-code.md)

## Backtracking

```cpp
// 模板
void backtrack(大集合(最後要返回的), 當前收集的小字串, 進度等等){
        // 終止條件：當遍歷完整個數字字串時，
        if(...){
            return;
        }

        // 取得當前數字對應的字母
        string temp_string = m[digits[index]];
        for(...){
            // 放進去
            // 遞迴
            // 拔出來
        }
    }
```

-   [17. Letter Combinations of a Phone Number](./Backtracking/17.letter-combinations-of-a-phone-number.md)
-   [22. Generate Parentheses](./Backtracking/22.generate-parentheses.md)
-   [39. Combination Sum](./Backtracking/39.combination-sum.md)
-   [40. Combination Sum II](./Backtracking/40.combination-sum-ii.md)
-   [46. Permutations](./Backtracking/46.permutations.md)
-   [47. Permutations II](./Backtracking/47.permutations-ii.md)
-   [77. Combinations](./Backtracking/77.combinations.md)
-   [78. Subsets](./Backtracking/78.subsets.md)
-   [113. Path Sum II](./Backtracking/113.path-sum-ii.md)

## DP

-   [118. Pascal's Triangle](./DP/118.pascal's-triangle.md)
-   [11\*. Pascal's Triangle II](./DP/119.pascal's-triangle-ii.md)
-   [53. Maximum Subarray](./DP/53.maximum-subarray.md)
-   [62. Unique Paths](./DP/62.unique-paths.md)
-   [64. Minimum Path Sum](./DP/64.minimum-path-sum.md)
-   [70. Climbing Stairs](./DP/70.climbing-stairs.md)
-   [72. Edit Distance](./DP/72.edit-distance.md)
-   [96. Unique Binary Search Trees](./DP/96.unique-binary-search-trees.md)
-   [95. Unique Binary Search Trees II](./DP/95.unique-binary-search-trees-ii.md)
