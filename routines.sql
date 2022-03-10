create
    definer = root@localhost function UserAge(dateOfBirth date) returns int deterministic
begin
    declare userAge int;
    set userAge = timestampdiff(year, dateOfBirth, date(now()));
    return (userAge);
end;

create
    definer = root@localhost procedure course_lottery()
begin
    declare userId int;
    declare courseId int;
    declare enrollmentCount int;
    -- select random student
    select id
    into userId
    from users
    where is_student = 1
    order by rand()
    limit 1;

    -- select random course
    select id
    into courseId
    from courses
    order by rand()
    limit 1;

    -- if student is already enrolled, leave
    select count(*)
    into enrollmentCount
    from enrollments
    where student_id = userId and course_id = courseId;

    if
        enrollmentCount = 1 then
        call course_lottery();
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
    select *, getAverageCoursePricesByLecturer(id) as avg_course_price
    from users
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
    definer = root@localhost procedure get_user_age(IN userId int)
sp: begin
    -- check if student exists
    declare userCount int;
    select count(*)
    into userCount
    from users
    where id = userId;

    -- if student doesn't exists
    -- terminate stored procedure
    if userCount = 0 then
        select'Student does not exist';
        leave sp;
    end if;

    select UserAge(u.dob) as age
    from users u
    where u.id = userId;
end;