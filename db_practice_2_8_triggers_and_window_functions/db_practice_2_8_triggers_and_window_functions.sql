-- 1. Сравнить цену каждого продукта n с средней ценой продуктов в категории
-- продукта n. Использовать window function. Таблица результата должна
-- содержать такие колонки: category_title, product_title, price, avg.

SELECT c.category_title, p.product_title, p.price, AVG(price) OVER (PARTITION BY c.category_title) FROM products p JOIN categories c ON p.category_id = c.category_id;

 

-- 2. Добавить 2 любых триггера и обработчика к ним, использовать транзакции.

-- 2.1 если новый заказ сделан сотрудником, то сделать скидку в 20 процентов
-- начнем транзакцию, чтобы потом можно было отменить изменения
BEGIN;


-- создадим функцию discount для триггер order_after_insert_employee_discount, который будет наложен на таблицу заказов
-- и если в таблицу заказов будет вносится новый заказ, а его заказчик будет из числа персонала (users.is_staff = 1)
-- то цена на заказ (total) будет обновлена со скидкой длоя персонала в 20 процентов 
CREATE OR REPLACE FUNCTION discount() 
	RETURNS TRIGGER 
	LANGUAGE PLPGSQL
	AS
$$
DECLARE 
	user_staff int;
BEGIN 
	SELECT u.is_staff INTO user_staff FROM "Order" o 
	JOIN carts c ON o.carts_cart_id = c.cart_id 
	JOIN users u ON c.users_user_id = u.user_id 
	WHERE o.order_id = NEW.order_id;
	
	IF user_staff = 1 then		
		UPDATE "Order" SET total = 0.8*total WHERE order_id = (SELECT MAX(order_id) FROM "Order");

	END IF;
	RETURN NEW;
END;
$$;


-- прицепим триггер к таблице заказов
CREATE TRIGGER order_after_insert_employee_discount
	AFTER INSERT 
	ON "Order"
	FOR EACH ROW
	EXECUTE PROCEDURE discount();

-- посмотрим какие триггеры у нас есть в базе данных
select event_object_schema as table_schema,
       event_object_table as table_name,
       trigger_schema,
       trigger_name,
       string_agg(event_manipulation, ',') as event,
       action_timing as activation,
       action_condition as condition,
       action_statement as definition
from information_schema.triggers
group by 1,2,3,4,6,7,8;



-- внесем в таблицу заказов новый заказ, где заказчик является сотрудником
INSERT INTO "Order" VALUES ((SELECT MAX(order_id) FROM "Order") + 1, 3, 3, 60, 100, '2019-02-14 00:00:00', '2020-02-14 00:00:00')

-- посмотрим на послений заказ и увидим, что скидка внесена
select * from "Order" where order_id = (SELECT MAX(order_id) FROM "Order");

-- откатим внесенные изменения, если они не нужны 
ROLLBACK;

-- отключим триггер employee_discount от таблицы заказов
ALTER TABLE "Order" 
DISABLE TRIGGER order_after_insert_employee_discount;

-- удалим триггер
DROP TRIGGER order_after_insert_employee_discount ON "Order";

-- удалим функцию
DROP FUNCTION discount;




-- 2.2 если в таблице пользователей происходит обновление и сотрудник перестает им быть, 
-- то все его заказы увеличиваются в цене на 20 процентов, а если становится сотрудником, 
-- то уменьшаются на 20 процентов, если обновление в части установки номера поля is_staff 
-- происходит некорректно, то не позволяет их провести и выбрасывает исключение 

-- начнем транзакцию, чтобы потом можно было отменить изменения
BEGIN;


CREATE OR REPLACE FUNCTION users_discounts_before_update_is_staff() 
	RETURNS TRIGGER 
	LANGUAGE PLPGSQL
	AS
	$$
BEGIN
IF OLD.is_staff = 1 AND NEW.is_staff = 0 then
	UPDATE "Order" o SET total = total*1.25
	WHERE order_id IN (SELECT o.order_id FROM users u 
	JOIN carts c ON c.users_user_id = u.user_id 
	JOIN "Order" o ON o.carts_cart_id = c.cart_id
	WHERE u.user_id = NEW.user_id);

ELSIF OLD.is_staff = 0 AND NEW.is_staff = 1 then
	UPDATE "Order" o SET total = total*0.8
	WHERE order_id IN (SELECT o.order_id FROM users u 
	JOIN carts c ON c.users_user_id = u.user_id 
	JOIN "Order" o ON o.carts_cart_id = c.cart_id
	WHERE u.user_id = NEW.user_id);
END IF;
	
IF NEW.is_staff NOT IN (0, 1) THEN
	RAISE EXCEPTION 'Is_staff must be 0 or 1';
END IF;

RETURN NEW;
END;
$$;

-- прицепим триггер к таблице заказов
CREATE TRIGGER users_before_update_is_staff
	BEFORE UPDATE 
	ON users
	FOR EACH ROW
	EXECUTE PROCEDURE users_discounts_before_update_is_staff();


-- посмотреть по третьему пользователя заказы
 	SELECT u.user_id, u.is_staff, o.total, o.order_id FROM "Order" o 
	JOIN carts c ON o.carts_cart_id = c.cart_id 
	JOIN users u ON c.users_user_id = u.user_id 
	WHERE u.user_id = 3;

-- посмотреть на изменения стоимости заказов при изменении is_staff, на примере тертьего пользователя
-- is_staff = 0, is_staff = 1 
UPDATE users SET is_staff = 1
WHERE user_id = 3;

-- или is_staff = 1 - выбросит исключение и не даст внести изменения в таблицу если is_staff не равен 0 или 1    
UPDATE users SET city = 'city 123', is_staff = 2
WHERE user_id = 3;

-- откатим внесенные изменения, если они не нужны
ROLLBACK;













