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
    },
    {
      name: "Emma L.",
      text: "Beautiful linen that drapes perfectly. Highly recommend!",
      rating: 5
    },
    {
      name: "Michael T.",
      text: "Great selection and excellent customer service.",
      rating: 5
    }
  ];

  const reviewsHtml = reviews.map(review => `
    <div class="review-card">
      <div class="review-card__header">
        <div class="review-card__avatar">${review.name.charAt(0)}</div>
        <div>
          <p class="review-card__name">${review.name}</p>
          <p class="review-card__date">Verified Buyer</p>
        </div>
      </div>
      <div class="review-card__rating">${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)}</div>
      <p class="review-card__text">"${review.text}"</p>
    </div>
  `).join('');

  reviewsContainer.innerHTML = `
    <div class="reviews-carousel">
      <button class="reviews-carousel__btn reviews-carousel__btn--prev" aria-label="Previous reviews">‹</button>
      <div class="reviews-carousel__track">
        ${reviewsHtml}
      </div>
      <button class="reviews-carousel__btn reviews-carousel__btn--next" aria-label="Next reviews">›</button>
    </div>
    <div class="reviews-dots">
      ${reviews.map((_, i) => `<button class="reviews-dot ${i === 0 ? 'is-active' : ''}" data-index="${i}" aria-label="Go to review ${i + 1}"></button>`).join('')}
    </div>
  `;

  // Carousel functionality
  const track = reviewsContainer.querySelector('.reviews-carousel__track');
  const prevBtn = reviewsContainer.querySelector('.reviews-carousel__btn--prev');
  const nextBtn = reviewsContainer.querySelector('.reviews-carousel__btn--next');
  const dots = reviewsContainer.querySelectorAll('.reviews-dot');
  let currentIndex = 0;

  function updateCarousel() {
    const cardWidth = track.querySelector('.review-card').offsetWidth;
    const gap = 20; // gap from CSS
    const scrollPosition = currentIndex * (cardWidth + gap);
    track.scrollTo({ left: scrollPosition, behavior: 'smooth' });
    
    dots.forEach((dot, i) => {
      dot.classList.toggle('is-active', i === currentIndex);
    });
  }

  prevBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex--;
      updateCarousel();
    }
  });

  nextBtn.addEventListener('click', () => {
    if (currentIndex < reviews.length - 1) {
      currentIndex++;
      updateCarousel();
    }
  });

  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      currentIndex = parseInt(dot.dataset.index);
      updateCarousel();
    });
  });

  // Auto-scroll
  let autoScrollInterval = setInterval(() => {
    if (currentIndex < reviews.length - 1) {
      currentIndex++;
    } else {
      currentIndex = 0;
    }
    updateCarousel();
  }, 5000);

  // Pause auto-scroll on hover
  track.addEventListener('mouseenter', () => clearInterval(autoScrollInterval));
  track.addEventListener('mouseleave', () => {
    autoScrollInterval = setInterval(() => {
      if (currentIndex < reviews.length - 1) {
        currentIndex++;
      } else {
        currentIndex = 0;
      }
      updateCarousel();
    }, 5000);
  });
});
