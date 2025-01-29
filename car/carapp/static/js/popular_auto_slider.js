document.addEventListener("DOMContentLoaded", () => {
    new Swiper(".korea .mySwiperl",{
        slidesPerView: "auto",
        spaceBetween: 16,
        centeredSlides: !0,
        pagination: {
            clickable: !0
        },
        navigation: {
            nextEl: ".korea .swiper_next",
            prevEl: ".korea .swiper_prev"
        },
        breakpoints: {
            0: {
                spaceBetween: 12
            },
            768: {
                spaceBetween: 16
            }
        }
    }),
    new Swiper(".china .mySwiperl",{
        slidesPerView: "auto",
        spaceBetween: 16,
        centeredSlides: !0,
        pagination: {
            clickable: !0
        },
        navigation: {
            nextEl: ".china .swiper_next",
            prevEl: ".china .swiper_prev"
        },
        breakpoints: {
            0: {
                spaceBetween: 12
            },
            768: {
                spaceBetween: 16
            }
        },
        on: {
            afterInit: function(e) {
                1074 < window.innerWidth ? e.slideTo(e.slides.length - 1) : e.slideTo(0)
            }
        }
    }),
    new Swiper(".japan .mySwiperl",{
        slidesPerView: "auto",
        spaceBetween: 16,
        centeredSlides: !0,
        pagination: {
            clickable: !0
        },
        navigation: {
            nextEl: ".japan .swiper_next",
            prevEl: ".japan .swiper_prev"
        },
        breakpoints: {
            0: {
                spaceBetween: 12
            },
            768: {
                spaceBetween: 16
            }
        }
    })
}
);
var changeCardImage = (e, i, a) => {
    let n = document.querySelector(i + " .img_items .main_card_img")
      , t = document.createElement("img");
    console.log(n),
    t.src = e,
    t.alt = "New Image",
    t.width = n.width,
    t.height = n.height,
    t.classList.add("main_card_img"),
    t.onload = () => {
        n.parentNode.replaceChild(t, n)
    }
    ,
    document.querySelectorAll(i + " .boll").forEach(e => {
        e.classList.remove("active")
    }
    ),
    document.querySelector(i + ` .opener_${a} .boll`).classList.add("active")
}
;
