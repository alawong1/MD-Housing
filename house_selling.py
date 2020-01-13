import pandas as pd 
import numpy as np 
import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics as metrics

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation

EPOCHS = 100

df = pd.read_csv("md_housing.csv")

df["Basement"].replace(["HasBasement:", "BasementType:", "None basement"], "None", inplace=True)
df["Basement"].replace("Basement:", "Finished basement", inplace=True)
df["ConstructMat1"].replace("T-1-11", "Wood Siding", inplace=True)
df["ConstructMat2"].replace("T-1-11", "Wood Siding", inplace=True)
df["ExteriorFeat1"].replace("View Type", "Water", inplace=True)

df.drop(["Address", "ListingURL"], axis=1, inplace=True)

df = df.drop(df[df["SalePrice"] > 3000000].index).reset_index(drop=True)
df = df.drop(df[df["SalePrice"] < 10000].index).reset_index(drop=True)

for c in df.columns:
    if df[c].dtype == 'object':
        lbl = LabelEncoder()
        lbl.fit(list(df[c].values))
        df[c] = lbl.transform(list(df[c].values))

X = df.drop(["id", "SalePrice"], axis=1)
y = df["SalePrice"]

X = (X - X.mean())/X.std()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print()
print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_test shape: {y_test.shape}")
print()

model = Sequential()

# Input layer
model.add(Dense(64, input_shape=[X_train.shape[1]]))
model.add(Activation("relu"))

# Hidden Layer 1
model.add(Dense(128))
model.add(Activation("relu"))
model.add(Dropout(0.05))

# Hidden Layer 2
model.add(Dense(128))
model.add(Activation("relu"))
model.add(Dropout(0.10))

# Hidden Layer 3
model.add(Dense(64))
model.add(Activation("relu"))
model.add(Dropout(0.10))

# Hidden Layer 4
model.add(Dense(32))
model.add(Activation("relu"))
model.add(Dropout(0.025))

# Hidden Layer 5
model.add(Dense(32))
model.add(Activation("relu"))
model.add(Dropout(0.025))

# Output layer
model.add(Dense(1))

optimizer = tf.keras.optimizers.RMSprop(0.001)
model.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])

model_history = model.fit(X_train, y_train, epochs=EPOCHS, validation_split=0.2, batch_size=32, verbose=1)

loss2, mae, mse = model.evaluate(X_test, y_test, verbose=2)
print("Testing set Mean Abs Error: ${:5.2f}".format(mae))
