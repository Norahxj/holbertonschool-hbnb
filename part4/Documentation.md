# HBnB Project Documentation

## Overview

HBnB is a full-stack web application inspired by online rental and booking platforms.  
The project combines a Flask-based REST API with a dynamic front-end built using HTML, CSS, and JavaScript.

The application supports:

- user authentication with JWT
- listing and filtering places
- viewing place details
- viewing and submitting reviews
- managing amenities
- role-based permissions for admins and regular users

This project was developed in multiple stages, with the final result integrating both back-end and front-end functionality into a complete user experience.

---

## Technologies Used

### Back-end
- Python 3
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- Flask-Bcrypt
- Flask-CORS
- SQLAlchemy
- SQLite

### Front-end
- HTML5
- CSS3
- JavaScript (ES6)
- Fetch API

---

## Project Structure

```text
holbertonschool-hbnb/
├── part3/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── places.py
│   │   │   ├── reviews.py
│   │   │   └── amenities.py
│   │   ├── services/
│   │   ├── models/
│   │   └── __init__.py
│   ├── instance/
│   │   └── development.db
│   ├── run.py
│   └── config.py
│
└── part4/
    ├── index.html
    ├── login.html
    ├── place.html
    ├── add_review.html
    ├── styles.css
    ├── scripts.js
    └── images/
Main Features
1. Authentication

Users can log in using email and password.

When login succeeds:

the API returns a JWT token
the token is stored in cookies
the user is redirected to index.html

When login fails:

an error message is displayed
2. Place Listing

The home page dynamically displays all available places.

Each place card includes:

image
title
price
location
description
details button
3. Filtering

The filtering system was improved during development.

Initial behavior

At first, the page only allowed filtering by price.

Final behavior

The page now supports:

filtering by price
filtering by city
City mapping used in the project
Cozy Apartment → Yanbu
Modern Studio → Jeddah
Luxury Villa → Riyadh
4. Place Details

Each place has a dedicated details page accessed through:

place.html?id=<place_id>

The page displays:

place image
title
host name
price per night
city/location
description
amenities
reviews
5. Reviews

Authenticated users can submit reviews through add_review.html.

Each review contains:

review text
rating
place ID

The system enforces important business rules:

a user cannot review their own place
a user cannot review the same place twice
a non-authenticated user is redirected to index.html
6. Amenities

Amenities were successfully created and managed through the admin account.

Examples added in the project:

WiFi
Swimming Pool
Air Conditioning

Amenities were then attached to places, for example:

Luxury Villa → Swimming Pool
Modern Studio → WiFi + Air Conditioning
7. Images

At first, place images were not displayed because the image paths and mapping were incomplete.

This was fixed by:

adding image files to part4/images
mapping each place title to its corresponding image file in scripts.js

Examples:

cozy_apartment.png
modern_studio.png
luxury_villa.png
Important Fixes and Improvements
1. Place ID display removed from visible UI

Initially, the place ID appeared in visible areas of the website.
This was later improved so that only user-friendly information is shown, such as:

place name
description
location

This made the interface cleaner and more professional.

2. Reviewer name fix

Originally, the review section displayed a generic title:

Guest Review

instead of showing the actual reviewer's name.

Before

The API returned only:

id
text
rating
user_id
place_id

And the front-end used:

reviewCard.innerHTML = `
  <h3>Guest Review</h3>
  <p class="review-comment">${reviewText}</p>
  <p><strong>Rating:</strong> ${rating}/5</p>
`;
After

The back-end was updated so that reviews also return:

"user": {
  "id": "...",
  "first_name": "...",
  "last_name": "..."
}

Then the front-end was updated to show:

const reviewerName = review.user
  ? `${review.user.first_name} ${review.user.last_name}`
  : 'Guest';

reviewCard.innerHTML = `
  <h3>Review by ${reviewerName}</h3>
  <p class="review-comment">${reviewText}</p>
  <p><strong>Rating:</strong> ${rating}/5</p>
`;
Result

The website now displays the actual name of the reviewer instead of the generic label.

3. Login visibility fix

Originally, after a successful login, the login button disappeared only on index.html, but it still appeared on other pages such as:

place.html
add_review.html
Cause

The script originally checked only the login element on the home page.

Before

The login element did not consistently use the same ID across pages, and the authentication visibility logic only affected the index page.

After

The login button/link was standardized using:

id="login-link"

and the JavaScript was updated to run on all pages:

function updateLoginLinkVisibility() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!loginLink) {
    return;
  }

  if (token) {
    loginLink.style.display = 'none';
  } else {
    loginLink.style.display = 'inline-block';
  }
}
Result

The login button now hides correctly across all pages once the user is authenticated.

4. Filter improvement

Initially, filtering was limited to prices only.

Before

The website displayed a price-only filter.

After

A second filter was added for cities:

Riyadh
Jeddah
Yanbu

Both filters now work together, so a place must match:

the selected price
the selected city
5. Review form improvement

Initially, the review form had only:

a text box

There was no rating dropdown, and submitting the form caused incorrect behavior, including redirecting to a blank page.

Before
no rating selection
incorrect submission behavior
blank page after submit
After

The form was redesigned to include:

review text
rating dropdown
proper place ID from URL
success/error message handling

The review submission flow was fixed so that:

reviews submit correctly to the API
unauthenticated users are redirected to index.html
after successful submission, the user is redirected properly instead of landing on a blank page
6. New user registration and review testing

A new regular user was successfully created as an admin.

This allowed proper testing of the review system, because:

a user cannot review a place they own
a user can review places owned by others
a user cannot review the same place twice

This confirmed that both authentication and business rules work correctly.

Running the Project

To open the website successfully:

Step 1

Move into part3:

cd part3
Step 2

Install required dependencies:

pip3 install -r requirements.txt
python3 -m pip install flask flask-sqlalchemy flask-jwt-extended flask-bcrypt flask-cors python-dotenv
Step 3

Run the application:

python3 run.py
Step 4

Open the website using:

https://web-80-92-27.cod-eu-west-3.hbtn.io/index.html
Step 5

Log in as admin:

Email: admin@hbnb.io
Password: admin1234
HTTP Status Codes Used
200 OK

Returned when a request succeeds.

Examples:

fetching places
fetching reviews
fetching amenities
successful updates
201 Created

Returned when a resource is successfully created.

Examples:

user creation
place creation
review creation
amenity creation
400 Bad Request

Returned when the request violates validation or business rules.

Examples:

invalid input
duplicate review
reviewing your own place
401 Unauthorized

Returned when authentication is missing or invalid.

Example:

missing Authorization header
403 Forbidden

Returned when the user is authenticated but not allowed to perform the action.

Examples:

non-admin trying to create a user
non-admin trying to create or update an amenity
unauthorized update action
404 Not Found

Returned when a requested resource does not exist.

Examples:

place not found
review not found
amenity not found
user not found
Final Notes

This project demonstrates:

REST API development
JWT authentication
role-based access control
dynamic front-end rendering
filtering and conditional UI behavior
full client/server interaction

It also shows a clear improvement process from initial functionality to a more polished and user-friendly final product.
