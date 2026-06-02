// API Configuration - Use API_URL from config.js
const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:8000' : 'https://skytex-rutc.onrender.com';

// API Functions
async function fetchProducts(filters = {}) {
  const params = new URLSearchParams();
  if (filters.material) params.append('material', filters.material);
  if (filters.colour) params.append('colour', filters.colour);
  if (filters.price_min !== undefined) params.append('price_min', filters.price_min);
  if (filters.price_max !== undefined) params.append('price_max', filters.price_max);

  const response = await fetch(`${API_BASE}/api/products?${params}`);
  if (!response.ok) throw new Error('Failed to fetch products');
  return response.json();
}

async function fetchProduct(id) {
  const response = await fetch(`${API_BASE}/api/products/${id}`);
  if (!response.ok) throw new Error('Failed to fetch product');
  return response.json();
}

async function fetchBestsellers() {
  const response = await fetch(`${API_BASE}/api/bestsellers`);
  if (!response.ok) throw new Error('Failed to fetch bestsellers');
  return response.json();
}

async function fetchReviews() {
  const response = await fetch(`${API_BASE}/api/reviews`);
  if (!response.ok) throw new Error('Failed to fetch reviews');
  return response.json();
}

async function submitContact(contactData) {
  const response = await fetch(`${API_BASE}/api/contact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(contactData)
  });
  if (!response.ok) throw new Error('Failed to submit contact');
  return response.json();
}

// Legacy PRODUCTS array for fallback (will be removed after migration)
const PRODUCTS = [];
