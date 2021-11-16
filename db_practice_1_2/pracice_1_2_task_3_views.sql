Задание 3
Создать 3 представления (1 из них должно быть материализированным и хранить данные от "тяжелого" запроса).

-- Выбрать все данные по всем заказам и только имена тех заказчиков, чей заказ состваил больше 400
CREATE OR REPLACE VIEW customers_name_where_price_more_400 AS
SELECT c.name , ord.* FROM "Order" ord 
LEFT JOIN customer c ON c.customer_id = ord.customer_id 
WHERE  ord.price > 400;

SELECT * FROM customers_name_where_price_more_400;


-- выбрать все данные по всем филиалам и только те заказы где модель машины была равной 3
CREATE OR REPLACE VIEW all_branch_and_orders_where_model_car_3 AS
SELECT b.branch_number as branch_branch_number, ord.* FROM "Order" ord 
RIGHT JOIN branch b ON b.branch_number = ord.branch_number 
JOIN car ON ord.car_number = car.car_number WHERE car.model_id = 3;

SELECT * FROM all_branch_and_orders_where_model_car_3;

DROP VIEW IF EXISTS all_branch_and_orders_where_model_car_3;



-- Выбрать все данные по всем заказам и только имена тех заказчиков, чей заказ состваил больше 400
CREATE OR REPLACE VIEW all_branch_and_orders_where_model_car_3 AS
SELECT b.branch_number as branch_branch_number, ord.* FROM "Order" ord 
RIGHT JOIN branch b ON b.branch_number = ord.branch_number 
JOIN car ON ord.car_number = car.car_number WHERE car.model_id = 3;

SELECT * FROM all_branch_and_orders_where_model_car_3;

DROP VIEW IF EXISTS all_branch_and_orders_where_model_car_3;



-- Выбрать все заказы где клиенты проживают по адрессу в диапазоне (address 30-50), которые сделали заказ на более чем на 300 деняк, и двигателем первой модели
-- с двигателем 'model engine 1'
CREATE MATERIALIZED VIEW orders_customer_address_30_50_model_eng_1_more_300
AS
SELECT a.address, ord.* FROM "Order" ord 
JOIN customer c ON c.customer_id = ord.customer_id 
JOIN car ON car.car_number = ord.car_number 
JOIN engine e ON e.engine_id = car.engine_id
JOIN customer_address ca ON c.customer_id = ca.customer_id
JOIN address a ON ca.address_id = a.address_id
WHERE  (e.engine = 'model engine  5') AND (a.address LIKE 'address 3_' OR a.address LIKE 'address 4_' OR a.address LIKE 'address 50') and ord.price >300
WITH NO DATA;

REFRESH MATERIALIZED VIEW orders_customer_address_30_50_model_eng_1_more_300;

SELECT * FROM orders_customer_address_30_50_model_eng_1_more_300;

DROP MATERIALIZED VIEW IF EXISTS orders_customer_address_30_50_model_eng_1_more_300;



