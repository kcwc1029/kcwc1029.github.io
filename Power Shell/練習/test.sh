#!/bin/bash

word=applebanana

# 從第 2 個位置 (第三個字元 'p') 開始，取 5 個字元
getout=${word:2:5}

echo $getout # pleba