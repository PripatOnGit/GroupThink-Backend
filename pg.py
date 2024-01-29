import psycopg2
import hashlib
from datetime import datetime


def connect_to_pg():
    conn_string = "host='localhost' dbname='polls_db' user='postgres' password='root'"
    conn = psycopg2.connect(conn_string)
    print("Connection Successful!")
    return conn


def execute_select_query(query, params=None):
    conn = connect_to_pg()
    cursor = conn.cursor()
    print(f"Executing {query} with Params {params or []}")
    cursor.execute(query, params)    
    results = cursor.fetchall()
    print(f"Affected {cursor.rowcount} rows")    
    conn.close()
    return results


def execute_update_query(query, params=None):
    conn = connect_to_pg()
    cursor = conn.cursor()
    print(f"Executing {query} with Params {params or []}")
    cursor.execute(query, params)    
    conn.commit()
    row_count = cursor.rowcount    
    conn.close()
    print(f"Affected {row_count} rows")    
    return row_count


def create_user(data):
    data["joinedAt"] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    data['password'] = hashlib.md5(data['password'].encode()).hexdigest()
    query = "INSERT INTO USERS (Name, Email, Username, Password, JoinedAt) VALUES (%s,%s,%s,%s,%s)"
    res = execute_update_query(query, (data['name'], data['email'], data['username'], data['password'], data['joinedAt']))        
    return res == 1
        
    
def search_user(field, value):
    query = f"SELECT * FROM USERS WHERE {field} = %s"
    user_found = execute_select_query(query, (value,))    
    return user_found


def read_all_users() -> list:
    pass


def read_all_polls() -> list:
    conn = connect_to_pg()
    cursor = conn.cursor()
    records = cursor.execute("")


if __name__ == "__main__":
    ls = search_user("username",'priu26')
    print(ls)