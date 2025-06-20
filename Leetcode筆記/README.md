## array

-   [26. Remove Duplicates from Sorted Array](./Array/26.remove-duplicates-from-sorted-array.md)
-   [27. Remove Element](./Array/27.remove-element.md)

## Matrix

-   [36. Valid Sudoku](./Matrix/36.valid-sudoku.md)
-   [48. Rotate Image](./Matrix/48.rotate-image.md)

## Hash Table

-   [1. Two Sum](./Hash-Table/1.two-sum.md)

## Binary Search

-   [35. Search Insert Position](./Binary-Search/35.search-insert-position.md)

## Stack

-   [20. Valid Parentheses](./Stack/20.valid-parentheses.md)

## Linked List

-   [2. Add Two Numbers](./Linked-List/2.add-two-numbers.md)
-   [19. Remove Nth Node From End of List](./Linked-List/19.remove-nth-node-from-end-of-list.md)
-   [21. Merge Two Sorted Lists](./Linked-List/21.merge-two-sorted-lists.md)
-   [24. Swap Nodes in Pairs](./Linked-List/24.swap-nodes-in-pairs.md)

## Sliding Window

-   [3. Longest Substring Without Repeating Characters](./Sliding-Window/3.longest-substring-without-repeating-characters.md)

## String

-   [6. Zigzag Conversion](./String/6.zigzag-conversion.md)
-   [38. Count and Say](./String/38.count-and-say.md)

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
