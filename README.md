This is a small project to test Maria DB 10 running on Synology DS920+. Kinda just some junk mashed together.

Main action happens in the upload.bash script. Python scripts are only meant to be invoked by upload.bash, so invoking them from somewhere else will almost certainly cause an error.

The 'datagen' folder contains a simple python script to generate some junk data. We want to establish a remote connection to the database and create tables given this data.

Requires the MariaDB C connector, 3.3 or greater