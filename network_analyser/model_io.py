import joblib


class ModelIO:
    # Save the model to the specified file path
    def save_model(self, model, file_path):  # the TryCatch should i do it here or in main
        joblib.dump(model, file_path)
        print(f"\n  [SUCCESS] Model saved to {file_path}\n")

    # Load the model from the specified file path
    def load_model(self, file_path):
        model = None
        model = joblib.load(file_path)
        print(f"\n  [SUCCESS] Model loaded from {file_path}\n")
        return model
