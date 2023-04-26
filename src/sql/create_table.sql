CREATE TABLE USERS
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

CREATE TABLE CULTURES
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

CREATE TYPE RIPENING_T AS ENUM ('type1', 'type2');
-- someone more qualified pls fix this

CREATE TABLE VEGETABLES
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

CREATE TYPE BLOOMING_T AS ENUM ('type1', 'type2');
CREATE TYPE COLOR_GROUP_T AS ENUM ('red', 'blue');
-- someone more qualified pls fix this

CREATE TABLE FLOWERS
(
    flower_id int,
    culture_id int,
    sort_name VARCHAR(100),
    flower_height int,
    blooming BLOOMING_T,
    color_group COLOR_GROUP_T,
    color VARCHAR(100) -- possibly RGB?
);

CREATE TABLE PHLOX_PAN
(
    phlox_id int,
    form VARCHAR(100), -- enum?
    flower_diam int
);

CREATE TABLE TOMATOES
(
    tomato_id int,
    det VARCHAR(50),
    shtamb BOOLEAN,
    color VARCHAR(50), -- RGB maybe?
    cold BOOLEAN,
    hot BOOLEAN
);