
Задание 2
Придувать 3 различных запроса SELECT с осмысленным использованием разных видов JOIN.
Используя explain добавить только необходимые индексы для уменьшения стоимости (cost) запросов.



-- Выбрать все заказы где клиенты проживают по адрессу в диапазоне (address 30-50), которые сделали заказ на более чем на 300 деняк, и двигателем первой модели
-- с двигателем 'model engine 1'
SELECT a.address, ord.* FROM "Order" ord 
JOIN customer c ON c.customer_id = ord.customer_id 
JOIN car ON car.car_number = ord.car_number 
JOIN engine e ON e.engine_id = car.engine_id
JOIN customer_address ca ON c.customer_id = ca.customer_id
JOIN address a ON ca.address_id = a.address_id
WHERE  (e.engine = 'model engine  5') AND (a.address LIKE 'address 3_' OR a.address LIKE 'address 4_' OR a.address LIKE 'address 50') and ord.price >300;
 

-- Выбрать все данные по всем заказам и только имена тех заказчиков, чей заказ состваил больше 400
SELECT c.name , ord.* FROM "Order" ord 
LEFT JOIN customer c ON c.customer_id = ord.customer_id 
WHERE  ord.price > 400;

-- выбрать все данные по всем филиалам и только те заказы где модель машины была равной 3
SELECT b.branch_number , ord.* FROM "Order" ord 
RIGHT JOIN branch b ON b.branch_number = ord.branch_number 
JOIN car ON ord.car_number = car.car_number WHERE car.model_id = 3;




-- Использование индексов

-- Индексы рекомендованно использовать таблицах в которые реже вносятся или изменяются данные, 
-- но чаще по ним производят поиск и выборка данных, ссответственно лучше всего индексы использовать
-- на столбцах по которым и производится запрос   

-- Рассмотрим предыдущий запрос:

-- Выбрать все заказы где клиенты проживают по адрессу в диапазоне (address 30-50), которые сделали заказ на более чем на 300 деняк, и двигателем первой модели
-- с двигателем 'model engine  5'
SELECT a.address, ord.* FROM "Order" ord 
JOIN customer c ON c.customer_id = ord.customer_id 
JOIN car ON car.car_number = ord.car_number 
JOIN engine e ON e.engine_id = car.engine_id
JOIN customer_address ca ON c.customer_id = ca.customer_id
JOIN address a ON ca.address_id = a.address_id
WHERE  (e.engine = 'model engine  5') AND (a.address LIKE 'address 3_' OR a.address LIKE 'address 4_' OR a.address LIKE 'address 50') and ord.price >300;

-- здесь на подойдет, как и большенстве задач, наложение индекса с алгоритмом бинарного дерева, т.к. в предикате используется сравнение и оператор LIKE
-- в зависимости от размеров таблиц и того как часто они обновляются стоит вносить индекс, очевидно, что двигатели будут реже изменятьс и дополняться, чем таблица с пользователями,
-- но таблица с пользователями, скорее всего, будет значительно больше, поэтому в целях оптимизации создадим индекс колонок обоих таблиц, которые используются в предикате

-- но в начале посмотрим как планировщик будет проводить поиск без внесения индексов

EXPLAIN SELECT a.address, ord.* FROM "Order" ord 
JOIN customer c ON c.customer_id = ord.customer_id 
JOIN car ON car.car_number = ord.car_number 
JOIN engine e ON e.engine_id = car.engine_id
JOIN customer_address ca ON c.customer_id = ca.customer_id
JOIN address a ON ca.address_id = a.address_id
WHERE  (e.engine = 'model engine  5') AND (a.address LIKE 'address 3_' OR a.address LIKE 'address 4_' OR a.address LIKE 'address 50') and ord.price >300;
 
-- теперь создадим индексы
BEGIN TRANSACTION;

CREATE INDEX idx_engine_engine
    ON engine USING btree (engine);

CREAE INDEX idx_address_address
	ON address USING btree (address);

-- снова взглянем на то как планировщик будет проводит поиск и сраним показатель cost

EXPLAIN SELECT a.address, ord.* FROM "Order" ord 
JOIN customer c ON c.customer_id = ord.customer_id 
JOIN car ON car.car_number = ord.car_number 
JOIN engine e ON e.engine_id = car.engine_id
JOIN customer_address ca ON c.customer_id = ca.customer_id
JOIN address a ON ca.address_id = a.address_id
WHERE  (e.engine = 'model engine  5') AND (a.address LIKE 'address 3_' OR a.address LIKE 'address 4_' OR a.address LIKE 'address 50') and ord.price >300;


-- модем удалить индексы с помощью команд
DROP INDEX idx_engine_engine;
DROP INDEX idx_address_address;

COMMIT;




