USE DATABASE ecommerce_lab;

show tasks;


create table IDS (Id int);

create or replace task InsertID
warehouse = COMPUTE_WH
schedule = '1 MINUTE'
as
insert into IDS select random();

//a taks é criada desativa campo state = suspended
show tasks;

alter task InsertID resume;

select * from IDS;

alter task InsertID suspend;


//drop task InsertID;

//Criar uma dag

create table IDS2 (Id int);

create or replace task InsertID2
warehouse = COMPUTE_WH
after InsertID
as
insert into IDS2 select random();

show tasks;

alter task InsertID2 resume;
alter task InsertID resume;


select * from IDS;
select * from IDS2;

select * from table(INFORMATION_SCHEMA.TASK_HISTORY())


drop task InsertID2;
