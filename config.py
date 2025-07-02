import urllib

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=eventserver12345.database.windows.net;"
    "DATABASE=event_db;"
    "UID=sqladmin;"
    "PWD=Admin123;"
)

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "yoursecretkey"
