let arrayDates = ["s18102025", "12122027y", "16032026"]

function parseDate(str) {
  const digits = str.replace(/\D/g, ""); // remove letras
  const day = Number(digits.slice(0, 2));
  const month = Number(digits.slice(2, 4)) - 1; // JS começa em 0
  const year = Number(digits.slice(4, 8));

  return new Date(year, month, day);
}

const newestString = arrayDates.reduce((oldest, current) => {
  return parseDate(current) < parseDate(oldest) ? current : oldest;
});

console.log(newestString);