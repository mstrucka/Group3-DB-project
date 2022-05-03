use mydb;
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
    from enrollments
    where student_id = userId and course_id = courseId;

    if enrollmentCount = 1 then
        call courseLottery();
    end if;

    -- enroll student in the course
    insert into enrollments (student_id, course_id)
    values (userId, courseId);

    select * from enrollments
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
    from users
    where id = userId;

    -- check if user exists
    if userCount = 0 then
        return 'User does not exist';
    end if;

    select u.is_student
    into is_student
    from users u
    where id = userId;

    -- check if user is lecturer
    if is_student = 1 then
        return 'User is not lecturer';
    end if;

    select avg(price)
    into average
    from courses
    where lecturer = userId;
    return average;
end;

create
    definer = root@localhost procedure getAverageCoursePricesByLecturers()
begin
    select id, firstName, lastName, getAverageCoursePricesByLecturer(id) as avg_course_price
    from users
    where is_student = 0
    order by avg_course_price desc;
end;

create
    definer = root@localhost function getCoursePricesSum() returns decimal(10, 2) deterministic
begin
    declare priceSum decimal(10,2);
    select sum(price)
    into priceSum
    from courses;

    return (priceSum);
end;

create
    definer = root@localhost function getRandomCourseId() returns int deterministic
begin
    declare courseId int;
    select id
    into courseId
    from courses
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
    from users
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
    from users
    where id = userId;

    -- if user doesn't exists
    -- terminate stored procedure
    if userCount = 0 then
        select'User does not exist';
        leave sp;
    end if;

    select calculateUserAge(u.dob) as age
    from users u
    where u.id = userId;
end; 