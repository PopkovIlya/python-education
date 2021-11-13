--Задание:
--Написать 3 представления для таблицы products, для таблиц order_status и order, для таблиц products и category.
--Создать материализированное представление для "тяжелого" запроса на свое усмотрение.
--Не забыть сделать запросы для удаления представлений.


-- запросы для таблциы products:
-- 1_products - вывести первую десятку товаров цена которых больше 300, а количество больше 40
CREATE OR REPLACE VIEW products_too_many_products AS
SELECT product_id, product_title, (in_stock - 40) AS excess_goods, 
(in_stock - 40)*price AS cost_excess_goods FROM products 
WHERE (in_stock > 40 AND price > 300 AND (in_stock - 40)*price > 0) ORDER BY cost_excess_goods DESC;

-- Вызов представления
SELECT * FROM products_too_many_products;


-- 2_products - вывести все товары общая стоимость которых больше 10000 
CREATE OR REPLACE VIEW products_max_total_price AS
SELECT product_id, product_title, price*in_stock AS total_price FROM products
WHERE price*in_stock > 10000 ORDER BY price*in_stock DESC; 

-- Вызов представления
SELECT * FROM products_max_total_price;


-- 3_products - на основе двух предыдущих преставлений выведим десятку товаров входящие в обе группы, которые не стоит закупать в ближайшее время
CREATE OR REPLACE VIEW products_no_need_buy AS
SELECT product_id, p.product_title, total_price, excess_goods, cost_excess_goods FROM products_too_many_products p
JOIN products_max_total_price USING(product_id) ORDER BY total_price DESC LIMIT 10;

-- Вызов представления
SELECT * FROM products_no_need_buy;

-- Удалим созданные представления
DROP VIEW IF EXISTS products_no_need_buy;
DROP VIEW IF EXISTS products_too_many_products;
DROP VIEW IF EXISTS products_max_total_price;

--Проверим что удалили
SELECT table_name
FROM INFORMATION_SCHEMA.views
WHERE table_schema = ANY(current_schemas(false));




-- 1_products_category выберем все товары в категории 1 количество которых больше 40 (в предположении что их слишком много хранится)
CREATE OR REPLACE VIEW products_category_too_many_products_first_category AS
  SELECT p.product_id, p.in_stock, c.category_title AS category
  FROM products p JOIN categories c USING(category_id) WHERE category_id = 1 AND p.in_stock > 40 ORDER BY p.in_stock DESC;

-- Вызов представления
SELECT * FROM products_too_many_products;


-- 2_products_category Выведем по названиям продуктов деньги вложеные в излишний товар (тех что болше 40)
CREATE OR REPLACE VIEW products_cost_surplus_products AS
  SELECT products.product_title, (p.in_stock - 40)*products.price AS surplus_amount 
  FROM products_category_too_many_products_first_category p 
  JOIN products USING(product_id) ORDER BY surplus_amount DESC;

-- Вызов представления
SELECT * FROM products_cost_surplus_products;



-- 3_products_category Выведим самую многочисленную категорию товаров

CREATE OR REPLACE VIEW products_category_largest_category AS
SELECT c.category_id, c.category_title, SUM(p.in_stock) AS all_goods_in_category FROM categories c 
  JOIN products p USING(category_id) GROUP BY category_id ORDER BY all_goods_in_category DESC;

-- Вызов представления
SELECT * FROM products_category_largest_category;


-- Удалим созданные представления
DROP VIEW IF EXISTS products_category_too_many_products_first_category;
DROP VIEW IF EXISTS products_too_many_products;
DROP VIEW IF EXISTS products_category_largest_category;


-- Проверим что удалили
SELECT table_name
FROM INFORMATION_SCHEMA.views
WHERE table_schema = ANY(current_schemas(false));



-- 1_order_status_order Выведим количество заказов по их состояни, кроме статусов 4 (Finished) и 5 (Canceled) 
CREATE OR REPLACE VIEW order_status_order_condition_conut_orders AS  
  SELECT s.order_status_id, s.status_name, COUNT(o.order_status_order_status_id) AS total_number_orders 
FROM order_status s 
JOIN "Order" o 
ON s.order_status_id = o.order_status_order_status_id 
WHERE s.order_status_id NOT IN (4, 5)
GROUP BY s.order_status_id ORDER BY total_number_orders DESC;
  
  
-- Вызов представления
SELECT * FROM order_status_order_condition_conut_orders;



-- 2_order_status_order Выведим заказы, которые были созданы в 2017 году и имеют статус заказа "In progress" (order_status_id = 2),
-- в порядке по возрастанию даты (от самых ранних) и по убыванию цены заказа (от самых дорогих к дешевым)
CREATE OR REPLACE VIEW order_status_order_in_progress_2017 AS  
    SELECT o.order_id, o.total, o.created_at
FROM "Order" o  
JOIN order_status s
ON s.order_status_id = o.order_status_order_status_id 
WHERE (o.created_at BETWEEN '2017-01-01' AND '2017-12-31') AND s.order_status_id = 2
ORDER BY o.created_at ASC, o.total DESC;


-- Вызов представления
SELECT * FROM order_status_order_in_progress_2017;



-- 3_order_status_order Выведим 10ку самых дорогих оплаченных заказов (order_status_id = 3, status_name = Paid),
-- в порядке по убыванию стоимости

CREATE OR REPLACE VIEW order_status_order_most_expensive_paid_orders AS  
    SELECT o.order_id, o.total, o.created_at
FROM "Order" o  
JOIN order_status s
ON s.order_status_id = o.order_status_order_status_id 
WHERE s.status_name = 'Paid'
ORDER BY o.total DESC LIMIT 10;


-- Вызов представления
SELECT * FROM order_status_order_most_expensive_paid_orders;

-- Удалим созданные представления
DROP VIEW IF EXISTS order_status_order_condition_conut_orders;
DROP VIEW IF EXISTS order_status_order_in_progress_2017;
DROP VIEW IF EXISTS order_status_order_most_expensive_paid_orders;

-- Проверим что удалили
SELECT table_name
FROM INFORMATION_SCHEMA.views
WHERE table_schema = ANY(current_schemas(false));




-- 1_MATERIALIZED ВЫведим сумму законченных заказов по городам с 1 по 17
CREATE MATERIALIZED VIEW completed_orders_by_city_1_17
AS
SELECT u.city, SUM(o.total) AS in_city_total_spend  FROM "Order" o 
JOIN order_status s ON s.order_status_id = o.order_status_order_status_id 
JOIN carts c ON c.cart_id = o.carts_cart_id
JOIN users u ON u.user_id = c.users_user_id
WHERE s.status_name = 'Finished' AND u.city LIKE 'city _' OR u.city LIKE 'city 1_' AND u.city NOT IN ('city 18', 'city 19')
GROUP BY u.city ORDER BY in_city_total_spend DESC
WITH NO DATA;


-- Загрузим данными 
REFRESH MATERIALIZED VIEW completed_orders_by_city_1_17;

-- посмотрим что загрузили
SELECT * FROM completed_orders_by_city_1_17;

-- удалим
DROP MATERIALIZED VIEW IF EXISTS completed_orders_by_city_1_17;


