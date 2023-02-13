const body = document.querySelector("body"),
      sidebar = body.querySelector(".sidebar"),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");
      searchIcon = body.querySelector(".search-box i");
      navlink = body.querySelector(".nav-link");
      navLinkElements = document.getElementsByClassName("nav-link");
      searchBox = body.querySelector(".search-box");


      toggle.addEventListener("click", () =>{
        sidebar.classList.toggle("close");
        searchBox.classList.toggle("tooltip")
        for (var i = 0; i < navLinkElements.length; i++){
          navLinkElements[i].classList.toggle("tooltip");
        }
      });

      searchIcon.addEventListener("click", () =>{
        if (sidebar.classList.contains("close")){
          sidebar.classList.toggle("close");
        }
      })

      modeSwitch.addEventListener("click", () =>{
        body.classList.toggle("light");

        if (body.classList.contains("light")){
          modeText.innerText = "Light Mode";
        }else{
          modeText.innerText = "Dark Mode";
        }

      });

      // When the user scrolls the page, execute myFunction 
        window.onscroll = function() {scrollProgress()};

        function scrollProgress() {
          var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
          var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
          var scrolled = (winScroll / height) * 80;
          document.getElementById("progressPoint").style.top = scrolled + 10 + "%";
        }