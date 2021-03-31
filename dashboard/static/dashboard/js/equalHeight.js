(function () {
  equalHeight(false);
})();
 
window.onresize = function(){
  equalHeight(true);
}
 
function equalHeight(resize) {
  var elements = document.getElementsByClassName("equalHeight"),
      allHeights = [],
      i = 0;
  if(resize === true){
    for(i = 0; i < elements.length; i++){
      elements[i].style.height = 'auto';
    }
  }
  for(i = 0; i < elements.length; i++){
    var elementHeight = elements[i].clientHeight;
    allHeights.push(elementHeight);
  }
  for(i = 0; i < elements.length; i++){
    elements[i].style.height = Math.max.apply( Math, allHeights) + 'px';
    if(resize === false){
      elements[i].className = elements[i].className + " show";
    }
  }
}