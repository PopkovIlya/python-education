-- 1.1 (INSERT data) Вносим в талицы Users, carts и  Order нового пользователя, 
-- его корзину и закакз который он сделал, а потом отменяем ROLLBACK.
-- (Первичный ключ не генерируется автоматически ни в одной из таблиц)

BEGIN;

-- Смотрим по id:
SELECT user_id, c.cart_id, ord.order_id FROM users 
	JOIN carts c ON user_id = c.users_user_id 
	JOIN "Order" ord ON c.cart_id = ord.carts_cart_id 
	ORDER BY ord.order_id DESC;

INSERT INTO users VALUES(
	(SELECT MAX(user_id) FROM users) + 1, 'email_new_user_1', 
	'123', 'first_name_add_user', 'last_name_add_user', 
	'middle_name_add_user', 0, 'Country add_user', 'City add_user',
	'address add_user');

INSERT INTO carts(cart_id, users_user_id) 
VALUES((SELECT MAX(cart_id) FROM carts) + 1, 
	(SELECT MAX(user_id) FROM users) - 1);

INSERT INTO "Order"(order_id, carts_cart_id, order_status_order_status_id) 
VALUES((SELECT MAX(order_id) FROM "Order") + 1, (SELECT MAX(cart_id) FROM carts), 1);

-- Смотрим добавились ли наши данные (по id):
SELECT user_id, c.cart_id, ord.order_id FROM users 
	JOIN carts c ON user_id = c.users_user_id 
	JOIN "Order" ord ON c.cart_id = ord.carts_cart_id ORDER BY ord.order_id DESC;


-- Отменяем внесенные данные
ROLLBACK;



-- 1.2 (INSERT data, fail) Вносим в талицы Users, carts и  Order нового пользователя, 
-- его корзину и закакз который он сделал, не получается по причине того, 
-- что для "Order".order_status_order_status_id используем недопустимое значение 
-- индентификатора (6) которого нет в таблице order_status. Откатываем все обратно с 
-- помощью команды COMMIT (в случае ошибки автоматически вызовится ROLLBACK)

BEGIN;
INSERT INTO users VALUES(
	(SELECT MAX(user_id) FROM users) + 1, 'email_new_user_1', 
	'123', 'first_name_add_user', 'last_name_add_user', 
	'middle_name_add_user', 0, 'Country add_user', 'City add_user',
	'address add_user');

INSERT INTO carts(cart_id, users_user_id) 
VALUES((SELECT MAX(cart_id) FROM carts) + 1, (SELECT MAX(user_id) FROM users) - 1);

INSERT INTO "Order"(order_id, carts_cart_id, order_status_order_status_id) 
VALUES((SELECT MAX(order_id) FROM "Order") + 1, (SELECT MAX(cart_id) FROM carts), 6);

-- Отменяем внесенные данные
COMMIT;



-- 2. (UPDATE data) Обновляем в талицах Users, carts и  Order данные, а потом отменяем ROLLBACK.

BEGIN;

-- Смотрим по то что будем обновлять:
SELECT u.user_id, u.is_staff, c.cart_id, c.total, ord.order_id, ord.order_status_order_status_id FROM users u
	JOIN carts c ON user_id = c.users_user_id 
	JOIN "Order" ord ON c.cart_id = ord.carts_cart_id 
	WHERE u.user_id = 1;


UPDATE users SET is_staff = 1 WHERE user_id = 1;
UPDATE carts SET total = 200 WHERE users_user_id = 1;
UPDATE "Order" SET order_status_order_status_id = 1 WHERE carts_cart_id = 1;

-- Проверяем что обновилось
SELECT u.user_id, u.is_staff, c.cart_id, c.total, ord.order_id, ord.order_status_order_status_id FROM users u
	JOIN carts c ON user_id = c.users_user_id 
	JOIN "Order" ord ON c.cart_id = ord.carts_cart_id 
	WHERE u.user_id = 1;

-- отменяем обновление:
ROLLBACK;



--3. (DELETE) 

-- Удалим последовательно из таблицы "Order" и order_status данные, т.к. 
-- есть огранечения по внешнему ключу от таблицы order_status на таблицу "Order"
BEGIN;
DELETE FROM "Order" WHERE order_status_order_status_id = 1;
DELETE FROM order_status WHERE order_status_id = 1;

-- Отменим удаление
ROLLBACK;


-- Попробуем удалить из таблицы users позьзователя с id = 1, но это не получится из-за 
-- ограничений внешнего ключа, поэтому для отмены транзакции можем вызвать COMMIT 
-- который автоматически вызовет откат к прежнему состоянию (или ROLLBACK чтобы точно и не перепутать)

BEGIN;

DELETE FROM users WHERE user_id = 1;

COMMIT;



-- 4. (SAVEPOINT) 

-- Начнем транзакцию:
BEGIN;

-- Посмотрим на последний заказ в таблице заказов:
SELECT * FROM "Order" WHERE order_id = (SELECT MAX(order_id) FROM "Order");

-- Внесем новый заказ в таблицу заказов:
INSERT INTO "Order"(order_id, carts_cart_id, order_status_order_status_id) 
VALUES((SELECT MAX(order_id) FROM "Order") + 1, (SELECT MAX(cart_id) FROM carts), 1);

-- Проверим, что внесли новый заказ:
SELECT * FROM "Order" WHERE order_id = (SELECT MAX(order_id) FROM "Order");


-- Создадим точку сохранения, которая включает в себя внесенные данные в таблицу заказов:
SAVEPOINT insert_to_order;


-- Удалим внесенный заказ:
DELETE FROM "Order" WHERE order_id = (SELECT MAX(order_id) FROM "Order");

--Проверим, что новый заказ был удален:
SELECT * FROM "Order" WHERE order_id = (SELECT MAX(order_id) FROM "Order");


-- Теперь вернемся к состоянию, когда заказ внесен, но удаления не производилось:
ROLLBACK TO SAVEPOINT insert_to_order;

-- Проверим, что новый заказ в таблице
SELECT * FROM "Order" WHERE order_id = (SELECT MAX(order_id) FROM "Order");


-- Удалим точку сохранения (просто как демонстрация)
RELEASE SAVEPOINT insert_to_order;

-- Вернемся в к исходному состаянию, до начала транзакции, когда заказ не был внесен в таблицу
ROLLBACK;

-- Проверим, что нового заказа в таблице нет
SELECT * FROM "Order" WHERE order_id = (SELECT MAX(order_id) FROM "Order");


