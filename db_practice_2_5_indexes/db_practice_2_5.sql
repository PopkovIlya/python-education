-- Задание:
-- Придумать 3 запроса, которые можно оптимизировать с помощью индекса (проверять
-- стоит ли оптимизировать запрос оператором explain) и оптимизировать их
-- используя индекс. Результат проверять также оператором explain.


-- Первый запрос

-- Смотрим как будет производится поиск планировщиком без индекса в таблице заказов
EXPLAIN SELECT * FROM "Order" WHERE order_status_order_status_id = 1;  
-- Seq Scan on "Order"  (cost=0.00..31.75 rows=280 width=39)

-- Создадим индекс в таблице "Order" для поля order_status_order_status_id на основе двоичного дерева
CREATE INDEX idx_order_order_status_order_statu_id
    ON "Order" USING btree (order_status_order_status_id);
    
-- Смотрим как планировщик будет производить поиск с индексом
EXPLAIN SELECT * FROM "Order" WHERE order_status_order_status_id = 1; 
-- Bitmap Heap Scan on "Order"  (cost=6.45..22.95 rows=280 width=39)

-- Вывести какие есть индексы в таблице заказов
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'Order'; 

-- Удалим созданный индекс
DROP INDEX idx_order_order_status_order_statu_id;


-- Второй запрос

-- Смотрим как будет производится поиск планировщиком без индекса в таблице пользователей
EXPLAIN SELECT * FROM users WHERE email = 'email3000@gmail.com';  
-- Seq Scan on users  (cost=0.00..99.12 rows=1 width=147)

-- Создадим уникальный индекс в таблице пользователей для поля электронной почты на основе двоичного дерева
CREATE INDEX idx_unq_users_email ON users USING btree (email);   

-- Смотрим как планировщик будет производить поиск с индексом
EXPLAIN SELECT * FROM users WHERE email = 'email3000@gmail.com'; 
-- Index Scan using idx_unq_users_email on users  (cost=0.28..8.30 rows=1 width=147)


-- Третий запрос

-- Добавим индекс в таблицу пользователей на колонку электронной почты на основе хэшей
CREATE INDEX idx_unq_hash_users_email ON users USING hash (email);

-- Смотрим как планировщик будет производить поиск с двумя индексами 
EXPLAIN SELECT * FROM users WHERE email = 'email3000@gmail.com';
-- Вывод: Index Scan using idx_unq_hash_users_email on users  (cost=0.00..8.02 rows=1 width=147)
-- Видим, что для такого поиска хэш немного улучшил ситуацию

