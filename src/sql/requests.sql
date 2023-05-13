CREATE TYPE ripening_enum_t AS ENUM (
        'Ультраскороспелый',
        'Раннеспелый',
        'Среднеспелый',
        'Позднеспелый'
    );

CREATE TYPE determinance_enum_t AS ENUM (
        'Индетерминантный',
        'Детерминантный',
        'Супердетерминантный'
    );

CREATE TABLE IF NOT EXISTS temp_tomato_table (
    ind INTEGER,
    tomato_name VARCHAR(256),
    hybridity BOOLEAN,
    ripening ripening_enum_t,
    ripening_time VARCHAR(256),
    determinance determinance_enum_t,
    height VARCHAR(256),
    weight VARCHAR(256)
);

DROP TABLE IF EXISTS weather;

DELETE FROM cultures
WHERE culture_id > 0;

INSERT INTO cultures(culture_id, culture_name, culture_table_name, is_vegetable, is_annual, air_temp, min_air_temp)
VALUES (1, 'Томат', 'temp_tomato_table', True, True, 6.0, 0.0);

SELECT * FROM weather
WHERE weather."City" = 'Брест';

DELETE FROM weather
WHERE RIGHT(weather."Date", 3) = 'csv';


INSERT INTO cultures(culture_id, culture_name, culture_table_name, is_vegetable, is_annual, air_temp, min_air_temp)
VALUES (1, 'Томат', 'temp_tomato_table', True, True, 6.0, 0.0),
       (2, 'Кабачок', 'temp_kabachok_table', True, True, 8.0, 5.0),
       (3, 'Баклажан', 'temp_baklazhan_table', True, True, 8.0, 5.0),
       (4, 'Дыня', 'temp_dynya_table', True, True, 13.0, 8.0),
       (5, 'Арбуз', 'temp_arbuz_table', True, True, 13.0, 8.0),
       (6, 'Перец', 'temp_perets_table', True, True, 7.0, 3.0);