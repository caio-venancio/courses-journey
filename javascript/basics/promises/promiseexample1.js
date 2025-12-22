//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise
//https://javascript.info/promise-basics
//https://www.w3schools.com/js/js_promise.asp

let myPromise = new Promise(function(myResolve, myReject) {
  setTimeout(function() { myResolve("I love You !!"); }, 2000);
});

myPromise.then(function(value) {
  console.log(value);
});