import pandas as pd
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from src.ideal_function_selector.database.database import DatabaseHandler, TrainingData, TestData, MappedTestData

class DataVisualizer:
    """
    Visualizes data using Bokeh.
    """
    def __init__(self, db_handler):
        self.db_handler = db_handler
        
    def visualize_data(self):
        """
        Visualizes the training data, test data, and mapped test data.
        """
        session = self.db_handler.get_session()
        training_data = pd.read_sql(session.query(TrainingData).statement, self.db_handler.engine)
        test_data = pd.read_sql(session.query(TestData).statement, self.db_handler.engine)
        mapped_data = pd.read_sql(session.query(MappedTestData).statement, self.db_handler.engine)
        
        p1 = figure(title="Training Data", x_axis_label='x', y_axis_label='y')
        p1.scatter(training_data['x'], training_data['y'], size=5, color="blue", alpha=0.5)
        
        p2 = figure(title="Test Data", x_axis_label='x', y_axis_label='y')
        p2.scatter(test_data['x'], test_data['y'], size=5, color="green", alpha=0.5)
        
        p3 = figure(title="Mapped Test Data", x_axis_label='x', y_axis_label='y')
        p3.scatter(mapped_data['x'], mapped_data['y'], size=5, color="red", alpha=0.5)
        
        grid = gridplot([[p1, p2, p3]])
        show(grid)