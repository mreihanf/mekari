CREATE TABLE IF NOT EXISTS employees (
  employe_id INTEGER,
  branch_id integer,
  salary integer,
  join_date DATE,
  resign_date DATE
);
CREATE TABLE if not exists timesheets (
  timesheet_id INTEGER,
  employee_id INTEGER,
  date DATE,
  checkin time,
  checkout TIME
);
CREATE TABLE if not exists salary (
	"insert_date" DATE,
	"year" INTEGER ,
	"month" INTEGER ,
	"branch_id" INTEGER ,
	"salary_per_hour" NUMERIC 
);
COPY employees FROM 'D:\employees.csv' DELIMITER ',' csv header;
COPY timesheets FROM 'D:\timesheets.csv' DELIMITER ',' csv header;