document.addEventListener('DOMContentLoaded', () => {
  updateLoginLinkVisibility();
  setupLoginForm();
  setupIndexPage();
});

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

function setupLoginForm() {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
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
}

async function loginUser(email, password) {
  const API_URL = '/api/v1/auth/login';

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    let errorText = 'Login failed';

    try {
      const errorData = await response.json();
      errorText = errorData.error || errorData.message || 'Invalid email or password';
    } catch (e) {
      errorText = `Login failed: ${response.statusText}`;
    }

    throw new Error(errorText);
  }
}

function setupIndexPage() {
  const placesList = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');

  if (!placesList || !priceFilter) {
    return;
  }

  populatePriceFilter();
  fetchPlaces(getCookie('token'));

  priceFilter.addEventListener('change', () => {
    filterPlacesByPrice();
  });
}

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

function populatePriceFilter() {
  const priceFilter = document.getElementById('price-filter');

  if (!priceFilter) {
    return;
  }

  priceFilter.innerHTML = `
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
    <option value="all" selected>All</option>
  `;
}

async function fetchPlaces(token) {
  const API_URL = '/api/v1/places/';
  const headers = {};

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(API_URL, {
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
    const description = place.description || 'No description available.';
    const title = place.title || place.name || 'Unnamed Place';
    const location = place.location || 'Location not available';

    placeCard.setAttribute('data-price', price);

    placeCard.innerHTML = `
      <h3>${title}</h3>
      <p><strong>Price per night:</strong> $${price}</p>
      <p><strong>Location:</strong> ${location}</p>
      <p>${description}</p>
      <a href="place.html" class="details-button">View Details</a>
    `;

    placesList.appendChild(placeCard);
  });

  filterPlacesByPrice();
}

function filterPlacesByPrice() {
  const priceFilter = document.getElementById('price-filter');
  const placeCards = document.querySelectorAll('.place-card');

  if (!priceFilter) {
    return;
  }

  const selectedValue = priceFilter.value;

  placeCards.forEach((card) => {
    const placePrice = Number(card.getAttribute('data-price'));

    if (selectedValue === 'all' || placePrice <= Number(selectedValue)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}
