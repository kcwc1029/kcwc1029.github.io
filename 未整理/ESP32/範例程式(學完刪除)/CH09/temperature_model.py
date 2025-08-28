# 讀取 temperature.txt 
import keras_lite_convertor as kc

path_name = 'temperature.txt'
Data_reader = kc.Data_reader(path_name, mode='regression')
data, label = Data_reader.read()

# 資料預處理
# 取資料中的 85% 當作訓練集
split_num = int(len(data)*0.85) 
train_data = data[:split_num]
train_label = label[:split_num]    

# 正規化
mean = train_data.mean() # 平均數
data -= mean
std = train_data.std()   # 標準差
data /= std

label /= 100     # 將 label範圍落在 0~1 (label正規化)

# 訓練集、驗證集、測試集的資料形狀
# 訓練集
print(train_data.shape)    

# 驗證集
validation_data = data[split_num:-5]    
print(validation_data.shape)
validation_label = label[split_num:-5]   

# 測試集
test_data = data[-5:]     
print(test_data.shape)
test_label = label[-5:] 

# 建立神經網路架構
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

model = Sequential()

# 增加一個密集層, 使用ReLU激活函數, 輸入層有1個輸入特徵 
model.add(layers.Dense(20, activation='relu', 
                       input_shape=(1,)))  
model.add(layers.Dense(20, activation='relu'))
model.add(layers.Dense(20, activation='relu'))
model.add(layers.Dense(1))
model.summary()    # 顯示模型資訊

# 編譯及訓練模型
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
train_history = model.fit(
    train_data, train_label,  # 測試集
    validation_data=(validation_data,
    validation_label),        # 驗證集
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
kc.save(model,'temperature_model.json')

# 顯示正規化相關資訊
print('mean =',mean)
print('std =',std)