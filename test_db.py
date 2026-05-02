import asyncio
import asyncpg

async def main():
    try:
        conn = await asyncpg.connect(
            user='myuser',
            password='mypassword',
            database='mydatabase',
            host='nlp_db'
        )
        print('OK:', await conn.fetchval('SELECT 1'))
        await conn.close()
    except Exception as e:
        print('ERROR:', type(e).__name__, e)

asyncio.run(main())