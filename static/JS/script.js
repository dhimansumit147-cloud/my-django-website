
/* ===============================
 ACTIVE CURRENT PAGE
================================ */


let currentPage = window.location.pathname;


document.querySelectorAll(".sidebar a").forEach(link=>{


    let linkPage = link.getAttribute("href");


    if(linkPage && linkPage !== "javascript:void(0)"){


        if(linkPage === currentPage){


            link.classList.add("active");


            let submenu = link.closest(".submenu");


            if(submenu){


                submenu.style.display="block";


                submenu.previousElementSibling.classList.add("active");


            }


        }


    }


});



/* ===============================
 DROPDOWN
================================ */


document.querySelectorAll(".menu-link").forEach(item=>{


item.addEventListener("click",()=>{


let submenu=item.nextElementSibling;


if(submenu.style.display==="block"){

submenu.style.display="none";

}

else{

submenu.style.display="block";

}


});


});


