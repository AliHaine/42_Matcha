-- matcha default
SELECT users.*,
    COUNT(DISTINCT common.interest_id) AS common_interests,
    ST_Distance(
        user_city.geom::geography,
        my_city.geom::geography
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
    AND users.city_id = my_city.id
    AND (
        (
            users.searching = (
                SELECT searching
                FROM users
                WHERE id = %(user_id)s
            )
        )::int + (
            users.commitment = (
                SELECT commitment
                FROM users
                WHERE id = %(user_id)s
            )
        )::int + (
            users.frequency = (
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
        OR (
            %(hetero)s = FALSE
            AND users.gender = %(gender)s
        )
    )
    AND (
        (
            users.hetero = TRUE
            AND %(gender)s != users.gender
        )
        OR (
            users.hetero = FALSE
            AND %(gender)s = users.gender
        )
    )
GROUP BY users.id,
    user_city.geom,
    my_city.geom
ORDER BY RANDOM()
LIMIT 500;