-- matcha default
SELECT users.*,
    COUNT(DISTINCT common.interest_id) AS common_interests,
    (
        round(
            (
                ST_Distance(
                    user_city.geom::geography,
                    my_city.geom::geography
                )::numeric / 1000
            ),
            -1
        )
    ) AS distance
FROM users
    JOIN cities user_city ON users.city_id = user_city.id
    JOIN cities my_city ON my_city.id = %(city_id)s
    LEFT JOIN users_interests other ON other.user_id = users.id
    LEFT JOIN users_interests common ON common.interest_id = other.interest_id
    AND common.user_id = %(user_id)s
WHERE users.id != %(user_id)s
    AND users.registration_complete = TRUE
    AND users.id NOT IN (
        SELECT viewed_id
        FROM user_views
        WHERE viewer_id = %(user_id)s
            AND liked = TRUE
    )
    AND users.age BETWEEN %(age_min)s AND %(age_max)s
    AND (
        SELECT COUNT(*)
        FROM users_interests ui
        WHERE ui.user_id = users.id
            AND ui.interest_id IN (
                SELECT interest_id
                FROM users_interests
                WHERE user_id = %(user_id)s
            )
    ) >= 1
    AND (
        (
            users.searching =(
                SELECT searching
                FROM users
                WHERE id = %(user_id)s
            )
        )::int +(
            users.commitment =(
                SELECT commitment
                FROM users
                WHERE id = %(user_id)s
            )
        )::int +(
            users.frequency =(
                SELECT frequency
                FROM users
                WHERE id = %(user_id)s
            )
        )::int
    ) >= 2
    AND (
        (
            %(hetero)s = TRUE
            AND users.gender != %(gender)s
        )
        OR (%(hetero)s = FALSE)
    )
    AND (
        (
            users.hetero = TRUE
            AND %(gender)s != users.gender
        )
        OR (users.hetero = FALSE)
    )
GROUP BY users.id,
    user_city.geom,
    my_city.geom
ORDER BY RANDOM()
LIMIT 500;


-- get user interests
SELECT interests.*
FROM interests
    INNER JOIN users_interests ui ON interests.id = ui.interest_id
WHERE ui.user_id = %(user_id)s;


-- get chat messages ASC
SELECT *
FROM messages
WHERE (sender_id = %(user_id_1)s AND receiver_id = %(user_id_2)s) OR (sender_id = %(user_id_2)s AND receiver_id = %(user_id_1)s)
ORDER BY created_at ASC
LIMIT %(nb_messages)s;

-- get chat messages DESC
SELECT *
FROM messages
WHERE (sender_id = %(user_id_1)s AND receiver_id = %(user_id_2)s) OR (sender_id = %(user_id_2)s AND receiver_id = %(user_id_1)s)
ORDER BY created_at DESC
LIMIT %(nb_messages)s;

-- check match
SELECT 1 AS match FROM user_views uv1
JOIN user_views uv2
  ON uv1.viewer_id = uv2.viewed_id
 AND uv1.viewed_id = uv2.viewer_id
WHERE uv1.viewer_id = %(user_id_1)s
  AND uv1.viewed_id = %(user_id_2)s
  AND uv1.liked = TRUE
  AND uv2.liked = TRUE
LIMIT 1;

-- get users
SELECT u.*,
        COUNT(ui2.interest_id) AS common_interests,
        (round((ST_Distance(
        user_city.geom::geography,
        my_city.geom::geography
    )::numeric / 1000), -1)) AS distance
FROM users u
    LEFT JOIN cities user_city ON user_city.id = u.city_id
    LEFT JOIN cities my_city ON my_city.id = %(city_id)s
    LEFT JOIN users_interests ui1 ON ui1.user_id = %(user_id)s
    LEFT JOIN users_interests ui2 ON ui2.user_id = u.id AND ui1.interest_id = ui2.interest_id;

-- group by users
GROUP BY u.id, user_city.geom, my_city.geom;