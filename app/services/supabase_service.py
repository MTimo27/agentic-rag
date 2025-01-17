from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY

# Initialize the Supabase client globally
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def insert_data(table: str, data: dict):
    """Insert data into the specified Supabase table."""
    try:
        result = supabase.table(table).insert(data).execute()
        print(f"Inserted data into {table}: {result}")
        return result
    except Exception as e:
        print(f"Error inserting data into Supabase: {e}")
        return None
