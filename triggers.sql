DELIMITER $$;

CREATE TRIGGER after_course_of_the_day_insert
AFTER INSERT
ON courses_of_the_day FOR EACH ROW
begin 
	update courses
	set platform_sale = platform_sale + 10
	where courses.id=NEW.course_id;
end;


CREATE TRIGGER before_user_insert
BEFORE INSERT
ON users FOR EACH ROW
begin 
	if (SELECT EXISTS (SELECT * FROM users where email=NEW.email) = 1)
    then
	SIGNAL SQLSTATE 'HY000'
	SET MESSAGE_TEXT = 'Email is already used', MYSQL_ERRNO = 1000;
    end if;
end;
