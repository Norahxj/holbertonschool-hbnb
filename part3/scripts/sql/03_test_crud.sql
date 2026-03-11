USE hbnb_db;

SELECT * FROM User;

INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    UUID(),
    'Luxury Villa',
    'A beautiful place with ocean view',
    300.00,
    48.8566,
    2.3522,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

SELECT * FROM Place;

INSERT INTO Review (id, text, rating, user_id, place_id)
VALUES (
    UUID(),
    'Amazing experience, will come again!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    (SELECT id FROM Place WHERE title = 'Luxury Villa' LIMIT 1)
);

SELECT * FROM Review;

UPDATE Review
SET text = 'Absolutely wonderful!'
WHERE text = 'Amazing experience, will come again!';

DELETE FROM Review WHERE rating = 5;

SELECT * FROM Review;
