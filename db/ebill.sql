CREATE TABLE etl_control
(
job_id_seq   INTEGER PRIMARY KEY AUTOINCREMENT,
etl_date     INTEGER NOT NULL

);

CREATE TABLE company
(
	co_id                INTEGER NOT NULL,
	co_ruc               INTEGER NOT NULL,
	co_serie             CHAR(18) NOT NULL,
	co_name              VARCHAR(100) NOT NULL,
	co_address           VARCHAR(100) NULL,
	co_cont_id           INTEGER NULL,
	etl_job_id           INTEGER NOT NULL,
	etl_date             INTEGER NOT NULL
);


CREATE TABLE cdr
(
	bill_id              INTEGER PRIMARY KEY AUTOINCREMENT,
	co_id                INTEGER NOT NULL,
	bill_no              INTEGER NOT NULL,
	bill_type            CHAR(10) NOT NULL,
	bill_file            CHAR(25) NOT NULL,
	sref_id              CHAR(18) NULL,
	sret_code            CHAR(18) NULL,
	sret_msg             CHAR(18) NULL,
	etl_jobid            INTEGER NOT NULL,
	etl_date             INTEGER NOT NULL

);

CREATE TABLE ebill
(
	bill_id              INTEGER PRIMARY KEY AUTOINCREMENT,
	co_id                INTEGER NULL,
	bill_no              INTEGER NULL,
	bill_type            CHAR(10) NULL,
	bill_file            CHAR(25) NULL,
	ret_code             INTEGER NULL,
	ret_msg              VARCHAR(255) NULL,
	etl_jobid            INTEGER NULL,
	etl_date             CHAR(25) NULL
);
