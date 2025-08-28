# %% 讀取資料
import keras_lite_convertor as kc

path_name = 'heart_risk.txt'
Data_reader = kc.Data_reader(path_name, mode='regression')
data, label = Data_reader.read(random_seed=12)
pass

# %% 資料分割-訓練集
split_num = int(len(data)*0.9)
train_data = data[:split_num]
train_label = label[:split_num]
pass

# %% 資料正規化
# 特徵資料正規化(標準化)
mean = train_data.mean(axis=0)
std = train_data.std(axis=0)

data -= mean
data /= std

# 標籤正規化(最大值正規化)
label /= 100
pass

# %% 查看資料集的形狀
# 訓練集
train_data = data[:split_num] # 訓練用資料
print(train_data.shape)
train_label = label[:split_num] # 訓練用標籤
# 驗證集
validation_data=data[split_num:-30] # 驗證用資料
print(validation_data.shape)
validation_label=label[split_num:-30] # 驗證用標籤
# 測試集
test_data=data[-30:] # 測試用資料,30 筆
print(test_data.shape)
test_label=label[-30:] # 測試用標籤
pass

# %% 建立神經網路架構
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential() # 建立序列模型
model.add(Dense(200, activation='relu', # 增加一層神經層
input_shape=(9, )))
model.add(Dense(200, activation='relu')) # 增加一層神經層
model.add(Dense(1))
model.summary()
pass

# %% 編譯及訓練模型
model.compile(
    optimizer='adam', loss='mse', metrics=['mae'])

history=model.fit(
    train_data, train_label, # 訓練集
    validation_data=(validation_data, validation_label), # 驗證集
    epochs=300)
pass

# %% 測試模型
prediction = model.predict(test_data)

# 預測值
print('prediction:')
print(prediction*100)
print()
# 實際值
print('ground truth:')
print(test_label*100)
print()
# 誤差值
print('error:')
print(test_label*100 - prediction*100)