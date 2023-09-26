CREATE TABLE IF NOT EXISTS USERS
(
    user_id INT PRIMARY KEY,
    salt VARCHAR(50) NOT NULL,
    hash_and_salt VARCHAR(50) NOT NULL,
    dt DATE,
    plants JSONB,
    location_address VARCHAR(150)
);

-- Plant JSON looks like this:
--
-- culture_id int
-- amount int
-- date_planted DATE
--
-- idea to consider: use a special struct for plant?
-- JSON in Postgres cheat sheet
-- https://postgrespro.ru/docs/postgresql/9.5/functions-json

CREATE TABLE IF NOT EXISTS CULTURES
(
    culture_id int,
    culture_name VARCHAR(100),
    culture_table_name VARCHAR(100),
    transplant_days int,
    is_vegetable BOOLEAN,
    is_annual BOOLEAN,
    ground_temp int,
    air_temp int,
    min_air_temp int,
    zone_min int,
    zone_max int
);

CREATE TYPE IF NOT EXISTS RIPENING_T AS ENUM ('type1', 'type2');
-- someone more qualified pls fix this

CREATE TABLE IF NOT EXISTS VEGETABLES
(
    vegetable_id int, -- is it needed though?
    culture_id int,
    sort_name VARCHAR(100), -- same question
    is_hybrid BOOLEAN,
    ripening RIPENING_T,
    day_ripe_min int,
    day_ripe_max int,
    plant_height int,
    plant_weight int,
    open_ground BOOLEAN,
    fruit_length int,
    house BOOLEAN,
    no_transplantant BOOLEAN,
    greenhouse BOOLEAN
);

CREATE TYPE IF NOT EXISTS BLOOMING_T AS ENUM ('type1', 'type2');
CREATE TYPE IF NOT EXISTS COLOR_GROUP_T AS ENUM ('red', 'blue');
-- someone more qualified pls fix this

CREATE TABLE IF NOT EXISTS FLOWERS
(
    flower_id int,
    culture_id int,
    sort_name VARCHAR(100),
    flower_height int,
    blooming BLOOMING_T,
    color_group COLOR_GROUP_T,
    color VARCHAR(100) -- possibly RGB?
);

CREATE TABLE IF NOT EXISTS PHLOX_PAN
(
    phlox_id int,
    form VARCHAR(100), -- enum?
    flower_diam int
);

CREATE TABLE IF NOT EXISTS TOMATOES
(
    tomato_id int,
    det VARCHAR(50),
    shtamb BOOLEAN,
    color VARCHAR(50), -- RGB maybe?
    cold BOOLEAN,
    hot BOOLEAN
);

INSERT INTO cultures(culture_id, culture_name, culture_table_name, is_vegetable, is_annual, air_temp, min_air_temp)
VALUES (1, 'Томат', 'temp_tomato_table', True, True, 6.0, 0.0),
       (2, 'Кабачок', 'temp_kabachok_table', True, True, 8.0, 5.0),
       (3, 'Баклажан', 'temp_baklazhan_table', True, True, 8.0, 5.0),
       (4, 'Дыня', 'temp_dynya_table', True, True, 13.0, 8.0),
       (5, 'Арбуз', 'temp_arbuz_table', True, True, 13.0, 8.0),
       (6, 'Перец', 'temp_perets_table', True, True, 7.0, 3.0);

CREATE SCHEMA weather_schema;