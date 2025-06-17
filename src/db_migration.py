from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# === CONFIGURATION ===

# Path to your local SQLite file
sqlite_file_path = r"E:\licenta_git_last\db_dani.sqlite3"

# MySQL database connection info
mysql_user = "root"
mysql_password = "root"
mysql_host = "localhost"
mysql_db = "movie_db"

# === CONNECTION STRINGS ===

sqlite_url = f"sqlite:///{sqlite_file_path}"
mysql_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"

# === CREATE ENGINES ===

sqlite_engine = create_engine(sqlite_url)
mysql_engine = create_engine(mysql_url)

# === REFLECT TABLES FROM SQLITE ===

metadata = MetaData()
metadata.reflect(bind=sqlite_engine, only=["home_genre", "home_movie", "home_movie_genre"])

# === CREATE TABLES IN MYSQL ===

metadata.create_all(mysql_engine)

# === COPY DATA FROM SQLITE TO MYSQL ===

SQLiteSession = sessionmaker(bind=sqlite_engine)
MySQLSession = sessionmaker(bind=mysql_engine)

sqlite_session = SQLiteSession()
mysql_session = MySQLSession()
count = 0
for table in metadata.sorted_tables:
    result = sqlite_session.execute(table.select())
    rows = result.mappings().all()  # This returns a list of dict-like mappings
    if rows:
        mysql_session.execute(table.insert(), rows)

mysql_session.commit()
print("✅ Migration complete!")
