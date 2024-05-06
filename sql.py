import psycopg2

def sql_connect():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="15995",
            host="localhost",
            database="users_db"
        )
        connection.commit()

        return True
    except (Exception, psycopg2.Error):
        return False
    
def sql_connection():
    connection = psycopg2.connect(
        user="postgres",
        password="15995",
        host="localhost",
        database="users_db"
    )
    connection.commit()

    return connection

def create_table():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """CREATE TABLE cars(
            id  SERIAL PRIMARY KEY,
            uid BIGINT NOT NULL,
            key BIGINT NOT NULL,
            brend TEXT NOT NULL,
            model TEXT NOT NULL,
            price BIGINT NOT NULL,
            rasm TEXT NOT NULL
        );
        """
        cursor.execute(create_table)
        conn.commit()
    else:
        print("Bazaga ulanishda xatolik yuz berdi")
                                
def add_information(id, key, brend, model, price, rasm):
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        
        insert_query = """ INSERT INTO cars (uid, key, brend, model, price, rasm) VALUES (%s, %s, %s, %s, %s, %s) """
        
        cursor.execute(insert_query, (id, key, brend, model, price, rasm))
        conn.commit()
    else:
        print("Bazaga ulanishda xatolik yuz berdi")
        
def user_info(id):
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE uid = %s", (id,))
        
        res = cursor.fetchall()
        conn.commit()
        if not res:
            return False
        else:
            return res
    else:
        print("Bazaga ulanishda xatolik yuz berdi")    
    
def delete(keys):
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        cursor.execute("delete from cars where key = %s", (keys,))
        conn.commit()