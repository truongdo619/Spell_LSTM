from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam, RMSprop


dataset = loadtxt("pima-indians-diabetes.csv", delimiter=",")
X = dataset[:, 0:8]
Y = dataset[:, 8]
model = Sequential()
model.add(Dense(12, input_dim=8, activation="relu"))
model.add(Dense(8, activation="relu"))
model.add(Dense(1, activation="sigmoid"))
optimizer=Adam()
model.compile(loss="binary_crossentropy" ,optimizer=optimizer, metrics=['accuracy'])
model.fit(X, Y, epochs=150, batch_size=10, verbose=0)
_, accuracy = model.evaluate(X, Y)
print("Accuracy %.2f" %(accuracy * 100))
predcitions = model.predict_classes(X)
for i in range(5):
    print("%s => %d ( expected %d )" %(X[i], predcitions[i], Y[i]))