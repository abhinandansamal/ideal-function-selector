import yaml
from src.ideal_function_selector.database.database import DatabaseHandler, TrainingData, IdealFunctions, TestData
from src.ideal_function_selector.components.data_loader import DataLoader
from src.ideal_function_selector.components.data_processor import DataProcessor
from src.ideal_function_selector.components.data_visualizer import DataVisualizer



def main():
    """
    Main function to load data, process it, and visualize the results.
    """
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    
    db_filename = config['database']['filename']
    db_handler = DatabaseHandler(db_filename)
    data_loader = DataLoader(db_handler)
    
    train_data_path = config['data_paths']['train_data']
    ideal_data_path = config['data_paths']['ideal_data']
    test_data_path = config['data_paths']['test_data']
    
    data_loader.load_csv_to_db(train_data_path, TrainingData)
    data_loader.load_csv_to_db(ideal_data_path, IdealFunctions)
    data_loader.load_csv_to_db(test_data_path, TestData)
    
    processor = DataProcessor(db_handler)
    best_fit_functions = processor.find_best_fit_functions()
    processor.map_test_data(best_fit_functions)
    
    visualizer = DataVisualizer(db_handler)
    visualizer.visualize_data()

if __name__ == "__main__":
    main()
