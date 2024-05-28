import unittest
import pandas as pd
import sys
import os
import logging
from src.ideal_function_selector.database.database import DatabaseHandler, TrainingData, IdealFunctions, TestData, MappedTestData
from src.ideal_function_selector.components.data_loader import DataLoader
from src.ideal_function_selector.components.data_processor import DataProcessor
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the src directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
# src_path = os.path.join(current_dir, '..', 'src')
# sys.path.append(src_path)

class TestDataProcessor(unittest.TestCase):
    """
    Unit tests for the DataProcessor class.
    """
    def setUp(self):
        """
        Set up the in-memory database and data loader for testing.
        """
        self.db_handler = DatabaseHandler(':memory:')
        self.data_loader = DataLoader(self.db_handler)
        self.processor = DataProcessor(self.db_handler)  # Initialize DataProcessor

        # Store temp files in current test directory
        self.test_data_dir = current_dir
        
        # Sample data to simulate the content of CSV files
        training_data = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y1': [1.1, 2.2, 3.3],
            'y2': [1.2, 2.3, 3.4],
            'y3': [1.3, 2.4, 3.5],
            'y4': [1.4, 2.5, 3.6]
        })
        
        # Simulating the structure of your ideal.csv file
        ideal_data = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y_values': [
                ','.join(map(str, [1.1, 1.2, 1.3, 1.4])),
                ','.join(map(str, [2.1, 2.2, 2.3, 2.4])),
                ','.join(map(str, [3.1, 3.2, 3.3, 3.4]))
            ]
        })

        test_data = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y': [1.0, 2.1, 3.4]
        })

        # Paths to temporary CSV files
        self.temp_train_csv = os.path.join(self.test_data_dir, 'temp_train_2.csv')
        self.temp_ideal_csv = os.path.join(self.test_data_dir, 'temp_ideal_2.csv')
        self.temp_test_csv = os.path.join(self.test_data_dir, 'temp_test_2.csv')

        # Saving sample data to temporary CSV files
        training_data.to_csv(self.temp_train_csv, index=False)
        ideal_data.to_csv(self.temp_ideal_csv, index=False)
        test_data.to_csv(self.temp_test_csv, index=False)

        # Load data into the database
        self.data_loader.load_csv_to_db(self.temp_train_csv, TrainingData)
        self.data_loader.load_csv_to_db(self.temp_ideal_csv, IdealFunctions)
        self.data_loader.load_csv_to_db(self.temp_test_csv, TestData)

    def test_find_best_fit_functions(self):
        """
        Test if the best fit functions are found correctly.
        """
        best_fit_functions = self.processor.find_best_fit_functions()
        # Add assertions to check if the functions are selected correctly
        self.assertIsNotNone(best_fit_functions)
        self.assertEqual(len(best_fit_functions), 4)  # Adjust the expected number of best fit functions if needed
        
    def test_map_test_data(self):
        """
        Test if the test data is mapped correctly to the ideal functions.
        """
        best_fit_functions = self.processor.find_best_fit_functions()
        self.processor.map_test_data(best_fit_functions)
        session = self.db_handler.get_session()
        mapped_data = session.query(MappedTestData).all()

        # Debugging output to understand why no data is being mapped
        logger.debug("Mapped Data:")
        for item in mapped_data:
            logger.debug(f"x: {item.x}, y: {item.y}, ideal_function: {item.ideal_function}, deviation: {item.deviation}")

        self.assertGreater(len(mapped_data), 0)  # Ensure some data is mapped
        session.close()

if __name__ == "__main__":
    unittest.main()