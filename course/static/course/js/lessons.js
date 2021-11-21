document.addEventListener("DOMContentLoaded", function(event) {
  let items = document.getElementsByClassName("collapsable");
  for(let i = 0; i < items.length; i++) {
      items[i].getElementsByClassName("lesson-title-content")[0].onclick = () => {
          console.log(items[i].getElementsByClassName("lesson-content")[0]);
          if(items[i].getElementsByClassName("lesson-content")[0].classList.contains("opened"))
            items[i].getElementsByClassName("lesson-content")[0].classList.remove("opened");
          else  
            items[i].getElementsByClassName("lesson-content")[0].classList.add("opened");
         
          if(items[i].getElementsByClassName("collapse-icon")[0].classList.contains("reversed"))
            items[i].getElementsByClassName("collapse-icon")[0].classList.remove("reversed");
          else  
            items[i].getElementsByClassName("collapse-icon")[0].classList.add("reversed");
      };
  }
});