use mydb;
/* TRIGGERS */
CREATE TRIGGER after_course_of_the_day_insert
AFTER INSERT
ON course_of_the_day FOR EACH ROW
begin
	update course
	set platform_sale = platform_sale + 10
	where course.id=NEW.course_id;
end;

/* VIEWS */
use mydb;
CREATE VIEW most_challenging_courses AS
SELECT *
FROM Course
ORDER BY Course.level DESC LIMIT 3;

CREATE VIEW students_with_most_enrollments AS
select User.firstName, User.lastName, count(student_id) as courses from Enrollment
left join User ON Enrollment.student_id = User.id
group by User.firstName, User.lastName
order by courses desc;

/* EVENTS */
/* for testing purposes */
/* ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 1 MINUTE */
CREATE EVENT IF NOT EXISTS removePlatformSaleEvent
ON SCHEDULE EVERY 1 DAY STARTS (CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 1 HOUR)
DO begin
    declare courseId int;
    select course_id into courseId from course_of_the_day order by date DESC limit 1;
	update course
	join course_of_the_day on course_of_the_day.course_id=course.id
	set platform_sale = 0
	where course.id=courseId;
end;

CREATE EVENT IF NOT EXISTS selectRandomCourse
ON SCHEDULE EVERY 1 DAY STARTS (CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 1 HOUR)
DO begin
	declare courseId int;
    select id into courseId from course order by rand() limit 1;

	insert into course_of_the_day (course_id, date)
	values(courseId, CURRENT_DATE);
end;

/* ROUTINES */
create
    definer = root@localhost function calculateUserAge(dateOfBirth date) returns int deterministic
begin
    declare userAge int;
    set userAge = timestampdiff(year, dateOfBirth, date(now()));
    return (userAge);
end;

create
    definer = root@localhost procedure courseLottery()
begin
    declare userId int;
    declare courseId int;
    declare enrollmentCount int;
    -- select random student
    select getRandomUserId(true)
    into userId;

    -- select random course
    select getRandomCourseId()
    into courseId;

    -- if student is already enrolled, leave and call again
    select count(*)
    into enrollmentCount
    from enrollment
    where student_id = userId and course_id = courseId;

    if enrollmentCount = 1 then
        call courseLottery();
    end if;

    -- enroll student in the course
    insert into enrollment (student_id, course_id)
    values (userId, courseId);

    select * from enrollment
    where student_id = userId and course_id = courseId;
end;

create
    definer = root@localhost function getAverageCoursePricesByLecturer(userId int) returns decimal(10, 2)
    deterministic
begin
    declare average decimal(10,2);
    declare is_student smallint;
    declare userCount int;

    select count(*)
    into userCount
    from user
    where id = userId;

    -- check if user exists
    if userCount = 0 then
        return 'User does not exist';
    end if;

    select u.is_student
    into is_student
    from user u
    where id = userId;

    -- check if user is lecturer
    if is_student = 1 then
        return 'User is not lecturer';
    end if;

    select avg(price)
    into average
    from course
    where lecturer = userId;
    return average;
end;

create
    definer = root@localhost procedure getAverageCoursePricesByLecturers()
begin
    select id, firstName, lastName, getAverageCoursePricesByLecturer(id) as avg_course_price
    from user
    where is_student = 0
    order by avg_course_price desc;
end;

create
    definer = root@localhost function getCoursePricesSum() returns decimal(10, 2) deterministic
begin
    declare priceSum decimal(10,2);
    select sum(price)
    into priceSum
    from course;

    return (priceSum);
end;

create
    definer = root@localhost function getRandomCourseId() returns int deterministic
begin
    declare courseId int;
    select id
    into courseId
    from course
    order by rand()
    limit 1;

    return courseId;
end;

create
    definer = root@localhost function getRandomUserId(isStudent tinyint(1)) returns int deterministic
begin
    declare userId int;
    select id
    into userId
    from user
    where is_student = isStudent
    order by rand()
    limit 1;

    return userId;
end;

create
    definer = root@localhost procedure getUserAge(IN userId int)
sp: begin
    -- check if student exists
    declare userCount int;
    select count(*)
    into userCount
    from user
    where id = userId;

    -- if user doesn't exists
    -- terminate stored procedure
    if userCount = 0 then
        select'User does not exist';
        leave sp;
    end if;

    select calculateUserAge(u.dob) as age
    from user u
    where u.id = userId;
end;
/* PRIVILEGES */
CREATE USER IF NOT EXISTS apiUser1 IDENTIFIED BY 'api123';
GRANT SELECT, UPDATE, DELETE, INSERT, EXECUTE ON *.* TO 'apiUser1' WITH GRANT OPTION;