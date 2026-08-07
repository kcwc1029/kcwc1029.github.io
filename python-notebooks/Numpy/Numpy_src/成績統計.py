import numpy as np

# 假設這是 10 位學員的 Python、SQL、Excel 三科成績。
# 每一列是一位學員，每一欄是一個科目。
scores = np.array(
    [
        [82, 76, 90],
        [68, 88, 72],
        [95, 91, 84],
        [73, 69, 78],
        [88, 85, 92],
        [60, 70, 66],
        [79, 81, 75],
        [92, 89, 96],
        [55, 63, 70],
        [84, 77, 88],
    ]
)

subject_names = np.array(["Python", "SQL", "Excel"])

print("每位學員平均分數:", scores.mean(axis=1))
print("每個科目平均分數:", scores.mean(axis=0))
print("每個科目最高分:", scores.max(axis=0))
print("每個科目最低分:", scores.min(axis=0))

best_subject_index = scores.mean(axis=0).argmax()
print("平均最高的科目:", subject_names[best_subject_index])

