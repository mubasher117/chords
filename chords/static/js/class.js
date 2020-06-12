
let loc = window.location.href;
let curr = loc.split('/')
let activeAlphabet  = curr[curr.length-1]
var element = document.getElementById(activeAlphabet);
element.classList.add('active');