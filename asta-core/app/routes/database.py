# This file is now deprecated. Use app.db.session instead.
from app.db.session import get_db

# Alias the function to maintain backward compatibility
get_db_connection = get_db
