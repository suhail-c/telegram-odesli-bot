import aiosqlite

# Function to create the database and table asynchronously
async def create_database():
    async with aiosqlite.connect("mydatabase.db") as db:
        cursor = await db.cursor()
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS mytable (
                id TEXT,
                link TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id)
            )
        """)
        await db.commit()

# Function to store values in the database asynchronously
async def store_values(id, link):
    async with aiosqlite.connect("mydatabase.db") as db:
        cursor = await db.cursor()
        await cursor.execute("INSERT INTO mytable (id, link) VALUES (?, ?)", (id, link))
        await db.commit()

# Function to retrieve values by ID asynchronously
async def retrieve_values_by_id(id):
    async with aiosqlite.connect("mydatabase.db") as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT link FROM mytable WHERE id=?", (id,))
        result = await cursor.fetchone()
    return result

# Function to delete entries older than a specified number of hours from a table asynchronously
async def delete_old_entries_by_hours(table_name, hours_threshold):
    async with aiosqlite.connect("mydatabase.db") as db:
        cursor = await db.cursor()
        await cursor.execute(f"DELETE FROM {table_name} WHERE timestamp < datetime('now', '-{hours_threshold} hours')")
        await db.commit()
