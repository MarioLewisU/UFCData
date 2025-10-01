import pandas as pd
from sqlalchemy import create_engine

def load_data_to_postgres():
    """Load processed CSV files into PostgreSQL database."""
    
    # Database connection
    engine = create_engine('postgresql://postgres:0000@localhost:5432/UFCData')
    
    # Tables and their CSV files
    tables_files = {
        'fighters': 'out/fighters.csv',
        'events': 'out/events.csv', 
        'fights': 'out/fights.csv',
        'fight_stats': 'out/fight_stats.csv'
    }
    
    print("Loading data into PostgreSQL...")
    
    for table, csv_file in tables_files.items():
        try:
            # Read CSV
            df = pd.read_csv(csv_file)
            print(f"Read {len(df)} rows from {csv_file}")
            
            # Load into PostgreSQL (append to avoid table drop issues)
            df.to_sql(table, engine, if_exists='append', index=False)
            print(f"Loaded {len(df)} rows into {table} table")
            
        except Exception as e:
            print(f"Error loading {table}: {e}")
    
    print("Data loading completed!")
    engine.dispose()

