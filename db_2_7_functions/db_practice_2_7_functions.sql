-- Задание 1:
-- Создать функцию, которая сетит shipping_total = 0 в таблице order, если город юзера равен x. Использовать IF clause.

-- не совсем понял что именно нужно сделать, поэтому сделал две функции (подозревая вторая будет ближе к поставленной задаче)

-- 1.1  создадим функцию, которая по номеру заказа и номеру города устанавливает доставку заказа раной нулю

begin transaction;

create or replace function free_shipping(specify_order_id int, specify_free_delivery_city int)
returns varchar
language plpgsql
as
$$
declare
	message_update varchar;
	x integer;
begin
	perform u.city from users u
	join carts c on u.user_id = c.users_user_id
	join "Order" o on o.carts_cart_id = c.cart_id
	where o.order_id = specify_order_id and u.city = 'city ' || specify_free_delivery_city;

if found then
	update "Order" set shipping_total = 0
	where order_id = specify_order_id;
	x := specify_free_delivery_city;
	message_update := 'Update successfully';
	return message_update;
else
	x := specify_free_delivery_city;
	message_update := 'Not update';
	return message_update;
end if;

end;
$$;

-- Вызываем функцию  
-- SELECT free_shipping(2, 2)

-- для проверки, что внесены изменения, необходимо указать номер города
-- SELECT u.user_id, u.city, o.order_id, o.shipping_total FROM users u JOIN carts c ON u.user_id = c.users_user_id
-- JOIN "Order" o ON o.carts_cart_id = cart_id WHERE u.city = 'city x';

-- удаляем функцию
-- drop function free_shipping(specify_order_id int, specify_free_delivery_city int);

-- на выбор
-- rollback; commit;



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


-- посмотреть всех пользователей, номера заказов и стоимость доставки заказов (для проверки, что внесены изменения), необходимо указать номер города
-- SELECT u.user_id, o.order_id, o.shipping_total FROM users u JOIN carts c ON u.user_id = c.users_user_id
-- JOIN "Order" o ON o.carts_cart_id = cart_id WHERE u.city = 'city x';

-- вызываем функцию
-- SELECT order_id_with_free_shipping(2)

-- удаляем функцию
-- drop function free_shipping(x int);

-- на выбор
-- rollback; commit;




-- Задание 2
-- Написать 2 любые хранимые процедуры с использованием условий, циклов и транзакций.


-- 1я процедура - процедура make_discounts принимает значение которое готовы потратить на акцию для работников,
-- которые сделали заказы (работники выбираются первые которые попались в запросе), снижая стоимость их заказов на 20 процентов.
-- И если количество заказов в состоянии прогресса больше чем количество оплаченных заказов, то проводится акция для 10 человек,
-- а если меньше то для пяти.
-- Но, если затраты на акцию привосходят заданную сумму, то акция не проводится 
  

create or replace procedure make_discounts(amount_for_all_discounts int)
language plpgsql
as $$
declare
	orders_in_process int;
	orders_paid int;
	winners record;
	count_winner int := 0;
	number_winners int := 0;
	total_discount int := amount_for_all_discounts;
begin
    select count(order_status_order_status_id) into orders_in_process FROM "Order" where order_status_order_status_id = 2;
    select count(order_status_order_status_id) into orders_paid FROM "Order" where order_status_order_status_id = 4;
	
    if orders_in_process > orders_paid then	    
        number_winners := 10;
        for winners in 
	    select user_id, u.first_name ||' '|| u.last_name ||' '|| u.middle_name as customer, sum(o.total)*0.2 as discount
	    from users u join carts c on c.users_user_id = u.user_id
	    join "Order" o on o.carts_cart_id = c.cart_id 
	    where u.is_staff = 1 GROUP BY u.user_id LIMIT number_winners
	    loop
		total_discount = total_discount - winners.discount; 
		update "Order" set total = 0.8*total
		where order_id = winners.user_id;
	
		count_winner := count_winner + 1;
		raise notice 'Winner % is % got % discount on orders', count_winner, winners.customer, winners.discount;
				
	    end loop;
    else 
	number_winners := 5;
	for winners in 
	    select user_id, u.first_name ||' '|| u.last_name ||' '|| u.middle_name as customer, sum(o.total)*0.2 as discount
	    from users u join carts c on c.users_user_id = u.user_id
	    join "Order" o on o.carts_cart_id = c.cart_id 
	    where u.is_staff = 1 GROUP BY u.user_id LIMIT number_winners
	    loop
		total_discount = total_discount - winners.discount; 
		update "Order" set total = 0.8*total
		where order_id = winners.user_id;
		
		count_winner := count_winner + 1;
		raise notice 'Winner % is % got % discount on orders', count_winner, winners.customer, winners.discount;
	    end loop;				
    commit;
    end if;
	
			
    if total_discount < 0 then
	raise notice 'no promotion';
	rollback;		
    end if;		
end;
$$;



-- сделаем через транзакцию, чтобы потом можно было вернуть к первоначальному состоянию
begin transaction;

-- можем взглянуть на сумму заказов первой десятки работников, чтобы потом сверится
--select user_id, sum(o.total)
--from users u join carts c on c.users_user_id = u.user_id
--join "Order" o on o.carts_cart_id = c.cart_id 
--where u.is_staff = 1 GROUP BY u.user_id LIMIT 10;


-- вызовим процедуру с указанием суммы доступной для акции 
call make_discounts(1000);


-- можем убарть внесенные изменения
-- rollback;

-- удалим процедуру
-- drop procedure make_discounts();



















