use mydb;
delimiter $$;

CREATE EVENT IF NOT EXISTS removePlatformSaleEvent
ON SCHEDULE EVERY 1 DAY STARTS (CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 1 HOUR)
DO begin 
    declare courseId int;
    select course_id into courseId from coursesoftheday order by date DESC limit 1;
	update courses
	join coursesoftheday on coursesoftheday.course_id=courses.id
	set platform_sale = 0
	where courses.id=courseId;
end

CREATE EVENT IF NOT EXISTS selectRandomCourse
ON SCHEDULE EVERY 1 DAY STARTS (CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 1 HOUR)
DO begin
	declare courseId int;
    select id into courseId from courses order by rand() limit 1;
    
	insert into coursesoftheday (course_id, date)
	values(courseId, CURRENT_DATE);
end