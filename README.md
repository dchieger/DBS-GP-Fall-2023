# DBS-GP-Fall-2023

Run a local mysql container
docker run -d --name mysql-container-DBS-GP -e MYSQL_ROOT_PASSWORD=root_password -e MYSQL_DATABASE=mysql_db -e MYSQL_USER=admin -e MYSQL_PASSWORD=password -p 3306:3306 mysql
