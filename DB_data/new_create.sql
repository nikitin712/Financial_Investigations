-- drop
BEGIN;
DROP TABLE IF EXISTS public."Cases_Bodies";
DROP TABLE IF EXISTS public."Cases";
DROP TABLE IF EXISTS public."Transactions";
DROP TABLE IF EXISTS public."Accounts";
DROP TABLE IF EXISTS public."Bodies";
DROP TABLE IF EXISTS public."Persons";
DROP TABLE IF EXISTS public."Cities";
END;

--create
BEGIN;


CREATE TABLE IF NOT EXISTS public."Persons"
(
    person_id integer NOT NULL,
    last_name character varying(32) NOT NULL,
    first_name character varying(32) NOT NULL,
    second_name character varying(32),
    birthday date NOT NULL,
    city_id integer,
    PRIMARY KEY (person_id)
);

CREATE TABLE IF NOT EXISTS public."Cities"
(
    city_id integer NOT NULL,
    city_name character varying(30) NOT NULL,
    PRIMARY KEY (city_id)
);

CREATE TABLE IF NOT EXISTS public."Accounts"
(
    account_id integer NOT NULL,
    account_number character varying(20) NOT NULL DEFAULT '0000000000000000',
    body_id integer,
    open_date timestamp without time zone,
    close_date timestamp without time zone,
    PRIMARY KEY (account_id)
);

CREATE TABLE IF NOT EXISTS public."Bodies"
(
    body_id integer NOT NULL,
    body_type character varying(3) NOT NULL,
    "INN" character varying(12) NOT NULL,
    body_name character varying(100),
    start_date date,
	end_date date,
    "CEO_id_or_person_id" integer NOT NULL,
	parent_body integer,
    PRIMARY KEY (body_id)
);

CREATE TABLE IF NOT EXISTS public."Transactions"
(
    trans_id integer NOT NULL,
    acc_from integer NOT NULL,
    acc_to integer NOT NULL,
	trans_date date NOT NULL,
    amount numeric(20, 2) NOT NULL,
    description character varying(100),
    PRIMARY KEY (trans_id)
);

CREATE TABLE IF NOT EXISTS public."Cases"
(
    case_id integer NOT NULL,
    start_date date NOT NULL,
    end_date date,
    description character varying(100),
    law_number character varying(30),
    PRIMARY KEY (case_id)
);

CREATE TABLE IF NOT EXISTS public."Cases_Bodies"
(
    case_id integer NOT NULL,
    body_id integer NOT NULL,
    PRIMARY KEY (case_id, body_id)
);

ALTER TABLE IF EXISTS public."Persons"
    ADD FOREIGN KEY (city_id)
    REFERENCES public."Cities" (city_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Accounts"
    ADD FOREIGN KEY (body_id)
    REFERENCES public."Bodies" (body_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Bodies"
    ADD FOREIGN KEY ("CEO_id_or_person_id")
    REFERENCES public."Persons" (person_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;
	
ALTER TABLE IF EXISTS public."Bodies"
    ADD FOREIGN KEY ("parent_body")
    REFERENCES public."Bodies" (body_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Transactions"
    ADD FOREIGN KEY (acc_from)
    REFERENCES public."Accounts" (account_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Transactions"
    ADD FOREIGN KEY (acc_to)
    REFERENCES public."Accounts" (account_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Cases_Bodies"
    ADD FOREIGN KEY (case_id)
    REFERENCES public."Cases" (case_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Cases_Bodies"
    ADD FOREIGN KEY (body_id)
    REFERENCES public."Bodies" (body_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

END;



--insert
BEGIN;
INSERT INTO public."Cities" VALUES
(1, 'Moscow'),
(2, 'St. Petersberg'),
(3, 'Sochi'),
(4, 'Ekaterinburg'),
(5, 'Vladimir'),
(6, 'Kazan'),
(7, 'Krasnogorsk'),
(8, 'Nizhniy Novgorod'),
(9, 'Samara'),
(10, 'Chelyabinsk');

-- id, last, first, second, birthday, city
INSERT INTO public."Persons" VALUES
(1, 'Blinovskaya', 'Elena', 'Olegovna', '1981-08-25', 1),
(2, 'Vasiliev', 'Nikolay', 'Vladimirovich', '2000-01-01', 4),
(3, 'Kravcev', 'Ivan', 'Borisovich', '1995-04-25', 9),
(4, 'Strelnikova', 'Yula', 'Grigorevna', '1972-11-11', 5),
(5, 'Levushkin', 'Marat', 'Yusupovich', '1980-03-17', 1),
(6, 'Trolin', 'Viktor', NULL, '1985-06-07', 1);

-- id, type, INN, name, start, end, owner, parent_comp 
INSERT INTO public."Bodies" VALUES
(1, 'ENT', '111222333444', 'Vasilek', '2015-06-09', Null, 3, Null),
(2, 'OOO', '5555566666', 'MetallNew', '2003-02-26', Null, 1, Null),
(3, 'OOO', '7777788888', 'Gorgeus', '2011-11-11', '2025-03-02', 2, Null),
(4, 'GUP', '3434343434', 'MetallOld', '2010-10-19', Null, 1, Null),
(5, 'GUP', '1010101010', 'Kommercia', '2023-09-10', Null, 6, Null),
(6, 'OOO', '1234512345', 'TransSib', '2024-01-02', Null, 2, Null),
(7, 'fiz', '760303376240', Null, Null, Null, 1, Null),
(8, 'fiz', '123456789010', Null, Null, Null, 2, Null),
(9, 'fiz', '109876543210', Null, Null, Null, 3, Null),
(10, 'fiz', '111122223333', Null, Null, Null, 4, Null),
(11, 'fiz', '444455556666', Null, Null, Null, 5, Null),
(12, 'fiz', '777788889999', Null, Null, Null, 6, Null),
(13, 'OOO', '7777777777', 'NewOldBlinov', '2015-12-31', Null, 1, 4);

INSERT INTO public."Accounts" VALUES
(1, '11111111111111111111', 2, '2003-02-26', Null),
(2, '22222222222222222222', 2, '2005-04-24', Null),
(3, '12121212121212121212', 4, '2010-10-19', Null),
(4, '21212121212121212121', 4, '2020-01-04', Null),
(5, '33333333333333333333', 13, '2015-12-31', Null),
(6, '44444444444444444444', 1, '2015-06-09', Null),
(7, '55555555555555555555', 3, '2011-11-11', '2025-03-02'),
(8, '77777777777777777777', 7, '2016-07-07', Null);

INSERT INTO public."Transactions" VALUES
(1, 1, 2, '2005-04-26', 20000000.10, Null),
(2, 1, 2, '2005-05-30', 40000000.10, Null),
(3, 2, 1, '2010-05-05', 30000.10, Null),
(4, 1, 3, '2020-11-11', 200000.10, Null),
(5, 1, 4, '2021-12-12', 12345.10, Null),
(6, 4, 2, '2021-12-12', 12345.10, Null),
(7, 4, 3, '2021-12-15', 100000000.10, Null),
(8, 6, 7, '2015-03-04', 120000.00, Null),
(9, 1, 8, '2022-03-03', 100000000.20, Null),
(10, 7, 8, '2013-05-05', 10000.10, Null),
(11, 8, 5, '2018-06-06', 2300.10, Null);

END;


-- ROLLBACK;