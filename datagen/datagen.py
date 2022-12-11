import numpy as np
from datetime import datetime, timedelta
import os, sys

if __name__ == '__main__':

    # Setting seeded random generator
    seed = 1234
    rng = np.random.default_rng(seed)

    # Size of arrays to generate
    gsize = 100

    # Dimension of mulivariate normal to generate
    dim = 4

    # Params for generating random strings
    ascii_lower = 32 # Lower bound on range of ascii values to use
    ascii_upper = 126 # Upper bound on range of ascii values to use
    str_len = 30 # Length of generated strings
    num_char_fields = 3 # Number of string columns to generate in the output file

    # Number of lines in the output file to write
    lines_to_write = 100000

    ################################################################################
    # List of integers
    int_field = [i for i in range(0, gsize + 1)]

    # Generate random dim-dimensional normal variable
    mean = rng.standard_normal(
        size = (dim)
    )
    psuedo_root = rng.standard_normal(
        size = (dim, dim)
    )
    cov = np.matmul(psuedo_root.transpose(), psuedo_root)

    normal_fields = rng.multivariate_normal(
        mean,
        cov,
        size = gsize
    )

    # Generate lists of text fields from random characters
    chars = [chr(x) for x in range(ascii_lower, ascii_upper + 1)]
    str_fields = np.array(
        [
            "".join(rng.choice(a=chars, size=str_len))
            for _ in range(gsize*num_char_fields)
        ]
    ).reshape(
        (num_char_fields, gsize)
    )
    
    # Generate datetime list ranging from Unix start to current date, delta = 1 day
    date_field = np.arange(
        datetime(1970, 1, 1),
        datetime.now().date(),
        timedelta(days=1)
    ).astype('datetime64[D]')

    ################################################################################
    # Store all the arrays in a dictionary, makes writing to file a bit easier
    data = {
        "Date": date_field,
        "Int_Field": int_field 
    }
    # Append normal variables
    for i in range(dim):
        data[f'Norm_Field_{i + 1}'] = normal_fields[:, i]
    # Append string variables
    for i in range(num_char_fields):
        data[f'Char_Field_{i + 1}'] = str_fields[i]

    ################################################################################

    # Change working directory to location of script
    ### NOTE: Sys.path could be anything afaik, but SHOULD be the absolute path of the script in the user's filesystem as long
    ### as this script is running as __main__. See https://docs.python.org/3/library/sys.html#sys.path
    old_path = os.getcwd()
    new_path = sys.path[0]
    os.chdir(new_path)

    # Create data subdir if needed
    if not os.path.exists('./data'):
        os.mkdir('./data')
    
    # Define the filename
    datecomp = str(datetime.now().date()).replace('-', '_')
    filename = f'./data/{datecomp}_JunkData.tsv'

    # Open the file and write data to it
    with open(filename, 'w') as f:
        # Convert the fields into a header line
        header = ('\t').join(list(data.keys()))
        f.write(header + '\n')
        
        # Write all the remaining data lines
        for _ in range(lines_to_write - 1):
            row = [str(rng.choice(a=arr)) for arr in data.values()]
            f.write(('\t').join(row) + '\n')
        # Write last line w/o newline
        row = [str(rng.choice(a=arr)) for arr in data.values()]
        f.write(('\t').join(row))

    # Revert back to original working directory
    os.chdir(old_path)
