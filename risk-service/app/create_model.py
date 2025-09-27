import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

def create_and_save_model():
    """
    Creates a simple Isolation Forest model and saves it to a file.
    This simulates a pre-trained model being available for the service.
    """
    # Create some dummy data for training
    # In a real scenario, this would be historical transaction data
    rng = np.random.RandomState(42)
    X_train = 0.2 * rng.randn(1000, 2)
    X_train = np.r_[X_train, rng.uniform(low=-5, high=5, size=(50, 2))]

    # Create and train the model
    model = IsolationForest(contamination='auto', random_state=42)
    model.fit(X_train)

    # Save the model to the 'models' directory
    model_path = "app/models/isolation_forest.joblib"
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    create_and_save_model()