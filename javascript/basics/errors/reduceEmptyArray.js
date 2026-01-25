// TypeError: Reduce of empty array with no initial value

// The TypeError: Reduce of empty array with no initial value occurs when the JavaScript Array.prototype.reduce() method is called on an empty array without providing an explicit initial value. 

// erro
// const numbers = [];
// const sum = numbers.reduce((accumulator, currentValue) => accumulator + currentValue);

// fix
const numbersFix = [];
const sumFix = numbersFix.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
