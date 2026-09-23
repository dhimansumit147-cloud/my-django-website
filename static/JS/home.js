/* =========================================================
   SUNGREEN SOLAR
   HOME PAGE — PROFESSIONAL JAVASCRIPT
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    "use strict";


    /* =====================================================
       01. HERO CAROUSEL
       ===================================================== */

    const solarCarousel = document.getElementById("solarCarousel");

    if (solarCarousel && typeof bootstrap !== "undefined") {

        const carousel = bootstrap.Carousel.getOrCreateInstance(
            solarCarousel,
            {
                interval: 6000,
                ride: "carousel",
                pause: "hover",
                wrap: true,
                touch: true
            }
        );

        carousel.cycle();
    }


    /* =====================================================
       02. HERO SLIDE ANIMATION RESET
       ===================================================== */

    if (solarCarousel) {

        solarCarousel.addEventListener(
            "slide.bs.carousel",
            function () {

                const contents =
                    solarCarousel.querySelectorAll(
                        ".hero-content"
                    );

                contents.forEach(function (content) {

                    content.style.opacity = "0";

                    content.style.transform =
                        "translateY(45px) translateX(-20px)";

                });

            }
        );


        solarCarousel.addEventListener(
            "slid.bs.carousel",
            function (event) {

                const activeSlide =
                    event.relatedTarget;

                if (!activeSlide) {
                    return;
                }

                const content =
                    activeSlide.querySelector(
                        ".hero-content"
                    );

                if (content) {

                    requestAnimationFrame(function () {

                        content.style.opacity = "1";

                        content.style.transform =
                            "translateY(0) translateX(0)";

                    });

                }

            }
        );

    }


    /* =====================================================
       03. NUMBER COUNTERS
       ===================================================== */

    const counters =
        document.querySelectorAll(".counter");

    const statsSection =
        document.querySelector(
            ".solar-stats-section"
        );


    function animateCounter(counter) {

        if (!counter) {
            return;
        }


        /* Prevent duplicate animation */

        if (
            counter.dataset.started === "true"
        ) {
            return;
        }


        counter.dataset.started = "true";


        const target =
            parseInt(
                counter.getAttribute("data-target"),
                10
            );


        if (isNaN(target)) {

            counter.textContent = "0";

            return;
        }


        let current = 0;


        const duration = 1800;

        const startTime =
            performance.now();


        function updateCounter(currentTime) {

            const elapsed =
                currentTime - startTime;


            const progress =
                Math.min(
                    elapsed / duration,
                    1
                );


            /*
             * Smooth ease-out animation
             */

            const easedProgress =
                1 - Math.pow(
                    1 - progress,
                    3
                );


            current =
                Math.floor(
                    easedProgress * target
                );


            counter.textContent =
                current.toLocaleString();


            if (progress < 1) {

                requestAnimationFrame(
                    updateCounter
                );

            } else {

                counter.textContent =
                    target.toLocaleString();

            }

        }


        requestAnimationFrame(
            updateCounter
        );

    }


    /* =====================================================
       04. START COUNTERS WHEN VISIBLE
       ===================================================== */

    if (counters.length) {

        if (
            "IntersectionObserver"
            in window
        ) {

            const counterObserver =
                new IntersectionObserver(
                    function (entries, observer) {

                        entries.forEach(
                            function (entry) {

                                if (
                                    entry.isIntersecting
                                ) {

                                    const sectionCounters =
                                        entry.target.querySelectorAll(
                                            ".counter"
                                        );


                                    sectionCounters.forEach(
                                        function (counter) {

                                            animateCounter(
                                                counter
                                            );

                                        }
                                    );


                                    observer.unobserve(
                                        entry.target
                                    );

                                }

                            }
                        );

                    },
                    {
                        threshold: 0.25
                    }
                );


            if (statsSection) {

                counterObserver.observe(
                    statsSection
                );

            } else {

                counters.forEach(
                    function (counter) {

                        animateCounter(
                            counter
                        );

                    }
                );

            }

        } else {

            /*
             * Fallback for older browsers
             */

            counters.forEach(
                function (counter) {

                    animateCounter(
                        counter
                    );

                }
            );

        }

    }


    /* =====================================================
       05. SCROLL REVEAL
       ===================================================== */

    const revealElements =
        document.querySelectorAll(
            ".solar-stat-card, " +
            ".about-highlight-card, " +
            ".solar-product-card, " +
            ".installation-card, " +
            ".why-card, " +
            ".testimonial-card"
        );


    if (
        revealElements.length &&
        "IntersectionObserver" in window
    ) {

        revealElements.forEach(
            function (element, index) {

                element.style.opacity = "0";

                element.style.transform =
                    "translateY(35px) scale(0.97)";

                element.style.transition =
                    "opacity 0.75s ease " +
                    (index % 4) * 0.08 +
                    "s, " +
                    "transform 0.75s cubic-bezier(0.22,1,0.36,1) " +
                    (index % 4) * 0.08 +
                    "s";

            }
        );


        const revealObserver =
            new IntersectionObserver(
                function (entries, observer) {

                    entries.forEach(
                        function (entry) {

                            if (
                                entry.isIntersecting
                            ) {

                                entry.target.style.opacity =
                                    "1";

                                entry.target.style.transform =
                                    "translateY(0) scale(1)";


                                observer.unobserve(
                                    entry.target
                                );

                            }

                        }
                    );

                },
                {
                    threshold: 0.12,
                    rootMargin:
                        "0px 0px -50px 0px"
                }
            );


        revealElements.forEach(
            function (element) {

                revealObserver.observe(
                    element
                );

            }
        );

    }


    /* =====================================================
       06. SMOOTH ANCHOR SCROLL
       ===================================================== */

    const anchorLinks =
        document.querySelectorAll(
            'a[href^="#"]'
        );


    anchorLinks.forEach(
        function (link) {

            link.addEventListener(
                "click",
                function (event) {

                    const targetId =
                        link.getAttribute(
                            "href"
                        );


                    if (
                        !targetId ||
                        targetId === "#"
                    ) {
                        return;
                    }


                    const target =
                        document.querySelector(
                            targetId
                        );


                    if (!target) {
                        return;
                    }


                    event.preventDefault();


                    const navbar =
                        document.querySelector(
                            ".navbar"
                        );


                    const navbarHeight =
                        navbar
                            ? navbar.offsetHeight
                            : 0;


                    const targetPosition =
                        target.getBoundingClientRect()
                            .top +
                        window.scrollY -
                        navbarHeight -
                        15;


                    window.scrollTo(
                        {
                            top:
                                targetPosition,

                            behavior:
                                "smooth"
                        }
                    );

                }
            );

        }
    );


    /* =====================================================
       07. HERO BUTTON RIPPLE EFFECT
       ===================================================== */

    const heroButtons =
        document.querySelectorAll(
            ".hero-btn, .section-btn, .cta-btn, .contact-cta-btn"
        );


    heroButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function (event) {

                    const ripple =
                        document.createElement(
                            "span"
                        );


                    const rect =
                        button.getBoundingClientRect();


                    const size =
                        Math.max(
                            rect.width,
                            rect.height
                        );


                    const x =
                        event.clientX -
                        rect.left -
                        size / 2;


                    const y =
                        event.clientY -
                        rect.top -
                        size / 2;


                    ripple.style.position =
                        "absolute";

                    ripple.style.width =
                        size + "px";

                    ripple.style.height =
                        size + "px";

                    ripple.style.left =
                        x + "px";

                    ripple.style.top =
                        y + "px";

                    ripple.style.borderRadius =
                        "50%";

                    ripple.style.background =
                        "rgba(255,255,255,0.25)";

                    ripple.style.pointerEvents =
                        "none";

                    ripple.style.transform =
                        "scale(0)";

                    ripple.style.opacity =
                        "1";

                    ripple.style.transition =
                        "transform 0.6s ease, opacity 0.6s ease";


                    button.style.position =
                        "relative";

                    button.style.overflow =
                        "hidden";


                    button.appendChild(
                        ripple
                    );


                    requestAnimationFrame(
                        function () {

                            ripple.style.transform =
                                "scale(2.5)";

                            ripple.style.opacity =
                                "0";

                        }
                    );


                    setTimeout(
                        function () {

                            ripple.remove();

                        },
                        650
                    );

                }
            );

        }
    );


    /* =====================================================
       08. PRODUCT CARD TILT EFFECT
       ===================================================== */

    const productCards =
        document.querySelectorAll(
            ".solar-product-card"
        );


    if (
        window.matchMedia(
            "(min-width: 992px)"
        ).matches
    ) {

        productCards.forEach(
            function (card) {

                card.addEventListener(
                    "mousemove",
                    function (event) {

                        const rect =
                            card.getBoundingClientRect();


                        const x =
                            event.clientX -
                            rect.left;


                        const y =
                            event.clientY -
                            rect.top;


                        const centerX =
                            rect.width / 2;


                        const centerY =
                            rect.height / 2;


                        const rotateX =
                            (y - centerY) /
                            30;


                        const rotateY =
                            (centerX - x) /
                            30;


                        card.style.transform =
                            "perspective(900px) " +
                            "rotateX(" +
                            rotateX +
                            "deg) " +
                            "rotateY(" +
                            rotateY +
                            "deg) " +
                            "translateY(-12px)";

                    }
                );


                card.addEventListener(
                    "mouseleave",
                    function () {

                        card.style.transform =
                            "";

                    }
                );

            }
        );

    }


    /* =====================================================
       09. ACTIVE NAVIGATION LINK
       ===================================================== */

    const currentPath =
        window.location.pathname
            .replace(/\/$/, "");


    const navLinks =
        document.querySelectorAll(
            ".navbar-nav .nav-link"
        );


    navLinks.forEach(
        function (link) {

            const href =
                link.getAttribute("href");


            if (!href) {
                return;
            }


            try {

                const linkURL =
                    new URL(
                        href,
                        window.location.origin
                    );


                const linkPath =
                    linkURL.pathname
                        .replace(/\/$/, "");


                if (
                    linkPath === currentPath
                ) {

                    link.classList.add(
                        "active"
                    );

                }

            } catch (error) {

                /* Ignore invalid URLs */

            }

        }
    );


    /* =====================================================
       10. NAVBAR SCROLL EFFECT
       ===================================================== */

    const navbar =
        document.querySelector(
            ".navbar"
        );


    function updateNavbar() {

        if (!navbar) {
            return;
        }


        if (window.scrollY > 30) {

            navbar.classList.add(
                "navbar-scrolled"
            );

        } else {

            navbar.classList.remove(
                "navbar-scrolled"
            );

        }

    }


    window.addEventListener(
        "scroll",
        updateNavbar,
        {
            passive: true
        }
    );


    updateNavbar();


    /* =====================================================
       11. PARALLAX HERO
       ===================================================== */

    const heroImages =
        document.querySelectorAll(
            ".slider-image"
        );


    if (
        heroImages.length &&
        window.matchMedia(
            "(min-width: 768px)"
        ).matches
    ) {

        window.addEventListener(
            "scroll",
            function () {

                const hero =
                    document.querySelector(
                        ".solar-hero"
                    );


                if (!hero) {
                    return;
                }


                const heroRect =
                    hero.getBoundingClientRect();


                if (
                    heroRect.bottom < 0 ||
                    heroRect.top > window.innerHeight
                ) {
                    return;
                }


                const movement =
                    window.scrollY * 0.08;


                heroImages.forEach(
                    function (image) {

                        image.style.transform =
                            "scale(1.05) " +
                            "translateY(" +
                            movement +
                            "px)";

                    }
                );

            },
            {
                passive: true
            }
        );

    }


    /* =====================================================
       12. PAGE LOADED
       ===================================================== */

    document.documentElement.classList.add(
        "home-page-loaded"
    );


    console.log(
        "Sungreen Solar Home JS loaded successfully."
    );

});