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
WHERE culture_id = 1;

INSERT INTO cultures(culture_id, culture_name, culture_table_name, is_vegetable, is_annual, air_temp, min_air_temp)
VALUES (1, 'Томат', 'temp_tomato_table', True, True, 6.0, 0.0);

SELECT * FROM weather
WHERE weather."City" = 'Брест';

DELETE FROM weather
WHERE RIGHT(weather."Date", 3) = 'csv';