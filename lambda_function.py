from slots import get_slots_info
VERSION="1.0.0"

def lambda_handler(event, context):
    print(f"Starting slots info lambda version {VERSION}")
    get_slots_info()
    print(f"Goodbye!")