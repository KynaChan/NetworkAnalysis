
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as accuracy_score


class ModelEvaluator:
    def __init__(self, model, test_data):
        self.model = model
        self.test_data = test_data

    def evaluate(self):
        # Placeholder for evaluation logic
        # This could include accuracy, precision, recall, etc.
        pass

    def get_metrics(self):
        # Placeholder for returning evaluation metrics
        pass

    # bar chart comparing ground truth and predicted labels
    def visualise_model_performance(model_type, pred_labels, target_labels):
        """
        A general method to visualize performance of any model (RF or IF) in a bar chart.

        :param model_type: str, "Random Forest" or "Isolation Forest"
        :param pred_labels: Predicted labels from the model
        :param true_labels: Ground truth labels
        """
        # Convert to Series for consistency
        pred_series = pd.Series(pred_labels)
        true_series = pd.Series(target_labels)

        # Count occurrences of each label
        pred_counts = pred_series.value_counts()
        true_counts = true_series.value_counts()

        # Ensure both Series have the same index (add missing labels if needed)
        all_labels = sorted(set(pred_counts.index).union(true_counts.index))
        pred_counts = pred_counts.reindex(all_labels, fill_value=0)
        true_counts = true_counts.reindex(all_labels, fill_value=0)

        # Bar positions
        x = np.arange(len(all_labels))
        width = 0.35  # width of each bar

        # Create the plot
        plt.figure(figsize=(10, 6))
        bars_gt = plt.bar(x - width/2, true_counts, width=width, label='Ground Truth', color='lightgreen')
        bars_pred = plt.bar(x + width/2, pred_counts, width=width, label='Predicted', color='cornflowerblue')

        for bar in bars_gt:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                     str(int(bar.get_height())), ha='center', va='bottom')

        for bar in bars_pred:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                     str(int(bar.get_height())), ha='center', va='bottom')

        # Set titles and labels
        title = f"Comparison of Ground Truth vs Predictions ({model_type})"
        plt.xlabel('Class Labels')
        plt.ylabel('Count')
        plt.title(title)
        plt.xticks(ticks=x, labels=all_labels, rotation=45)
        plt.legend()

        plt.tight_layout()
        plt.savefig(title.replace(" ", "_") + ".png")
        plt.show()


def compare_model_accuracies(model_name,target_labels,predictions_dict):
    """
    Plots accuracy comparison for models using different feature sets.
    
    Parameters:
    - model_name (str): 'Isolation Forest' or 'Random Forest'
    - true_labels (Series): Ground truth labels.
    - predictions_dict (dict): Keys are model variants (e.g., 'Original', 'Common'), 
                               values are predicted labels (Series or array).

    Example:
    >>> compare_model_accuracies(model_name="Isolation Forest",true_labels=target_label_list,
        predictions_dict={
            'Original': if_pred_result['if_anomaly'],
            'Common Features': if_common_preds['if_pred'],
            'Combined Features': if_combine_preds['if_pred'],
            'IF-only Features': if_only_preds['if_pred']
            }
        )

    >>> compare_model_accuracies(model_name="Random Forest",true_labels=y_test,
        predictions_dict={
            'Original Features': rf_test_pred,
            'Common Features': rf_common_preds,
            'Combined Features': rf_combine_preds,
            'RF-only Features': rf_only_preds
            }
        )
    """
    labels = list(predictions_dict.keys())
    accuracies = [
        accuracy_score(target_labels, predictions_dict[label]) for label in labels
    ]

    x = np.arange(len(labels))
    width = 0.6

    plt.figure(figsize=(10, 6))
    bars = plt.bar(x, accuracies, color='cornflowerblue')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01,
                 f'{height:.2f}', ha='center', va='bottom')

    title = f"Accuracy Comparison of {model_name} Models\n(with different feature sets)"
    plt.xticks(ticks=x, labels=labels, rotation=15)
    plt.ylim(0, 1.05)
    plt.ylabel("Accuracy")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(title.replace(" ", "_") + ".png")
    plt.show()