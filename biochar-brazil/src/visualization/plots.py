from matplotlib import pyplot as plt
import seaborn as sns

def plot_suitability_scores(suitability_data):
    plt.figure(figsize=(10, 6))
    sns.histplot(suitability_data, bins=30, kde=True)
    plt.title('Distribution of Suitability Scores for Biochar Application')
    plt.xlabel('Suitability Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig('suitability_scores_distribution.png')
    plt.close()

def plot_risk_assessment(risk_data):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Risk Factor', y='Value', data=risk_data)
    plt.title('Risk Assessment for Biochar Application')
    plt.xlabel('Risk Factor')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('risk_assessment_plot.png')
    plt.close()

def plot_aggregated_scores(aggregated_data):
    plt.figure(figsize=(12, 8))
    sns.heatmap(aggregated_data, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Aggregated Suitability Scores by Region')
    plt.xlabel('Region')
    plt.ylabel('Score')
    plt.tight_layout()
    plt.savefig('aggregated_scores_heatmap.png')
    plt.close()