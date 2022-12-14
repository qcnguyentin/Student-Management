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
  let search_selected = document.getElementById("search-selected").value;
  let input_search_name = document.getElementById("input-search-name");
  let input_search_class = document.getElementById("input-search-class");
  let input_search_MSHS = document.getElementById("input-search-MSHS");
  let a = 'Tìm theo tên'
  let b = 'Tìm theo MSHS'
  let c = 'Tìm theo lớp'
  if ( document.getElementById("search-selected").value >= a ){
    //If the div is hidden, show it
    input_search_name.style.display = 'block';
    input_search_class.style.display = 'none';
    input_search_MSHS.style.display = 'none';
  } else if ( document.getElementById("search-selected").value <= b ) {
    //If the div is shown, hide it
    input_search_name.style.display = 'none';
    input_search_class.style.display = 'none';
    input_search_MSHS.style.display = 'block';
  }
  else {
    input_search_name.style.display = 'none';
    input_search_class.style.display = 'block';
    input_search_MSHS.style.display = 'none';
  }
};
