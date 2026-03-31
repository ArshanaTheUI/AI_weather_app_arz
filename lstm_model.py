import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Sample data
temps = [30, 32, 34, 35, 37, 36, 38, 39]

X = []
y = []

window = 3

for i in range(len(temps) - window):
    X.append(temps[i:i+window])
    y.append(temps[i+window])

X = np.array(X)
y = np.array(y)

# reshape for LSTM
X = X.reshape((X.shape[0], X.shape[1], 1))

model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(window, 1)))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

model.fit(X, y, epochs=100, verbose=0)

# 🔥 THIS CREATES FILE
model.save("lstm_model.h5")

print("Model saved ✅")