function displayStatus(){
  let f = document.getElementById("search-class-id");
  if ( f.style.display == 'none' ){
    //If the div is hidden, show it
    f.style.display = 'block';
  } else {
    //If the div is shown, hide it
    f.style.display = 'none';
  }
};

function SearchStudentBtn(){
  let search_with_name = document.getElementById("search-with-name");
  let search_with_class = document.getElementById("search-with-class");
  let search_with_MSHS = document.getElementById("search-with-MSHS");
  let input_search_name = document.getElementById("input-search-name");
  let input_search_class = document.getElementById("input-search-class");
  let input_search_MSHS = document.getElementById("input-search-MSHS");
  if ( search_with_name.selected == true ){
    //If the div is hidden, show it
    input_search_name.style.display = 'block';
    input_search_class.style.display = 'none';
    input_search_MSHS.style.display = 'none';
  } else if ( search_with_class.selected == true ) {
    //If the div is shown, hide it
    input_search_name.style.display = 'none';
    input_search_class.style.display = 'block';
    input_search_MSHS.style.display = 'none';
  }
  else {
    input_search_name.style.display = 'none';
    input_search_class.style.display = 'none';
    input_search_MSHS.style.display = 'block';
  }
};
