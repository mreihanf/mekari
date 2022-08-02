--Truncate table to overwrite
TRUNCATE TABLE salary;

--Insert result from query to table
insert into salary
SELECT y AS YEAR ,m AS month,branch_id, SUM(salary)/SUM(timediff) as salary_per_hour
FROM (
SELECT DATE_PART('year', DATE) y,date_part('month', DATE) m,branch_id,employee_id,salary
,SUM(CASE WHEN checkin > checkout THEN ((EXTRACT(EPOCH FROM checkout) - EXTRACT(EPOCH FROM checkin))/3600)+24 ELSE (EXTRACT(EPOCH FROM checkout) - EXTRACT(EPOCH FROM checkin))/3600 end) timediff
FROM timesheets LEFT JOIN employees ON employe_id = employee_id WHERE checkin IS NOT NULL AND checkout IS NOT NULL 
GROUP BY 1,2,3,4,5
) x
GROUP by 1,2,3
ORDER BY 1,2,3,4