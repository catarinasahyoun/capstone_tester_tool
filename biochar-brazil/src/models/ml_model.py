from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

class MLModel:
    def __init__(self, data):
        self.data = data
        self.model = RandomForestRegressor()
        self.features = None
        self.target = None

    def prepare_data(self, feature_columns, target_column):
        self.features = self.data[feature_columns]
        self.target = self.data[target_column]

    def train(self, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.target, test_size=test_size, random_state=random_state)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        return mse

    def predict(self, new_data):
        return self.model.predict(new_data)

    def feature_importance(self):
        return self.model.feature_importances_