Задание 5
Написать 2 любые хранимые процедуры. В них использовать транзакции для insert, update, delete.

-- 1я, добавлянм клиента, если его имя уже есть в базе, пишем об этом сообщение

create or replace procedure update_name_customer(user_id int,
   new_name varchar(255))
language plpgsql
as $$
declare
    new_name_customer varchar;
    count_name int := 0;
begin

	update customer
	set name = new_name
	where customer_id = user_id
	returning name
	into new_name_customer;
	
	select count(customer_id) into count_name from customer
	where name = new_name_customer;
	
	if count_name > 1 then
		raise notice 'The customer with the same name already exists';		
		rollback;
	end if;
end; $$;

call update_name_customer(2, 'customer name 1');

select * from customer;

drop procedure update_name_customer(user_id int, new_name varchar(255))



-- 2я на вставку, условие вставки будет тоже что и раньше т.е. такого имени не должно быть 

create or replace procedure insert_name_customer(new_name varchar(255))
language plpgsql
as $$
declare
    new_name_customer varchar;
    count_name int := 0;
begin

	insert into customer(name) values(new_name)
	returning name
	into new_name_customer;
	
	select count(customer_id) into count_name from customer
	where name = new_name_customer;
	
	if count_name > 1 then
		raise notice 'The customer with the same name already exists';		
		rollback;
	end if;
end; $$;

call insert_name_customer('customer name 81');

select * from customer;

drop procedure insert_name_customer(new_name varchar(255))




