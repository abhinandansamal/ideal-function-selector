import logging
import pandas as pd
import numpy as np
import logging
from sqlalchemy.orm import sessionmaker
from src.ideal_function_selector.database.database import TrainingData, IdealFunctions, TestData, MappedTestData

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Processes data to find best fit functions and map test data.
    """
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def find_best_fit_functions(self, num_functions=4):
        """
        Finds the best fit functions for the training data.

        Args:
            num_functions (int): Number of best fit functions to find.

        Returns:
            list: List of best fit function IDs.
        """
        session = self.db_handler.get_session()
        training_data = pd.read_sql(session.query(TrainingData).statement, self.db_handler.engine)
        ideal_functions = pd.read_sql(session.query(IdealFunctions).statement, self.db_handler.engine)
        
        best_fit_functions = []
        for _, train_row in training_data.iterrows():
            x_val = train_row['x']
            best_fit = None
            min_error = float('inf')
            for _, ideal_row in ideal_functions.iterrows():
                y_values = list(map(float, ideal_row['y_values'].split(',')))
                if len(y_values) != 50:
                    continue
                error = sum((train_row['y'] - y_val)**2 for y_val in y_values)
                if error < min_error:
                    min_error = error
                    best_fit = ideal_row['id']
            best_fit_functions.append(best_fit)
        
        session.close()
        return best_fit_functions

    def map_test_data(self, best_fit_functions):
        """
        Maps test data to the closest ideal functions within the defined criteria.

        Args:
            best_fit_functions (list): List of best fit function IDs.
        """
        session = self.db_handler.get_session()
        test_data = pd.read_sql(session.query(TestData).statement, self.db_handler.engine)
        ideal_functions = pd.read_sql(session.query(IdealFunctions).statement, self.db_handler.engine)
        
        logger.debug(f"Best fit function IDs: {best_fit_functions}")
        logger.debug(f"Ideal functions:\n{ideal_functions.head()}")

        ideal_functions = ideal_functions[ideal_functions['id'].isin(best_fit_functions)]
        mapped_data = []

        for _, test_row in test_data.iterrows():
            x_val = test_row['x']
            best_fit = None
            min_deviation = float('inf')
            for _, ideal_row in ideal_functions.iterrows():
                y_values = list(map(float, ideal_row['y_values'].split(',')))
                if len(y_values) != 50:
                    continue
                for y_val in y_values:
                    deviation = abs(test_row['y'] - y_val)
                    if deviation < min_deviation:
                        min_deviation = deviation
                        best_fit = ideal_row['id']
            if min_deviation < np.sqrt(2):
                mapped_data.append((test_row['x'], test_row['y'], best_fit, min_deviation))
        
        for x, y, ideal_func, deviation in mapped_data:
            session.add(MappedTestData(x=x, y=y, ideal_function=ideal_func, deviation=deviation))
        session.commit()
        session.close()

        logger.debug(f"Mapped data: {mapped_data}")