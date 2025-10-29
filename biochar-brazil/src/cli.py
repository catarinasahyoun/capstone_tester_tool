import argparse
from src.config import load_config
from src.data.loader import load_data
from src.analysis.suitability import calculate_suitability
from src.visualization.plots import plot_results

def main():
    parser = argparse.ArgumentParser(description='Biochar Application Suitability Tool')
    parser.add_argument('--config', type=str, help='Path to the configuration file', default='configs/config.yaml')
    parser.add_argument('--output', type=str, help='Output directory for results', default='results/')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Load data
    data = load_data(config['data_sources'])
    
    # Calculate suitability
    suitability_scores = calculate_suitability(data, config['suitability_criteria'])
    
    # Plot results
    plot_results(suitability_scores, args.output)

if __name__ == '__main__':
    main()