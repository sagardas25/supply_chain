import joblib
import os

def load_model():
    """
    Load the saved XGBoost model and feature columns from disk.
    
    Returns:
        model: The loaded XGBoost model.
        X_columns: The list of feature column names used for training.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(dir_path, "xgb_model.pkl")
    columns_path = os.path.join(dir_path, "xgb_model_columns.pkl")
    
    model = joblib.load(model_path)
    X_columns = joblib.load(columns_path)
    
    return model, X_columns