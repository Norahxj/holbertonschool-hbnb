USE hbnb_db;

INSERT IGNORE INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$4Pcq/d.KIykcNpGGR03BoOOrM9urFMwM0nqC6n2T78zR9dsjGrfZ6',
    TRUE
);

INSERT IGNORE INTO Amenity (id, name) VALUES
    ("66157811-19ec-4351-93cf-0ffbe1a594f7", 'WiFi'),
    ("c3ddeb7e-fbca-452a-85e2-c5a945d9bba9", 'Swimming Pool'),
    ("6ec7d3b6-7707-4e31-af81-8b25c7b582ba", 'Air Conditioning');
