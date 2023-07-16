create table task (
	task_id varchar PRIMARY KEY,
    task_name varchar,
    date_created timestamp,
    date_updated timestamp,
    due_date timestamp,
    url varchar,
    status_name varchar,
    date_closed timestamp
);

create table members (
	member_id numeric primary key,
	member_name varchar
);


create table hours (
	time_id numeric primary key,
	task_id varchar,
	user_id numeric,
	start_date timestamp,
	end_date timestamp,
	duration numeric
	
);

create table tags (
	tag_name varchar
);

create table task_merbers_relantionship (
    task_id varchar,
    member_id numeric
);

create table task_tags_relantionship (
    task_id varchar,
    tag_name varchar
);

create table hour_tags_relationship (
	time_id numeric,
	tag_name varchar
);
