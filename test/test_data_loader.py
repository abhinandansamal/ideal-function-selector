import unittest
import pandas as pd
import sys
import os
import logging
from src.ideal_function_selector.database.database import DatabaseHandler, TrainingData, IdealFunctions, TestData
from src.ideal_function_selector.components.data_loader import DataLoader
from sqlalchemy.orm import sessionmaker


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the src directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
# src_path = os.path.join(current_dir, '..', 'src')
# sys.path.append(src_path)


class TestDataLoader(unittest.TestCase):
    """
    Unit tests for the DataLoader class.
    """
    def setUp(self):
        """
        Set up the in-memory database and data loader for testing.
        """
        self.db_handler = DatabaseHandler(':memory:')
        self.data_loader = DataLoader(self.db_handler)
        self.Session = sessionmaker(bind=self.db_handler.engine)

        # Ensure the test_data directory exists
        self.test_data_dir = current_dir  # Store temp files in current test directory

        # Paths to temporary CSV files
        self.temp_train_csv = os.path.join(self.test_data_dir, 'temp_train.csv')
        self.temp_ideal_csv = os.path.join(self.test_data_dir, 'temp_ideal.csv')
        self.temp_test_csv = os.path.join(self.test_data_dir, 'temp_test.csv')
        
    def test_load_csv_to_db(self):
        """
        Test if data is loaded correctly into the database.
        """
        # Sample data to simulate the content of CSV files
        training_data = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y': [1.1, 2.2, 3.3]
        })
        ideal_data = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y1': [1.1, 2.1, 3.1],
            'y2': [1.2, 2.2, 3.2]
        })
        test_data = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y': [1.0, 2.1, 3.4]
        })

        # Saving sample data to temporary CSV files
        training_data.to_csv(self.temp_train_csv, index=False)
        ideal_data.to_csv(self.temp_ideal_csv, index=False)
        test_data.to_csv(self.temp_test_csv, index=False)

        # Load data into the database
        self.data_loader.load_csv_to_db(self.temp_train_csv, TrainingData)
        self.data_loader.load_csv_to_db(self.temp_ideal_csv, IdealFunctions)
        self.data_loader.load_csv_to_db(self.temp_test_csv, TestData)

        # Check if data was loaded correctly
        session = self.Session()

        loaded_training_data = session.query(TrainingData).all()
        self.assertEqual(len(loaded_training_data), 3)
        self.assertEqual(loaded_training_data[0].x, 1.0)
        self.assertEqual(loaded_training_data[0].y, 1.1)

        loaded_ideal_data = session.query(IdealFunctions).all()
        self.assertEqual(len(loaded_ideal_data), 3)
        self.assertEqual(loaded_ideal_data[0].x, 1.0)
        self.assertEqual(loaded_ideal_data[0].y_values, '1.1,1.2')

        loaded_test_data = session.query(TestData).all()
        self.assertEqual(len(loaded_test_data), 3)
        self.assertEqual(loaded_test_data[0].x, 1.0)
        self.assertEqual(loaded_test_data[0].y, 1.0)

        session.close()

if __name__ == "__main__":
    unittest.main()