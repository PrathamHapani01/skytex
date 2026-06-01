document.addEventListener("DOMContentLoaded", () => {
  const reviewsContainer = document.getElementById("reviews-container");
  if (!reviewsContainer) return;

  const reviews = [
    {
      name: "Sarah M.",
      text: "Absolutely stunning fabrics! The quality exceeded my expectations.",
      rating: 5
    },
    {
      name: "James K.",
      text: "Fast shipping and beautiful materials. Will order again!",
      rating: 5
    },
    {
      name: "Priya R.",
      text: "The swatch kit was so helpful. Made choosing easy.",
      rating: 4
    }
  ];

  reviewsContainer.innerHTML = reviews.map(review => `
    <div class="review-card">
      <div class="review-rating">${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)}</div>
      <p class="review-text">"${review.text}"</p>
      <p class="review-author">- ${review.name}</p>
    </div>
  `).join('');
});
