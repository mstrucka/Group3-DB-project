insert into students (school, education, firstName, lastName, dob)
values
   ('DTU', 'BA', 'Ole', 'Olesen', '1997-08-08'),
   ('KEA', 'Software Development', 'Sam', 'Horacek', '2007-01-02'),
   ('KEA', 'Software Development', 'Marek', 'Strucka', '1999-04-01'),
   ('KEA', 'Web Development', 'Peter', 'Hartmann', '1993-07-22'),
   ('KU', 'Datalogi', 'Person', 'McPersonface', '2000-01-01');

insert into lecturers (firstName, lastName)
values
       ('Darth', 'Vader'),
       ('Indiana', 'Jones'),
       ('Uncle', 'Sam');

insert into courses (title, description, level, price, sale, category, lecturer)
values
       ('Introduction to the Dark Side',
        'Learn the basics of the Dark Side, and how to become a true sith lord',
        'beginner', 50.00, 0, 'evil', 1),
       ('Advanced Whipping',
        'Take your whipping to the next level in this advanced whipping course
        featuring the one and only Indiana Jones. Using advanced whipping techniques and
        tricks you will be guided towards whipping mastery.', 'advanced', 111, 0, 'whipping', 2),
       ('Guns and how to use them', 'In this course you will not only learn to wield powerful weapons,
        but also learn the history of guns. We will also touch upon different military skill and strategic war
        concepts, as well as practical tips on warfare in the front line. You will also learn how to make
        molotov cocktails of course. YMRA EHT NIOJ', 'intermediate', 66.6, 1, 'war', 3),
       ('KISS and other principles', 'Keep It Simple Stupid, no refunds!', 'ignorant', 123, 0, 'useless', 1),
       ('Surviving as a developer', 'Learn how to preserve and ration bits. Dont take too large bytes when consuming', 'beginner', 47.71, 0, 'survival', 2),
       ('How to SQL', 'Learn the basics of the structured query language.', 'noob', 99.99, 0, 'sql', 3);
