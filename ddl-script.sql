create table if not exists lecturers
(
    id        int auto_increment
        primary key,
    resume    blob        null,
    firstName varchar(45) not null,
    lastName  varchar(45) not null
);

create table if not exists courses
(
    id          int auto_increment
        primary key,
    title       varchar(45)    not null,
    description varchar(500)   null,
    level       varchar(45)    not null,
    price       decimal(10, 2) not null,
    sale        tinyint(1)     null,
    category    varchar(45)    not null,
    lecturer    int            null,
    constraint lecturer_id
        foreign key (lecturer) references lecturers (id)
            on update cascade on delete cascade
);

create index lecturer_id_idx
    on courses (lecturer);

create index title_index
    on courses (title);

create table if not exists lectures
(
    id          int auto_increment
        primary key,
    title       varchar(45) not null,
    description varchar(45) null,
    price       decimal     not null
);

create table if not exists courselectures
(
    course_id  int not null,
    lecture_id int not null,
    primary key (course_id, lecture_id),
    constraint course_id
        foreign key (course_id) references courses (id)
            on update cascade on delete cascade,
    constraint course_lectures_lecture_id
        foreign key (lecture_id) references lectures (id)
            on update cascade on delete cascade
);

create index lecture_id_idx
    on courselectures (lecture_id);

create table if not exists resources
(
    id   int auto_increment
        primary key,
    type varchar(45) not null,
    name varchar(45) null
);

create table if not exists lectureresources
(
    resource_id int not null,
    lecture_id  int not null,
    primary key (resource_id, lecture_id),
    constraint lecture_id
        foreign key (lecture_id) references lectures (id)
            on update cascade on delete cascade,
    constraint resource_id
        foreign key (resource_id) references resources (id)
            on update cascade on delete cascade
);

create index lecture_id_idx
    on lectureresources (lecture_id);

create table if not exists students
(
    id        int auto_increment
        primary key,
    school    varchar(45) null,
    education varchar(45) null,
    firstName varchar(45) not null,
    lastName  varchar(45) not null,
    dob       date        not null
);

create table if not exists enrollments
(
    student_id      int                                not null,
    course_id       int                                not null,
    enrollment_date datetime default CURRENT_TIMESTAMP not null,
    primary key (student_id, course_id),
    constraint enrollment_course
        foreign key (course_id) references courses (id)
            on update cascade on delete cascade,
    constraint enrollment_student
        foreign key (student_id) references students (id)
            on update cascade on delete cascade
);

create index enrollment_course_idx
    on enrollments (course_id);

