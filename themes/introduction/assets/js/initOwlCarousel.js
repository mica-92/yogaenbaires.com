$(document).ready(function(){
  $(".owl-carousel").owlCarousel({
    loop: true,            // Infinite looping
    margin: 20,            // Space between items
    nav: false,            // ← Disable navigation arrows
    dots: true,            // Keep pagination dots
    autoplay: true,        // Auto-play (optional)
    responsive: {          // Responsive settings
      0: { items: 1 },
      768: { items: 1 },
      1024: { items: 1 }
    }
  });
});