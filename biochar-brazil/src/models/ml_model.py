"""
Machine Learning model for predicting biochar suitability or related outcomes.
Integrates with data pipeline for the Biochar-Brazil project.
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
import joblib
from pathlib import Path


class MLModel:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.model = RandomForestRegressor(random_state=42)
        self.features = None
        self.target = None
        self.trained = False

    def prepare_data(self, feature_columns: list[str] = None, target_column: str = None):
        """
        Prepare feature and target data for training.
        If no feature_columns are given, use all numeric columns except target.
        """
        if target_column is None:
            raise ValueError("You must specify a target column for training.")

        if feature_columns is None:
            feature_columns = [c for c in self.data.select_dtypes(include=[np.number]).columns if c != target_column]

        self.features = self.data[feature_columns].fillna(0)
        self.target = self.data[target_column].fillna(0)
        print(f"Prepared data with {len(self.features.columns)} features.")
        return self.features, self.target

    def train(self, test_size=0.2, random_state=42, save_path: str = "data/processed/ml_model.pkl"):
        """
        Train the model and save it to disk.
        """
        if self.features is None or self.target is None:
            raise RuntimeError("Data not prepared. Call prepare_data() first.")

        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.target, test_size=test_size, random_state=random_state
        )

        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)

        mse = mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        self.trained = True
        joblib.dump(self.model, Path(save_path))

        print(f"✅ Model trained. MSE = {mse:.3f}, R² = {r2:.3f}")
        print(f"Model saved to {save_path}")
        return mse, r2

    def predict(self, new_data: pd.DataFrame):
        """
        Predict new outcomes using the trained model.
        """
        if not self.trained:
            raise RuntimeError("Model not trained. Train or load a model first.")

        new_data = new_data.fillna(0)
        return self.model.predict(new_data)

    def feature_importance(self):
        """
        Return feature importance as a sorted DataFrame.
        """
        importance = pd.DataFrame({
            "feature": self.features.columns,
            "importance": self.model.feature_importances_
        }).sort_values("importance", ascending=False)
        return importance

    def load(self, model_path: str = "data/processed/ml_model.pkl"):
        """
        Load a pre-trained model from disk.
        """
        self.model = joblib.load(model_path)
        self.trained = True
        print(f"✅ Loaded model from {model_path}")
