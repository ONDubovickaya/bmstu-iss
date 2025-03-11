DROP TABLE entities;
DROP TABLE cases CASCADE;
DROP TABLE documents CASCADE;


CREATE TABLE IF NOT EXISTS cases (
    id SERIAL PRIMARY KEY,
    number VARCHAR(50),
    court VARCHAR(255),
    participants TEXT
);

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    date DATE,
    type VARCHAR(50),
    case_id INTEGER REFERENCES cases(id)
);

CREATE TABLE IF NOT EXISTS entities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(50),
    document_id INTEGER REFERENCES documents(id)
);


INSERT INTO cases (number, court, participants) VALUES
('СИП-162', 'Федеральная служба по интеллектуальной собственности', 'ООО "Четыре лапы", ООО"ГРУМ"'),
('21АП-6475', 'Арбитражный суд города Севастополя', 'Геворгян Геворг Хачикович'),
('А73-2806', 'Арбитражный суд Хабаровского края', 'ПАО "ДЭК", ФГАУ "Росжилкомплекс"'),
('А56-14358', 'Арбитражный суд города Санкт-Петербурга и Ленинградской области', 'ГУ Управление Пенсионного Фонда РФ, ООО "ПРОДТОРГ"'),
('СИП-184', 'Суд по интеллектуальным правам', 'Ленциг Акциенгезельшафт', 'ВИОРИКА-КОСМЕТИК Эс.А'),
('А71-2265', 'Арбитражный суд Удмуртской Республики', 'ООО "Спецавтохозяйство", ООО "Альянс"'),
('А82-3222', 'Арбитражный суд Ярославской области', 'Коржов Олег Игоревич'),
('А84-767', 'Арбитражный суд города Севастополя', 'Роговская Кристина Евгеньевна'),
('А81-651', 'Арбитражный суд Ямало-Ненецкого АО', 'ОАО "Российские железные дороги", ПАО "Государственная транспортная лизинговая компания"'),
('А81-640', 'Арбитражный суд Ямало-Ненецкого АО', 'ПАО "Ростелеком", ООО "Виват"'),
('08АП-5518', '8 арбитражный апелляционный суд', 'ПАО "Ростелеком", ООО "Виват"'),
('Ф04-5118', 'Арбитражный суд Западно-Сибирского округа', 'ПАО "Ростелеком", ООО "Виват"');

INSERT INTO documents (title, date, type, case_id) VALUES
('Решение суда 1-ой инстанции о частичном удовлетворении иска', '2023-10-04', 'Решение', 1),
('Назначение дела к судебному разбирательству', '2023-06-27', 'Назначение', 1),
('Решение суда 1-ой инстанции о признании гражданина банкротом', '2023-10-25', 'Решение', 2),
('Определение суда 1-ой инстанции о прекращении производства по заявлению/жалобе', '2023-08-21', 'Определение', 2),
('Постановление суда апелляционной инстанции оставить определние суда без изменения, жалобу без удовлетворения', '2024-10-18', 'Постановление', 2),
('Решение суда 1-ой инстанции о взыскании денежных средств и возврате госпошлины', '2025-02-18', 'Решение', 3),
('Назначение дела к судебному разбирательству', '2025-01-13', 'Назначение', 3),
('Выдача судебного приказа (ст.229.6 АПК)', '2021-03-04', 'Судебный приказ', 4),
('Определение суда 1-ой инстанции о прекращении производства по делу в связи с принятием отказа от заявленных требований', '2021-07-20', 'Определение', 5),
('Определение суда 1-ой инстанции об оставлении искового заявления без рассмотрения', '2021-09-29', 'Определение', 6),
('Определение суда 1-ой инстанции о принятии к производству заявления о признании должника банкротом', '2025-02-07', 'Определение', 8),
('Решение суда 1-ой инстанции об отказе в иске', '2020-06-21', 'Решение', 9),
('Решение суда 1-ой инстанции об удовлетворении ходатайства', '2020-05-20', 'Решение', 10),
('Постановление суда апелляционной инстанции оставить решение суда без изменения', '2020-08-27', 'Постановление', 11),
('Постановление суда кассационной инстанции оставить постановление апелляционной инстанции без изменения', '2020-12-25', 'Постановление', 12);

INSERT INTO entities (name, type, document_id) VALUES
('Интеллектуальные права', 'Термин', 1),
('Банкротство', 'Термин', 2),
('Госпошлина', 'Термин', 3),
('Судебный приказ', 'Документ', 4),
('Интеллектуальные права', 'Термин', 5),
('Банкротство', 'Термин', 7),
('Банкротство', 'Термин', 8),
('Ходатайство', 'Документ', 10);


SELECT * FROM documents WHERE type = 'Постановление';
SELECT * FROM cases WHERE number = 'СИП-184';
SELECT number FROM cases WHERE participants LIKE '%ПАО \"Ростелеком\"%';

SELECT d.title, e.name 
FROM documents d 
JOIN entities e ON d.id = e.document_id;

SELECT e.name AS entity_name, d.title AS document_title
FROM entities e
JOIN documents d ON e.document_id = d.id
WHERE d.id IN (SELECT id FROM cases WHERE court = 'Арбитражный суд города Севастополя');

SELECT c.number, COUNT(d.id) AS document_count
FROM cases c
LEFT JOIN documents d ON c.id = d.case_id
GROUP BY c.number;

SELECT c.number, c.court, d.title, d.date
FROM cases c
LEFT JOIN documents d ON c.id = d.case_id
ORDER BY d.date ASC;

SELECT c.number, c.court, d.title, d.date
FROM cases c
LEFT JOIN documents d ON c.id = d.case_id
WHERE d.date >= '2023-10-01'
ORDER BY d.date DESC;


CREATE INDEX IF NOT EXISTS idx_documents_title
ON documents USING gin(to_tsvector('russian', title));

CREATE INDEX IF NOT EXISTS idx_cases_participants
ON cases USING gin(to_tsvector('russian', participants));

SELECT * FROM documents WHERE to_tsvector('russian', title) @@ to_tsquery('банкрот');
SELECT * FROM documents WHERE to_tsvector('russian', title) @@ to_tsquery('производство');
SELECT * FROM cases WHERE to_tsvector('russian', participants) @@ to_tsquery('ООО');

SELECT c.* FROM cases c
JOIN documents d ON d.case_id = c.id
WHERE to_tsvector('russian', d.title) @@ to_tsquery('решение');

SELECT e.* FROM entities e
JOIN documents d ON e.document_id = d.id
WHERE to_tsvector('russian', d.title) @@ to_tsquery('банкрот');

SELECT c.* FROM cases c
JOIN documents d ON c.id = d.case_id
WHERE to_tsvector('russian', d.title) @@ to_tsquery('судебный');

SELECT * FROM documents
WHERE to_tsvector('russian', title) @@ to_tsquery('постановление | определение');