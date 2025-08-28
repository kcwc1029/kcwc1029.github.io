# 讀取 ppg_classification
import keras_lite_convertor as kc
 
path = 'ppg_classification'

Data_reader = kc.Data_reader(
    path, 
    mode='binary',       # binary 適用於二元分類
    label_name=['others', 'ppg'])   # 標籤名稱
data, label = Data_reader.read()


# 資料預處理
# 取資料中的 80% 當作訓練集
split_num = int(len(data)*0.8) 
train_data=data[:split_num]
train_label=label[:split_num]    

# 正規化
mean = train_data.mean() # 平均數
data -= mean
std = train_data.std()   # 標準差
data /= std
  
# 驗證集
validation_data=data[split_num:-5]  
validation_label=label[split_num:-5]   

# 測試集
test_data=data[-5:]     
test_label=label[-5:]

# %% 建立神經網路架構
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

model = Sequential()
model.add(layers.Reshape((300, 1), input_shape=(300,)))
model.add(layers.Conv1D(4, 3, activation='relu', 
                        padding='valid'))       # 卷積層
model.add(layers.MaxPooling1D())                # 池化層  
model.add(layers.Conv1D(4, 3, activation='relu',
                        padding='valid'))
model.add(layers.MaxPooling1D())
model.add(layers.Conv1D(8, 3, activation='relu',
                        padding='valid'))
model.add(layers.MaxPooling1D())
model.add(layers.Flatten())   # 展平層
model.add(layers.Dense(
    1, activation='sigmoid')) # 輸出層的啟動函數為 sigmoid


# 編譯及訓練模型
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy'])

train_history = model.fit(
    train_data, train_label,    # 訓練集
    validation_data=(           # 驗證集
        validation_data, validation_label), 
    epochs=200)                 # 訓練週期為200


# 測試模型
print('prediction:')
print(model.predict(test_data))
print()
print('groundtruth:')
print(test_label)


# 儲存模型
kc.save(model, 'ppg_model.json')


# 輸出平均數與標準差
print('mean =', mean)
print('std =', std)