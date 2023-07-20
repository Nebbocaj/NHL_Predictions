
import numpy as np
from sklearn.linear_model import LinearRegression

def linear_regression_prediction(x_train, y_train, x_test):
    # Create a linear regression model
    model = LinearRegression()

    # Reshape x_train and y_train if they are 1D arrays
    x_train = np.array(x_train).reshape(-1, 1)
    y_train = np.array(y_train)

    # Train the model with the given data
    model.fit(x_train, y_train)

    # Reshape x_test if it is a 1D array
    x_test = np.array(x_test).reshape(-1, 1)

    # Make predictions on the test data
    y_pred = model.predict(x_test)

    return y_pred

# Example usage:
x_train = [0, 1, 2, 3, 4, 5, 6, 7]
y_train = [16, 30, 41, 41, 34, 33, 44, 64]
x_test = [len(x_train)]

predictions = linear_regression_prediction(x_train, y_train, x_test)
print(predictions)