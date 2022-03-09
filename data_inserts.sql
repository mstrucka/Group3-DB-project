use mydb;
/* students here */
insert into users (email, password_hash, is_student, school, education, firstName, lastName, dob)
values
   ('olee@olee.com', '666999', 1,  'DTU', 'BA', 'Ole', 'Olesen', '1997-08-08'),
   ('sam@ko.com', '123456', 1, 'KEA', 'Software Development', 'Sam', 'Horacek', '2007-01-02'),
   ('marek@strucka.com', '12534', 1, 'KEA', 'Software Development', 'Marek', 'Strucka', '1999-04-01'),
   ('hartmann@gmail.com', '444', 1, 'KEA', 'Web Development', 'Peter', 'Hartmann', '1993-07-22'),
   ('person@gmail.com', '333', 1, 'KU', 'Datalogi', 'Person', 'McPersonface', '2000-01-01');

/* users here */
insert into users (email, password_hash, is_student, firstName, lastName, dob)
values
       ('darth@vader.com', '555', 0, 'Darth', 'Vader', '2011-01-01'),
       ('indi@gmail.com', '1345234', 0, 'Indiana', 'Jones', '1998-01-01'),
       ('sam@novak.com', '123', 0,'Uncle', 'Sam', '2003-01-01');

insert into courses (title, description, level, price, platform_sale, category, lecturer)
values
       ('Introduction to the Dark Side',
        'Learn the basics of the Dark Side, and how to become a true sith lord',
        1, 50.00, 0, 'evil', 6),
       ('Advanced Whipping',
        'Take your whipping to the next level in this advanced whipping course
        featuring the one and only Indiana Jones. Using advanced whipping techniques and
        tricks you will be guided towards whipping mastery.', 3, 111, 0, 'whipping', 6),
       ('Guns and how to use them', 'In this course you will not only learn to wield powerful weapons,
        but also learn the history of guns. We will also touch upon different military skill and strategic war
        concepts, as well as practical tips on warfare in the front line. You will also learn how to make
        molotov cocktails of course. YMRA EHT NIOJ', 2, 66.6, 1, 'war', 8),
       ('KISS and other principles', 'Keep It Simple Stupid, no refunds!', 2, 123, 0, 'useless', 7),
       ('Surviving as a developer', 'Learn how to preserve and ration bits. Dont take too large bytes when consuming', 3, 47.71, 0, 'survival', 7),
       ('How to SQL', 'Learn the basics of the structured query language.', 3, 99.99, 0, 'sql', 6);

insert into payments(id, date, is_refund, total)
values 
	(1,'1998-01-01', 0, 100.00),
	(2,'1998-01-02', 0, 150.00),
    (3,'1998-01-03', 1, 200.00);
insert into enrollments(student_id, course_id, payment_id)
values
		(1,1,1),
        (2,2,2),
        (1,2,3);