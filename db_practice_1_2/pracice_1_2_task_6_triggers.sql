-- Задание 6
-- Добавить 2 триггера (один из них ДО операции по изменению данных, второй после) и функции или процедуры-обработчики к ним.


-- создадим два триггера, которые не дают изменить имя пользователя, на такое, которое уже существует

-- 1й до обновления
CREATE OR REPLACE FUNCTION fun_customer_before_update() 
	RETURNS TRIGGER 
	LANGUAGE PLPGSQL
	AS
	$$

declare
    count_name int := 0;
BEGIN
	select count(customer_id) into count_name from customer
	where name = NEW.name;
	
	IF count_name > 0 then
	
	raise notice 'A customer % already exists', NEW.name;
	rollback;
	END IF;
	
	RETURN NEW;
END;
$$;
	
	
CREATE TRIGGER trig_customer_before_update
	BEFORE UPDATE 
	ON customer
	FOR EACH ROW
	EXECUTE PROCEDURE fun_customer_before_update();
	
update customer set name = 'customer name 1' where customer_id = 2;

select * from customer;	


DROP TRIGGER trig_customer_before_update ON customer;
	
	
-- 2й триггер - после обновления
	
CREATE OR REPLACE FUNCTION fun_customer_after_update() 
	RETURNS TRIGGER 
	LANGUAGE PLPGSQL
	AS
	$$

declare
    count_name int := 0;
BEGIN
	select count(customer_id) into count_name from customer
	where name = NEW.name;
	
	IF count_name > 0 then
	
	raise notice 'A customer % already exists', NEW.name;
	rollback;
	END IF;
	
	RETURN NEW;
END;
$$;
	
	
CREATE TRIGGER trig_customer_after_update
	AFTER UPDATE 
	ON customer
	FOR EACH ROW
	EXECUTE PROCEDURE fun_customer_after_update();
	
update customer set name = 'customer name 1' where customer_id = 3;
select * from customer;

rollback;
	
DROP TRIGGER trig_customer_after_update ON customer;
