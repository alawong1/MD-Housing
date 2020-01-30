import pandas as pd 
import numpy as np
import time
import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn

from sklearn.preprocessing   import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model    import LinearRegression
from sklearn.ensemble        import RandomForestRegressor, GradientBoostingRegressor
from sklearn                 import metrics as metrics

import tensorflow as tf
from tensorflow.keras.models    import Sequential
from tensorflow.keras.layers    import Dense, Dropout, Activation
from tensorflow.keras           import regularizers

EPOCHS = 400

df = pd.read_csv("md_house_data.csv")

# Reduce the memory size of the dataframe for faster calculations.
float_cols = ("TotalLivArea", "PriceSqft", "Stories", "YearBuilt", "LotSize")
int_cols   = ("Bathrooms", "Bedrooms", "FullBaths", "HalfBaths", "SalePrice")

for fcol in float_cols:
    df[fcol] = df[fcol].astype("float32")

for icol in int_cols:
     df[icol] = df[icol].astype("int32")

df.drop(["Address", "ListingURL"], axis=1, inplace=True)

df = df.drop(df[df["SalePrice"] > 1500000].index).reset_index(drop=True)
df = df.drop(df[df["SalePrice"] < 10000].index).reset_index(drop=True)

for c in df.columns:
    if df[c].dtype == 'object':
        lbl = LabelEncoder()
        lbl.fit(list(df[c].values))
        df[c] = lbl.transform(list(df[c].values))

X = df.drop(["ids", "SalePrice"], axis=1)
y = df["SalePrice"]

# Normalize the dataset to make calculations easier.
# Use normalization when the dataset consists of a large range of numbers.
X = (X - X.mean())/X.std()
X.head()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

''' -- Linear Regression -- '''
linear_reg = LinearRegression(n_jobs=-1)
linear_reg.fit(X_train, y_train)
y_linear_pred = linear_reg.predict(X_test)

linear_acc = linear_reg.score(X_test, y_test)

''' -- Random Forest Regression -- '''
rf_reg = RandomForestRegressor(min_samples_split=4, min_samples_leaf=1, n_estimators=100, n_jobs=-1, random_state=42)
rf_reg.fit(X_train, y_train)

y_rf_pred = rf_reg.predict(X_test)
rf_acc = rf_reg.score(X_test, y_test)

''' -- Gradient Boost Regression -- '''
gb_reg = GradientBoostingRegressor(learning_rate=0.1, n_estimators=100, min_samples_split=8, random_state=42)
gb_reg.fit(X_train, y_train)

y_gb_pred = gb_reg.predict(X_test)
gb_acc = gb_reg.score(X_test, y_test)

''' -- Neural Network -- '''
# Input layer
model = Sequential()

model.add(Dense(64, kernel_regularizer=regularizers.l2(0.060), input_shape=[X_train.shape[1]]))
model.add(Activation("elu"))

# Hidden Layer 1
model.add(Dense(256, kernel_regularizer=regularizers.l2(0.060)))
model.add(Activation("elu"))
model.add(Dropout(0.15))

# Hidden Layer 2
model.add(Dense(128, kernel_regularizer=regularizers.l2(0.060)))
model.add(Activation("elu"))
model.add(Dropout(0.15))

# Hidden Layer 3
model.add(Dense(64, kernel_regularizer=regularizers.l2(0.060)))
model.add(Activation("elu"))
model.add(Dropout(0.08))

# Hidden Layer 4
model.add(Dense(64, kernel_regularizer=regularizers.l2(0.060)))
model.add(Activation("elu"))
model.add(Dropout(0.08))

# Hidden Layer 5
model.add(Dense(128, kernel_regularizer=regularizers.l2(0.060)))
model.add(Activation("elu"))
model.add(Dropout(0.15))

# Output layer
model.add(Dense(1))

# optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.001, rho=0.88)
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])    

last_time = time.time()
model_history = model.fit(X_train, y_train, epochs=EPOCHS, validation_split=0.2, batch_size=32, verbose=1)
# model.save("nn_house_model.h5")
print("\nModel took approximately {:5.2f} seconds to train.".format(time.time() - last_time))

loss2, mae, mse = model.evaluate(X_test, y_test, verbose=2)

print("\nLinear Regression:")
print("Accuracy: {:5.7f}".format(linear_acc))
print("Mean Absolute Error:     ${:5.2f}".format( metrics.mean_absolute_error(y_test, y_linear_pred)) )
print("Mean Squared Error:      ${:5.2f}".format( metrics.mean_squared_error(y_test, y_linear_pred)) )
print("Root Mean Squared Error: ${:5.2f}".format( np.sqrt(metrics.mean_squared_error(y_test, y_linear_pred))) )

print("\nRandom Forest Regression:")
print("Accuracy: {:5.7f}".format(rf_acc))
print("Mean Absolute Error:     ${:5.2f}".format( metrics.mean_absolute_error(y_test, y_rf_pred) ))
print("Mean Squared Error:      ${:5.2f}".format( metrics.mean_squared_error(y_test, y_rf_pred)) )
print("Root Mean Squared Error: ${:5.2f}".format( np.sqrt(metrics.mean_squared_error(y_test, y_rf_pred))))

print("\nGradient Boosting Regression:")
print("Accuracy: {:5.7f}".format(gb_acc))
print("Mean Absolute Error:     ${:5.2f}".format( metrics.mean_absolute_error(y_test, y_gb_pred) ))
print("Mean Squared Error:      ${:5.2f}".format( metrics.mean_squared_error(y_test, y_gb_pred)) )
print("Root Mean Squared Error: ${:5.2f}".format( np.sqrt(metrics.mean_squared_error(y_test, y_gb_pred))))

print("\nNeural Network:")
print("Accuracy: Not applicable")
print("Mean Absolute Error:     ${:5.2f}".format( mae ))
print("Mean Squared Error:      ${:5.2f}".format( mse ))
print("Root Mean Squared Error: ${:5.2f}".format( np.sqrt(mse)))