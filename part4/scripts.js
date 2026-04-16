// Run the correct setup functions after the HTML page is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  updateLoginLinkVisibility();
  setupLoginForm();
  setupIndexPage();
  setupPlacePage();
  setupAddReviewPage();
});

// Show or hide the login link depending on whether a token exists
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

// Attach login form submit behavior if the current page contains the login form
function setupLoginForm() {
  const loginForm = document.getElementById('login-form');

  if (!loginForm) {
    return;
  }

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('error-message');

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (errorMessage) {
      errorMessage.textContent = '';
    }

    try {
      await loginUser(email, password);
    } catch (error) {
      if (errorMessage) {
        errorMessage.textContent = error.message;
      } else {
        alert(error.message);
      }
    }
  });
}

// Send login request to the backend API and store the returned token in cookies
async function loginUser(email, password) {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) {
    let errorText = 'Login failed';

    try {
      const errorData = await response.json();
      errorText = errorData.error || errorData.message || 'Invalid email or password';
    } catch (e) {
      errorText = `Login failed: ${response.statusText}`;
    }

    throw new Error(errorText);
  }

  const data = await response.json();
  document.cookie = `token=${data.access_token}; path=/`;
  window.location.href = 'index.html';
}

// Initialize the home page by loading places and connecting the filters
function setupIndexPage() {
  const placesList = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');
  const cityFilter = document.getElementById('city-filter');

  if (!placesList || !priceFilter || !cityFilter) {
    return;
  }

  populateFilters();
  fetchPlaces(getCookie('token'));

  priceFilter.addEventListener('change', () => {
    filterPlaces();
  });

  cityFilter.addEventListener('change', () => {
    filterPlaces();
  });
}

// Fill the price and city filters with default options
function populateFilters() {
  const priceFilter = document.getElementById('price-filter');
  const cityFilter = document.getElementById('city-filter');

  if (priceFilter) {
    priceFilter.innerHTML = `
      <option value="all" selected>All Prices</option>
      <option value="10">Up to $10</option>
      <option value="50">Up to $50</option>
      <option value="100">Up to $100</option>
    `;
  }

  if (cityFilter) {
    cityFilter.innerHTML = `
      <option value="all" selected>All Cities</option>
      <option value="Riyadh">Riyadh</option>
      <option value="Jeddah">Jeddah</option>
      <option value="Yanbu">Yanbu</option>
    `;
  }
}

// Fetch the list of places from the backend API
async function fetchPlaces(token) {
  const headers = {};

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch('/api/v1/places/', {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error('Failed to fetch places');
    }

    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('Error fetching places:', error);

    const placesList = document.getElementById('places-list');
    if (placesList) {
      placesList.innerHTML = '<h2>Available Places</h2><p>Unable to load places at the moment.</p>';
    }
  }
}

// Return an image path based on the place title
function getPlaceImage(place) {
  const title = (place.title || place.name || '').toLowerCase();

  if (title === 'cozy apartment') {
    return 'images/cozy_apartment.png';
  }

  if (title === 'modern studio') {
    return 'images/modern_studio.png';
  }

  if (title === 'luxury villa') {
    return 'images/luxury_villa.png';
  }

  return 'images/logo.png';
}

// Return a city based on the place title
function getPlaceCity(place) {
  const title = (place.title || place.name || '').toLowerCase();

  if (title === 'cozy apartment') {
    return 'Yanbu';
  }

  if (title === 'modern studio') {
    return 'Jeddah';
  }

  if (title === 'luxury villa') {
    return 'Riyadh';
  }

  return 'Unknown City';
}

// Return the location string for a place
function getPlaceLocation(place) {
  return getPlaceCity(place);
}

// Return a description for the place, using API data if available
function getPlaceDescription(place) {
  if (place.description) {
    return place.description;
  }

  const title = (place.title || place.name || '').toLowerCase();

  if (title === 'cozy apartment') {
    return 'Nice and quiet';
  }

  if (title === 'modern studio') {
    return 'A modern studio in the city center';
  }

  if (title === 'luxury villa') {
    return 'A spacious villa with a pool';
  }

  return 'No description available.';
}

// Render all places as cards on the home page
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');

  if (!placesList) {
    return;
  }

  placesList.innerHTML = '<h2>Available Places</h2>';

  places.forEach((place) => {
    const placeCard = document.createElement('article');
    placeCard.className = 'place-card';

    const price = Number(place.price || place.price_by_night || 0);
    const title = place.title || place.name || 'Unnamed Place';
    const description = getPlaceDescription(place);
    const city = getPlaceCity(place);
    const location = getPlaceLocation(place);
    const imageSrc = getPlaceImage(place);

    // Store filter values as custom data attributes on each card
    placeCard.setAttribute('data-price', price);
    placeCard.setAttribute('data-city', city);

    placeCard.innerHTML = `
      <img src="${imageSrc}" alt="${title}">
      <h3>${title}</h3>
      <p><strong>Price per night:</strong> $${price}</p>
      <p><strong>Location:</strong> ${location}</p>
      <p>${description}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(placeCard);
  });

  // Apply filters after displaying the places
  filterPlaces();
}

// Filter visible place cards based on selected price and city
function filterPlaces() {
  const priceFilter = document.getElementById('price-filter');
  const cityFilter = document.getElementById('city-filter');
  const placeCards = document.querySelectorAll('.place-card');

  if (!priceFilter || !cityFilter) {
    return;
  }

  const selectedPrice = priceFilter.value;
  const selectedCity = cityFilter.value;

  placeCards.forEach((card) => {
    const placePrice = Number(card.getAttribute('data-price'));
    const placeCity = card.getAttribute('data-city');

    const matchesPrice =
      selectedPrice === 'all' || placePrice <= Number(selectedPrice);

    const matchesCity =
      selectedCity === 'all' || placeCity === selectedCity;

    if (matchesPrice && matchesCity) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

// Initialize the place details page
function setupPlacePage() {
  const placeDetailsSection = document.getElementById('place-details');
  const reviewsSection = document.getElementById('reviews');
  const addReviewSection = document.getElementById('add-review');

  if (!placeDetailsSection || !reviewsSection || !addReviewSection) {
    return;
  }

  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    placeDetailsSection.innerHTML = '<h1>Place Details</h1><p>Place ID not found in URL.</p>';
    reviewsSection.innerHTML = '<h2>Reviews</h2><p>No reviews available.</p>';
    addReviewSection.style.display = 'none';
    return;
  }

  // Show add review button only if the user is logged in
  if (token) {
    addReviewSection.innerHTML = `
      <a href="add_review.html?id=${placeId}" class="details-button">Add Review</a>
    `;
  } else {
    addReviewSection.innerHTML = '';
  }

  // Load place details and reviews
  fetchPlaceDetails(token, placeId);
  fetchPlaceReviews(placeId);
}

// Extract the place ID from the URL query string
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// Fetch a single place's details from the backend
async function fetchPlaceDetails(token, placeId) {
  const headers = {};

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }

    const place = await response.json();
    displayPlaceDetails(place);
  } catch (error) {
    console.error('Error fetching place details:', error);

    const placeDetailsSection = document.getElementById('place-details');
    if (placeDetailsSection) {
      placeDetailsSection.innerHTML = '<h1>Place Details</h1><p>Unable to load place details.</p>';
    }
  }
}

// Display one place with its main information, description, and amenities
function displayPlaceDetails(place) {
  const placeDetailsSection = document.getElementById('place-details');

  if (!placeDetailsSection) {
    return;
  }

  const title = place.title || place.name || 'Unnamed Place';
  const description = place.description || 'No description available.';
  const price = place.price || place.price_by_night || 0;
  const imageSrc = getPlaceImage(place);
  const location = getPlaceLocation(place);

  let ownerName = 'Owner information not available';
  if (place.owner) {
    ownerName = `${place.owner.first_name} ${place.owner.last_name}`;
  }

  let amenitiesHTML = '<li>No amenities available.</li>';
  if (place.amenities && place.amenities.length > 0) {
    amenitiesHTML = place.amenities.map((amenity) => `<li>${amenity.name}</li>`).join('');
  }

  placeDetailsSection.innerHTML = `
    <img src="${imageSrc}" alt="${title}">
    <h1>${title}</h1>

    <div class="place-info">
      <p><strong>Host:</strong> ${ownerName}</p>
      <p><strong>Price per night:</strong> $${price}</p>
      <p><strong>Location:</strong> ${location}</p>
    </div>

    <div class="place-info">
      <h2>Description</h2>
      <p>${description}</p>
    </div>

    <div class="place-info">
      <h2>Amenities</h2>
      <ul>
        ${amenitiesHTML}
      </ul>
    </div>
  `;
}

// Fetch reviews for the selected place
async function fetchPlaceReviews(placeId) {
  try {
    const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
      method: 'GET'
    });

    if (!response.ok) {
      throw new Error('Failed to fetch reviews');
    }

    const reviews = await response.json();
    displayPlaceReviews(reviews);
  } catch (error) {
    console.error('Error fetching reviews:', error);

    const reviewsSection = document.getElementById('reviews');
    if (reviewsSection) {
      reviewsSection.innerHTML = '<h2>Reviews</h2><p>Unable to load reviews.</p>';
    }
  }
}

// Display all reviews for the current place
function displayPlaceReviews(reviews) {
  const reviewsSection = document.getElementById('reviews');

  if (!reviewsSection) {
    return;
  }

  reviewsSection.innerHTML = '<h2>Reviews</h2>';

  if (!reviews || reviews.length === 0) {
    reviewsSection.innerHTML += '<p>No reviews yet.</p>';
    return;
  }

  reviews.forEach((review) => {
    const reviewCard = document.createElement('article');
    reviewCard.className = 'review-card';

    const reviewText = review.text || 'No review text available.';
    const rating = review.rating || 'No rating';
    const reviewerName = review.user
      ? `${review.user.first_name} ${review.user.last_name}`
      : 'Guest';

    reviewCard.innerHTML = `
      <h3>Review by ${reviewerName}</h3>
      <p class="review-comment">${reviewText}</p>
      <p><strong>Rating:</strong> ${rating}/5</p>
    `;

    reviewsSection.appendChild(reviewCard);
  });
}

// Initialize the add review page and handle review submission
function setupAddReviewPage() {
  const reviewForm = document.getElementById('add-review-form');
  const reviewMessage = document.getElementById('review-message');
  const placeIdDisplay = document.getElementById('place-id-display');

  if (!reviewForm || !reviewMessage || !placeIdDisplay) {
    return;
  }

  const token = checkReviewAuthentication();
  if (!token) {
    return;
  }

  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    reviewMessage.textContent = 'Place ID not found.';
    reviewMessage.className = 'error';
    reviewForm.style.display = 'none';
    return;
  }

  // Show the place ID on the page
  placeIdDisplay.textContent = placeId;

  // Submit review form
  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const reviewText = document.getElementById('review').value.trim();
    const rating = document.getElementById('rating').value;

    reviewMessage.textContent = '';
    reviewMessage.className = '';

    try {
      await submitReview(token, placeId, reviewText, rating);
      reviewMessage.textContent = 'Review submitted successfully!';
      reviewMessage.className = 'success';
      reviewForm.reset();
    } catch (error) {
      reviewMessage.textContent = error.message;
      reviewMessage.className = 'error';
    }
  });
}

// Ensure the user is logged in before allowing review submission
function checkReviewAuthentication() {
  const token = getCookie('token');

  if (!token) {
    window.location.href = 'index.html';
    return null;
  }

  return token;
}

// Send a new review to the backend API
async function submitReview(token, placeId, reviewText, rating) {
  const response = await fetch('/api/v1/reviews/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      text: reviewText,
      rating: Number(rating),
      place_id: placeId
    })
  });

  if (!response.ok) {
    let errorText = 'Failed to submit review';

    try {
      const errorData = await response.json();
      errorText = errorData.error || errorData.message || errorText;
    } catch (e) {
      errorText = `Failed to submit review: ${response.statusText}`;
    }

    throw new Error(errorText);
  }

  return response.json();
}

// Read a cookie value by its name
function getCookie(name) {
  const cookies = document.cookie.split(';');

  for (let i = 0; i < cookies.length; i += 1) {
    const cookie = cookies[i].trim();

    if (cookie.startsWith(`${name}=`)) {
      return cookie.substring(name.length + 1);
    }
  }

  return null;
}
