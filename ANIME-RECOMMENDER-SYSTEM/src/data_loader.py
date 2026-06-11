import pandas as pd

class AnimeDataLoader:
    def __init__(self, origional_csv: str, processed_csv: str):
        self.origional_csv = origional_csv
        self.processed_csv = processed_csv
    
    def load_and_process(self):
        # Load the original CSV file
        df = pd.read_csv(self.origional_csv, encoding='utf-8', on_bad_lines='skip')
        
        # Process the data (example: drop rows with missing values)
        processed_df = df.dropna()
        
        #required columns
        required_columns = {'Name' , 'Genres','sypnopsis'}
        
        #missing columns
        missing_columns = [col for col in required_columns if col not in processed_df.columns]
        
        #if missing handle error
        if missing_columns:
            raise ValueError(f"Missing required columns in the CSV file")
        
        #combine 'name', 'Genres', 'sypnopsis' into a single column 'combined_info'
        df['combined_info'] = ( "Title: " + df["Name"] + " Overview: " +df["sypnopsis"] + "Genres : " + df["Genres"])
        
        # Save the combined_info data column to a new CSV file
        df[['combined_info']].to_csv(self.processed_csv , index=False,encoding='utf-8')
        
        return self.processed_csv