let index = 0;
const slides = document.querySelectorAll(".slide");
const totalSlides = slides.length;

function moveSlide(step) {
    index += step;
    if (index >= totalSlides) index = 0;
    if (index < 0) index = totalSlides - 1;
    updateSlider();
}

function updateSlider() {
    document.getElementById("slider").style.transform = `translateX(${-index * 100}%)`;
}

// Auto-slide every 3 seconds
setInterval(() => {
    moveSlide(1);
}, 3000);

// Event JS
let currentIndexes = {}; // Stores index for each carousel separately

function showSlide(eventIndex) {
    const carousels = document.querySelectorAll(".carousel-slider .carousel-track");
    if (!currentIndexes[eventIndex]) currentIndexes[eventIndex] = 0;

    const totalSlides = carousels[eventIndex].children.length;

    if (currentIndexes[eventIndex] >= totalSlides) {
        currentIndexes[eventIndex] = 0; // Loop back to first image
    } else if (currentIndexes[eventIndex] < 0) {
        currentIndexes[eventIndex] = totalSlides - 1; // Loop to last image
    }

    const offset = -currentIndexes[eventIndex] * 500; // Adjust width according to CSS
    carousels[eventIndex].style.transform = `translateX(${offset}px)`;
}

function nextSlide(eventIndex) {
    currentIndexes[eventIndex]++;
    showSlide(eventIndex);
}

function prevSlide(eventIndex) {
    currentIndexes[eventIndex]--;
    showSlide(eventIndex);
}

// Initialize first slide position for each carousel
document.querySelectorAll(".carousel-slider .carousel-track").forEach((_, i) => showSlide(i));

// Add event listeners for navigation buttons
document.querySelectorAll(".carousel-slider").forEach((carousel, index) => {
    const prevBtn = carousel.querySelector(".prev");
    const nextBtn = carousel.querySelector(".next");

    if (prevBtn) {
        prevBtn.addEventListener("click", () => prevSlide(index));
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => nextSlide(index));
    }
});

// Gallery page
let slideIndex = 0;
let slideInterval;

document.addEventListener("DOMContentLoaded", function () {
  showSlides();
  autoSlides(); // Start auto-slideshow on page load
});

// Next/previous controls
function plusSlides(n) {
  clearInterval(slideInterval); // Stop auto-slide when manually clicked
  slideIndex += n;
  showSlides();
  autoSlides(); // Restart auto-slide after manual control
}

// Thumbnail image controls
function currentSlide(n) {
  clearInterval(slideInterval);
  slideIndex = n - 1;
  showSlides();
  autoSlides();
}

function showSlides() {
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");

  if (slideIndex >= slides.length) { slideIndex = 0; }
  if (slideIndex < 0) { slideIndex = slides.length - 1; }

  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (let i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  slides[slideIndex].style.display = "block";
  dots[slideIndex].className += " active";
}

// Automatic slideshow function
function autoSlides() {
  slideInterval = setInterval(() => {
    slideIndex++;
    showSlides();
  }, 2000); // Change slide every 2 seconds
}

// NEWS PAGE
document.querySelectorAll('.filter-btn').forEach(button => {
    button.addEventListener('click', function() {
        const filter = this.getAttribute('data-filter');
        document.querySelectorAll('.news-item').forEach(item => {
            item.style.display = filter === 'all' || item.classList.contains(filter) ? 'block' : 'none';
        });
    });
});

document.getElementById('news-search').addEventListener('input', function() {
    const searchValue = this.value.toLowerCase();
    document.querySelectorAll('.news-item').forEach(item => {
        const text = item.innerText.toLowerCase();
        item.style.display = text.includes(searchValue) ? 'block' : 'none';
    });
});

document.querySelectorAll('.read-more').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const newsItem = this.closest('.news-item');
        document.getElementById('popup-title').textContent = newsItem.querySelector('h2').textContent;
        document.getElementById('popup-content').textContent = newsItem.getAttribute('data-content');
        document.getElementById('news-popup').style.display = 'block';
    });
});

function closePopup() {
    document.getElementById('news-popup').style.display = 'none';
}

// captcha code
function generateCaptcha() {
    let captcha = Math.random().toString(36).substring(2, 8).toUpperCase();
    document.getElementById("captchaCode").innerText = captcha;
}

function validateCaptcha() {
    let enteredCaptcha = document.getElementById("captchaInput").value;
    let generatedCaptcha = document.getElementById("captchaCode").innerText;
    
    if (enteredCaptcha !== generatedCaptcha) {
        alert("CAPTCHA verification failed! Please try again.");
        generateCaptcha();
        return false;
    }
    return true;
}

generateCaptcha();