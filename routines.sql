create
    definer = root@localhost function CustomerAge(dateOfBirth date) returns int deterministic
begin
    declare customerAge int;
    set customerAge = timestampdiff(year, dateOfBirth, date(now()));
    return (customerAge);
end;

create
    definer = root@localhost procedure course_lottery()
begin
    declare studentId int;
    declare courseId int;
    declare enrollmentCount int;
    -- select random student
    select id
    into studentId
    from students
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
    where student_id = studentId and course_id = courseId;

    if
        enrollmentCount = 1 then
        call course_lottery();
    end if;

    -- enroll student in the course
    insert into enrollments (student_id, course_id)
    values (studentId, courseId);

    select * from enrollments
    where student_id = studentId and course_id = courseId;
end;

create
    definer = root@localhost function getAverageCoursePricesByLecturer(lecturerId int) returns decimal(10, 2)
    deterministic
begin
    declare average decimal(10,2);
    select avg(price)
    into average
    from courses
    where lecturer = lecturerId;
    return average;
end;

create
    definer = root@localhost procedure getAverageCoursePricesByLecturers()
begin
    select *, getAverageCoursePricesByLecturer(id) as avg_course_price
    from lecturers
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
    definer = root@localhost procedure get_customer_age(IN studentId int)
sp: begin
    -- check if student exists
    declare studentCount int;
    select count(*)
    into studentCount
    from students
    where id = studentId;

    -- if student doesn't exists
    -- terminate stored procedure
    if studentCount = 0 then
        select'Student does not exist';
        leave sp;
    end if;

    select CustomerAge(s.dob) as age
    from students s
    where s.id = studentId;
end;