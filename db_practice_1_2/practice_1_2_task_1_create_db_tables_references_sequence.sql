Для всех нижеприведенных заданий используй субд PostgreSql и созданную ER диаграмму в задании "ER Diagram". Все команды сохранить в отдельные файлы для каждого задания.

Задание 1
Создать бд, создать таблицы, добавить связи между таблицами, заполнить таблицу данными (их нужно сгенерировать в большом количестве - для этого можно использовать последовательности, собственные или встроенные функции - никаких внешних генераторов).

-- внесенные изменения 
-- 1 - в таблице адресов номер филиала не является внешним ключом, иначе все адреса должны иметь номер филиала, а от адресов так же зависят адреса клиентов, что нам не подходит (или отдельно адресс вынести в поле филиалов, наверное так было бы лучше, но идем по тдиаграмме. (на диаграмме считать ограничение внешнего ключа на поле branch_id недействительным, но само поле остается) 
-- 2 - между таблицами филиалов и номеров телефоном установлена связь один ко многим и это требует создания поля в таблице телефоном с номером филиала, в общем будем счиать что связь один к одному и без наложения ограничения внешнего ключа (так сказать мы просто собираем все телефоны в одну таблицу).

-- Задание 1
-- создадим базу данных
CREATE DATABASE car_rental;

-- создадим таблицы

begin transaction;

CREATE TABLE IF NOT EXISTS address (
	address_id SERIAL NOT NULL PRIMARY KEY ,
	branch_id INT,
	address VARCHAR(255));
	
CREATE TABLE IF NOT EXISTS customer_address (
	address_id INT,
	customer_id INT);
	

CREATE TABLE IF NOT EXISTS customer (
	customer_id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(255));
	
CREATE TABLE IF NOT EXISTS customers_phone (
	phone_number INT,
	customer_id INT);
	
CREATE TABLE IF NOT EXISTS phone (
	phone_number INT NOT NULL PRIMARY KEY);

CREATE TABLE IF NOT EXISTS branch (
	branch_number SERIAL NOT NULL PRIMARY KEY,
	phone_number INT); 
	
CREATE TABLE IF NOT EXISTS "Order" (
	order_id SERIAL NOT NULL PRIMARY KEY,
	date_of_renting date NOT NULL,
	car_number INT NOT NULL,
	price INT NOT NULL,
	period_renting INT NOT NULL,
	branch_number INT NOT NULL,
	customer_id INT NOT NULL);

CREATE TABLE IF NOT EXISTS car(
	car_number INT NOT NULL PRIMARY KEY,
	car_manufacturer char,
	model_id INT NOT NULL,
	engine_id INT NOT NULL);
	
CREATE TABLE IF NOT EXISTS model_car (
	model_id SERIAL NOT NULL PRIMARY KEY,
	model VARCHAR(255));

CREATE TABLE IF NOT EXISTS engine (
	engine_id SERIAL NOT NULL PRIMARY KEY,
	engine VARCHAR(255));
	
COMMIT;




BEGIN;


ALTER TABLE customer_address ADD FOREIGN KEY (address_id)
REFERENCES address(address_id);

ALTER TABLE customer_address ADD FOREIGN KEY (customer_id)
REFERENCES customer(customer_id);
  
ALTER TABLE customers_phone ADD FOREIGN KEY (customer_id)
REFERENCES customer(customer_id);

ALTER TABLE customers_phone ADD FOREIGN KEY (phone_number)
REFERENCES phone(phone_number);

ALTER TABLE "Order" ADD FOREIGN KEY (car_number)
REFERENCES car(car_number);

ALTER TABLE "Order" ADD FOREIGN KEY (branch_number)
REFERENCES branch(branch_number);

ALTER TABLE "Order" ADD FOREIGN KEY (customer_id)
REFERENCES customer(customer_id);

ALTER TABLE car ADD FOREIGN KEY (model_id)
REFERENCES model_car(model_id);

ALTER TABLE car ADD FOREIGN KEY (engine_id)
REFERENCES engine(engine_id);

COMMIT;




-- Заполним таблицы с использованием последовательностей

-- заполняем таблицу адресов (будет 100 адресов и 20 из них принадлежат филиалам, остальные будут за клиентами (21 - 100

begin transaction;


DROP SEQUENCE seq_address_address;
DROP SEQUENCE seq_address_branch_id;

CREATE SEQUENCE IF NOT EXISTS seq_address_address 
    INCREMENT 1
	MINVALUE 1
	MAXVALUE 101
    START 1;
	
CREATE SEQUENCE IF NOT EXISTS seq_address_branch_id 
    INCREMENT 1
	MINVALUE 1
	MAXVALUE 101
    START 1;

-- если не первый раз в транзакции запускаем, то стоит запустить последовательность первичных ключов таблицы адресов с 1, ну для ровноты счета
ALTER SEQUENCE IF EXISTS address_address_id_seq RESTART WITH 1;

do $$
begin
	for counter in 1..100
		loop
			if counter < 21 then
				insert into address(branch_id, address) values(nextval('seq_address_branch_id'), ('address ' || nextval('seq_address_address') :: text) );
			else
				insert into address(branch_id, address) values(NULL, ('address ' || nextval('seq_address_address') :: text) );
			end if;
		end loop;
end; $$;


-- посмотрим что внесли
select * from address;

-- зафиксируем внесенные данные и закончим транзакцию
commit;

-- можем удалить последовательности, но не стоит, потому что мы их еще используем
-- DROP SEQUENCE seq_address_address;
-- DROP SEQUENCE seq_address_branch_id;



-- внесем данные в таблицу пользователей, помним что на custome_id наложена последовательность через serial)

-- начнем транзакцию
BEGIN;

-- обновим старую последовательность, чтобы ее можно было по новой использовать (можно и так, но лучше чтобы с единицы начиналось, так понятней)
ALTER SEQUENCE IF EXISTS seq_address_address RESTART WITH 1;
-- а это чтобы обнулить до единицы serial наложенный на customer_id, на всякий случай 
ALTER SEQUENCE IF EXISTS customer_customer_id_seq RESTART WITH 1

do $$
begin
	for counter in 1..80
		loop
			insert into customer("name") values(('customer name ' || nextval('seq_address_address') :: text) );
		end loop;
end; $$;

-- посмотрим что внесли
select * from customer;

-- зафиксируем
commit;


-- внесем данные в таблицу customer_address
BEGIN;

-- используем наши уже созданные последовательности
ALTER SEQUENCE IF EXISTS seq_address_address RESTART WITH 21 MAXVALUE 100 NO CYCLE;
ALTER SEQUENCE IF EXISTS seq_address_branch_id RESTART WITH 1 MAXVALUE 100 NO CYCLE;

begin;

do $$
begin
	for counter in 1..80
		loop
			insert into customer_address values(nextval('seq_address_address'), nextval('seq_address_branch_id'));
		end loop;
end; $$

-- посмотрим что внесли
select * from customer_address;


-- зафиксируем
commit;



-- заполняем талицу телефонов (тоже 100 телефонов, первых 20 кторых принадлежат филиалам)
begin transaction;


CREATE SEQUENCE IF NOT EXISTS seq_phone 
    INCREMENT 1
	MINVALUE 30950000
	MAXVALUE 31950000
    START 30950000;


do $$
begin
	for counter in 1..100
		loop
			insert into phone values(nextval('seq_phone'));
		end loop;
end; $$;

select * from phone;

-- DROP SEQUENCE seq_phone;
-- select currval('seq_phone')
commit;




-- заполняем талицу customer_phone (тоже 100 телефонов, первых 20 кторых принадлежат филиалам)

ALTER SEQUENCE IF EXISTS seq_phone RESTART WITH 30950020;
ALTER SEQUENCE IF EXISTS seq_address_branch_id RESTART WITH 1;

begin transaction;


do $$
begin
	for counter in 1..80
		loop
			insert into customers_phone values(nextval('seq_phone'), nextval('seq_address_branch_id'));
		end loop;
end; $$;

select * from customers_phone;

commit;


-- заполняем талицу branch (первых 20 в таблице phone принадлежат филиалам)
ALTER SEQUENCE IF EXISTS seq_phone RESTART WITH 30950000;
ALTER SEQUENCE IF EXISTS seq_address_branch_id RESTART WITH 1;

begin transaction;

do $$
begin
	for counter in 1..20
		loop
			insert into branch values(nextval('seq_address_branch_id'), nextval('seq_phone'));
		end loop;
end; $$;

select * from branch;

commit;



-- заполняем талицу model_car (пусть будет 10), используем всю ту же созданную ранее последовательность и цикл
ALTER SEQUENCE IF EXISTS seq_address_branch_id RESTART WITH 1;

begin transaction;

do $$
begin
	for counter in 1..10
		loop
			insert into model_car(model) values(('model number  ' || nextval('seq_address_branch_id') :: text) );
		end loop;
end; $$;

select * from model_car;

commit;



-- заполняем талицу engine (пусть будет 5), используем всю ту же созданную ранее последовательность и цикл
ALTER SEQUENCE IF EXISTS seq_address_branch_id RESTART WITH 1;

begin transaction;

do $$
begin
	for counter in 1..5
		loop
			insert into engine(engine) values(('model engine  ' || nextval('seq_address_branch_id') :: text) );
		end loop;
end; $$;

select * from engine;

commit;


-- заполняем талицу car (пусть будет 20), используем всю те же созданные ранее последовательности, но с добавлением циклов в них и цикл. В том числе создадим последовательность для заполнения поля car_number будем считать, что у номера машины 4х числовой номер, а производитель у всех машин opel

CREATE SEQUENCE IF NOT EXISTS seq_car_car_number 
    INCREMENT 1
	MINVALUE 1000
	MAXVALUE 2000
    START 1000;

ALTER SEQUENCE IF EXISTS seq_address_branch_id RESTART WITH 1 MAXVALUE 5 CYCLE;
ALTER SEQUENCE IF EXISTS seq_address_address RESTART WITH 1  MAXVALUE 10 CYCLE;



ALTER TABLE car ALTER COLUMN car_manufacturer TYPE text;

begin transaction;

do $$
begin
	for counter in 1..20
		loop
			insert into car(car_number, car_manufacturer, model_id, engine_id) 
			values(
			nextval('seq_car_car_number'), 'opel', nextval('seq_address_address'), nextval('seq_address_branch_id') 
			);
		end loop;
end; $$;

select * from car;

commit;


-- заполняем таблицу заказов. пусть их будет 80 (как и клиентов)

ALTER SEQUENCE IF EXISTS seq_address_branch_id RESTART WITH 1 MAXVALUE 20 CYCLE;
ALTER SEQUENCE IF EXISTS seq_address_address RESTART WITH 1  MAXVALUE 80 CYCLE;
ALTER SEQUENCE IF EXISTS seq_car_car_number RESTART WITH 1000 MAXVALUE 1019 CYCLE;

CREATE SEQUENCE IF NOT EXISTS seq_order_period_renting
	INCREMENT 1
	MINVALUE 1
	MAXVALUE 5
    START 1
	CYCLE;
	
CREATE SEQUENCE IF NOT EXISTS seq_order_price
	INCREMENT 100
	MINVALUE 100
	MAXVALUE 500
    START 100
	CYCLE;
	
	
begin transaction;

do $$
begin
for counter in 1..80
	loop
		insert into "Order"(date_of_renting, 
			car_number, 
			period_renting, 
			price, 
			branch_number, 
			customer_id)
		values(
			now()+ counter*(interval '1 day'),
			nextval('seq_car_car_number'),
			nextval('seq_order_period_renting'),
			nextval('seq_order_price'),
			nextval('seq_address_branch_id'), 
			nextval('seq_address_address')
			);			
	end loop;
end; $$;

-- select * from "Order";
commit;

