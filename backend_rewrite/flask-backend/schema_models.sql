DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS cities CASCADE;
DROP TABLE IF EXISTS interests CASCADE;
DROP TABLE IF EXISTS users_interests CASCADE;
DROP TABLE IF EXISTS user_views CASCADE;

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    cityname VARCHAR(250) NOT NULL,
    citycode INT NOT NULL,
    departementname VARCHAR(250) NOT NULL,
    departementcode INT NOT NULL,
    regionname VARCHAR(250) NOT NULL,
    regioncode INT NOT NULL,
    centerlon FLOAT NOT NULL,
    centerlat FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cityname_not_empty CHECK (cityname <> ''),
    CONSTRAINT departementname_not_empty CHECK (departementname <> ''),
    CONSTRAINT regionname_not_empty CHECK (regionname <> '')
);

CREATE TABLE interests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    category VARCHAR(250),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT interestname_not_empty CHECK (name <> '')
);

CREATE TABLE users (
    -- first step register
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(1) NOT NULL,
    -- second step register
    city_id INT,  -- Rendre la ville obligatoire
    searching VARCHAR(13),
    commitment VARCHAR(11),
    frequency VARCHAR(13),
    weight VARCHAR(7),
    size VARCHAR(8),
    shape VARCHAR(7),
    smoking BOOLEAN,
    alcohol VARCHAR(13),
    diet VARCHAR(16),
    -- third step register
    description VARCHAR(500),
    -- other informations
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- unclassed informations
    status VARCHAR(13) DEFAULT 'Disconnected',
    pictures_number INT DEFAULT 0,
    registration_complete BOOLEAN DEFAULT FALSE,

    -- constraint setup
    CONSTRAINT firstname_not_empty CHECK (firstname <> ''),
    CONSTRAINT firstname_invalid CHECK (firstname ~ '^[a-zA-Z\s-]+$'),
    CONSTRAINT lastname_not_empty CHECK (lastname <> ''),
    CONSTRAINT lastname_invalid CHECK (lastname ~ '^[a-zA-Z\s-]+$'),
    CONSTRAINT email_not_empty CHECK (email <> ''),
    CONSTRAINT email_unique UNIQUE (email),
    CONSTRAINT email_invalid CHECK (email ~ '^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+$'),
    CONSTRAINT password_not_empty CHECK (password <> ''),
    CONSTRAINT age_positive CHECK (age > 15 AND age < 80),
    CONSTRAINT gender_check CHECK (gender IN ('M', 'F')),
    CONSTRAINT fk_city_id FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE SET NULL,  -- Clé étrangère activée
    CONSTRAINT searching_invalid CHECK (searching IN ('Friends', 'Love', 'Just talking')),
    CONSTRAINT commitment_invalid CHECK (commitment IN ('Short term', 'Long term', 'Undecided')),
    CONSTRAINT frequency_invalid CHECK (frequency IN ('Daily', 'Weekly', 'Occasionally')),
    CONSTRAINT weight_invalid CHECK (weight IN ('< 50', '51-60', '61-70', '71-80', '81-90', '91-100', '> 100')),
    CONSTRAINT size_invalid CHECK (size IN ('< 150', '151-160', '161-170', '171-180', '181-190', '191-200', '> 200')),
    CONSTRAINT shape_invalid CHECK (shape IN ('Skinny', 'Normal', 'Sporty', 'Fat')),
    CONSTRAINT smoking_invalid CHECK (smoking IN (TRUE, FALSE)),
    CONSTRAINT alcohol_invalid CHECK (alcohol IN ('Never', 'Occasionally', 'Every week', 'Every day')),
    CONSTRAINT diet_invalid CHECK (diet IN ('Omnivor', 'Vegetarian', 'Vegan', 'Rich in protein')),
    CONSTRAINT description_invalid CHECK (description ~ '^[a-zA-Z\s-]+$'),
    CONSTRAINT status_invalid CHECK (status IN ('Connected', 'Disconnected'))
);

CREATE TABLE users_interests (
    id SERIAL PRIMARY KEY,
    user_id INT,
    interest_id INT,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_interest_id FOREIGN KEY (interest_id) REFERENCES interests(id) ON DELETE CASCADE
);

CREATE TABLE user_views(
    id SERIAL PRIMARY KEY,
    viewer_id INT,
    viewed_id INT,
    liked BOOLEAN DEFAULT FALSE,
    blocked BOOLEAN DEFAULT FALSE,
    report BOOLEAN DEFAULT FALSE,
    last_view TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_viewer_id FOREIGN KEY (viewer_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_viewed_id FOREIGN KEY (viewed_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE waiting_notifications(
    id SERIAL PRIMARY KEY,
    user_id INT,
    message VARCHAR(250),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)