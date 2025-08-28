# 讀取 pwtt_bp.txt 
import keras_lite_convertor as kc

path_name = 'pwtt_bp.txt'
Data_reader = kc.Data_reader(path_name, mode='regression')
data, label = Data_reader.read()


# 資料預處理
# 正規化
data /= 200
label /= 100

# 取資料中的 85% 當作訓練集
split_num = int(len(data)*0.85) 
train_data = data[:split_num]
train_label = label[:split_num]    

# 驗證集
validation_data = data[split_num:-5]
validation_label = label[split_num:-5]

# 測試集
test_data = data[-5:]
test_label = label[-5:]


# 建立神經網路架構
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

model = Sequential()
# 增加一個密集層, 使用ReLU激活函數
model.add(layers.Dense(20, activation='relu', 
                       input_shape=(1,)))# 輸入層有1個輸入特徵  
model.add(layers.Dense(20, activation='relu'))
model.add(layers.Dense(20, activation='relu'))
model.add(layers.Dense(1))


# 編譯及訓練模型
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
train_history = model.fit(
    train_data, train_label,  # 測試集
    validation_data=(validation_data, validation_label),
    epochs=1000)              # 訓練週期


# 測試模型
# 預測值
print('prediction:')
print(model.predict(test_data))
print()
# 實際值
print('groundtruth:')
print(test_label)


# 儲存模型
# kc.save(model,'bp_model.json')