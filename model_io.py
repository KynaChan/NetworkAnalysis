
import joblib


class ModelIO:
    
    # def __init__(self):
    #     pass

    # Save the model to the specified file path
    def save_model(self, model, file_path): # the TryCatch should i do it here or in main
        try:
            joblib.dump(model, file_path)
            print(f"\n  [SUCCESS] Model saved to {file_path}\n")
        except FileNotFoundError:
            print(f"\n  [ERROR] File not found: {file_path}\n")
        except Exception as e:
            print(f"\n  [ERROR] An error occurred while saving the model: {e}\n")   



    # Load the model from the specified file path
    def load_model(self, file_path):
        try:
            model = joblib.load(file_path)
            print(f"\n  [SUCCESS] Model loaded from {file_path}\n")
        except FileNotFoundError:
            print(f"\n  [ERROR] File not found: {file_path}\n")
        except Exception as e:
            print(f"\n  [ERROR] An error occurred while loading the model: {e}\n")
            model = None
            
        # Return the loaded model
        return model