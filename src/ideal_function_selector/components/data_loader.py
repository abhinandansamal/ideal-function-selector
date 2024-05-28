import pandas as pd
from src.ideal_function_selector.database.database import TrainingData, IdealFunctions, TestData

class DataLoader:
    """
    Handles loading CSV data into the database.
    """
    def __init__(self, db_handler):
        self.db_handler = db_handler
        
    def load_csv_to_db(self, csv_file, table_class):
        """
        Loads data from a CSV file into a specified database table.

        Args:
            csv_file (str): Path to the CSV file.
            table_class (Base): SQLAlchemy ORM class for the table.
        """
        session = self.db_handler.get_session()
        data = pd.read_csv(csv_file)
        
        if table_class == IdealFunctions:
            for _, row in data.iterrows():
                y_values = ','.join(map(str, row.iloc[1:].values))
                session.add(table_class(x=row.iloc[0], y_values=y_values))
        elif table_class == TrainingData:
            for _, row in data.iterrows():
                for col in row.index[1:]:
                    session.add(table_class(x=row['x'], y=row[col]))
        else:
            for _, row in data.iterrows():
                session.add(table_class(x=row.iloc[0], y=row.iloc[1]))
        
        session.commit()
        session.close()
