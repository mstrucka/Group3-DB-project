CREATE VIEW most_challenging_courses AS
SELECT *  
FROM Courses
ORDER BY Courses.level DESC LIMIT 3;  

CREATE VIEW students_with_most_enrollments AS
select Users.firstName, Users.lastName, count(student_id) as courses from Enrollments
left join Users ON Enrollments.student_id = Users.id
group by Users.firstName, Users.lastName
order by courses desc;