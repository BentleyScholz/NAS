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
    print(f'Connected to {database_name}')

    ##################################################
    # erase and reacreate test table
    ##################################################

    ### Read in data so we know what fields we need

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

    # Helper function for converting pandas dtypes to sql dtypes
    # def convert_dtypes(dtype:str):
    #     if 

    schema = dict(
        zip(
            df.dtypes.index,
            df.dtypes.values
        )
    )

    print(schema)

    query = f'''
    CREATE OR REPLACE {database_table};
    '''

    # print(f'Executing query {query}')
    # cur.execute(query)

    ##################################################
    # load data and write to db
    ##################################################

    # Helper function for formating queries

