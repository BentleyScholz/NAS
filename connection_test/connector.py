# Module Imports
import mariadb
import sys, os
import pandas as pd

# directory to look for data
# Note: should be invoked from the upload.bash script, so current directory should be
# top level of the project. Running this from anywhere else may not (and is not supposed to) work
data_dir = "./datagen/data"

if __name__ == "__main__":

    # Takes four system arguments in the following order:
    # 1) user: str
    # 2) password: str
    # 3) host: str, ip address
    # 4) port: int

    assert len(sys.argv) >= 5, "Too few arguments"

    print('Attempting to connect...')

    # Need to be connected to the VPN

    conn = mariadb.connect(
        user=sys.argv[1],
        password=sys.argv[2],
        host=sys.argv[3],
        port=int(sys.argv[4])
    )

    print(f'Connected: {conn.open}')

    cur = conn.cursor()

    database_name = 'test_db'
    database_table = 'test_tbl'

    ##################################################
    # Erase and recreate test db
    ##################################################

    query = f'''
    CREATE OR REPLACE DATABASE {database_name};
    '''

    print(f'Executing query {query}')
    cur.execute(query)

    conn.select_db(new_db=database_name)
    print(f'Connected to {conn.database}')

    ##################################################
    # erase and reacreate test table
    ##################################################

    ### Read in data so we know what fields we need
    # make sure char array size matches with the string length in datagen.py

    table_schema = '''
    (Date DATE, Int_Field INT(8) UNSIGNED, Norm_Field_1 FLOAT, Norm_Field_2 FLOAT, Norm_Field_3 FLOAT, Norm_Field_4 FLOAT, Char_Field_1 CHAR(30), Char_Field_2 CHAR(30), Char_Field_3 CHAR(30))
    '''

    query = f'''
    CREATE OR REPLACE TABLE {database_table} {table_schema};
    '''

    print(f'Executing query {query}')
    cur.execute(query)

    ##################################################
    # load data and write to db
    ##################################################

    # get filenames in data directory
    files_in_dir = os.listdir(data_dir)
    assert len(files_in_dir) == 1, 'Data directory should have exactly one file'
    data_file = files_in_dir[0]
    
    df = pd.read_csv(
        filepath_or_buffer=f'{data_dir}/{data_file}',
        sep='\t',
        header=0,
        quoting=3
    )

    table_fields = '''
    (Date, Int_Field, Norm_Field_1, Norm_Field_2, Norm_Field_3, Norm_Field_4, Char_Field_1. Char_Field_2, Char_Field_3)
    '''

    query = f'''
    INSERT INTO {database_table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

    values_tuple = [tuple(x) for x in df.values]

    cur.executemany(
        query,
        values_tuple[:1000]
    )
    
    ##################################################
    # query data to make sure the tables arent empty
    ##################################################

    print('Found the following data after inserting:')

    cur.execute(
        f'SELECT * FROM {database_table}'
    )
    limit = 10
    token = 0
    for x in cur:
        if token >= limit:
            break
        else:
            print(x)