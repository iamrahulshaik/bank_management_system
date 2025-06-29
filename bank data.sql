set autocommit = 0;
SET SQL_SAFE_UPDATES = 0;
alter user 'root'@'localhost' identified with mysql_native_password by 'mysql';
flush privileges;
create database bank;
use bank;
create table register (name varchar(50) , ac_tpye varchar(50),contact varchar(50) primary key ,location varchar(50),pin int);
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ac_number VARCHAR(20),
    transaction_type VARCHAR(10),  -- 'credit' or 'debit'
    amount INT,
    balance_after INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
create table employee (id int primary key ,admin_id varchar(50) unique,password varchar(50));



select * from employee;
select * from transactions;
select  * from register;
desc register;
desc transactions;
desc employee;