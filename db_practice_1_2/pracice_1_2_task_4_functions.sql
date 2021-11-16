Задание 4
Создать 2 функции (одна из них должна возвращать таблицу, одна из них должна использовать циклы, одна из них должна использовать курсор).

-- 2й, создаем функцию, которая по заданному номеру города обновляет достаку до стоимости равной 0 
-- и выводит номера этих заказов

-- на всякий слуай сделаем через транзакцию
begin transaction;

create or replace function order_id_with_free_shipping(x int)
returns table(free_id int)
language plpgsql
as
$$
begin
	perform o.order_id from users u
	join carts c on u.user_id = c.users_user_id
	join "Order" o on o.carts_cart_id = c.cart_id
	where u.city = 'city ' || x;
if found then
	update "Order" set shipping_total = 0
	where order_id = x;
return query	
	select o.order_id from users u
	join carts c on u.user_id = c.users_user_id
	join "Order" o on o.carts_cart_id = c.cart_id
	where u.city = 'city ' || x;
end if;
end;
$$;



-- создадим функцию, которая по номеру customer_id будет возвращать данные таблицу с данными о заказчике, такие как имя, адресс и телефон
-- если такого номера нет, то будет выбрасывать ошибку 
begin transaction;

create or replace function customer_info(user_id int)
returns 
table(customer_name varchar, c_address varchar, c_phone int)
language plpgsql
as
$$
declare 
not_info varchar := 'no data';
no_phone int := 0;
begin
	perform customer_id from customer
	where customer_id = user_id;
if found then
	return query
		SELECT c.name, a.address,
		p.phone_number FROM customer c 
		JOIN customer_address ca ON c.customer_id = ca.customer_id
		JOIN address a ON ca.address_id = a.address_id
		JOIN customers_phone cp ON cp.customer_id = c.customer_id
		JOIN phone p ON p.phone_number = cp.phone_number
		WHERE c.customer_id = user_id;
else 
	raise exception 'Not customer with id = %', user_id;
end if;
end;
$$;


 SELECT * FROM customer_info(2)
 
commit;




-- сделаем тоже, но с использования курсора и для нескольких закзчиков по вводу id вывод будем делать в виде строки текста и вывод будет в виде текста

begin transaction;

create or replace function customer_info(user_id_start int, user_id_end int)
returns text
language plpgsql
as
$$
declare 

cur_customers_info cursor(user_id_start int, user_id_end int)
		FOR SELECT c.name as name, a.address as ad,
		p.phone_number as pn FROM customer c 
		JOIN customer_address ca ON c.customer_id = ca.customer_id
		JOIN address a ON ca.address_id = a.address_id
		JOIN customers_phone cp ON cp.customer_id = c.customer_id
		JOIN phone p ON p.phone_number = cp.phone_number
		WHERE c.customer_id between user_id_start and user_id_end;

rec_info record;
result text default '';

begin
	perform customer_id from customer
	where customer_id between user_id_start and user_id_end;
if found then
	open cur_customers_info(user_id_start, user_id_end);
	loop
		fetch cur_customers_info into rec_info;
		exit when not found;
		
		result := result || ',' || rec_info.name || ',' || rec_info.ad || ',' || rec_info.pn|| ';';
	end loop;
	close cur_customers_info;
else 
	raise exception 'Not customer with id = % or %', user_id_start, user_id_end;
end if;

return result;
end; $$

 SELECT customer_info(2, 10)
 
commit;


