var requestButton = document.querySelector("#requestButton"),
  skip_animation_button = document.querySelector("#skipAnimationButton"),
  quote_line = document.querySelector("#quote"),
  author_line = document.querySelector("#author"),
  book_line = document.querySelector("#book"),
  typing_sound = new Audio(),
  chosen_quote_object,
  running = 0,
  interval,
  index = 0;

Array.prototype.compare = function(test_array) {
  for (var i = 0; i < this.length; i++) {
    if (test_array.indexOf(this[i]) == -1)
      return false;
  }
  return true;
};

typing_sound.addEventListener("ended", function() {
  this.currentTime = 0;
  // this.play();
});

requestButton.addEventListener("click", function() {
  if (running === 0) {
    quote_line.innerHTML = "";
    author_line.innerHTML = "";
    book_line.innerHTML = "";
    write_quote();
  }
});

skip_animation_button.addEventListener("click", function() {
  typing_sound.pause();
  typing_sound.currentTime = 0;
  running = 0;
  index = 0;
  window.clearInterval(interval);
  quote_line.innerHTML = chosen_quote_object.quote;
  author_line.innerHTML = chosen_quote_object.author;
  book_line.innerHTML = chosen_quote_object.book;
});

function type_out(letter, text, line) {
  letter = index;
  if (letter == text.length) {
    if (text.compare(chosen_quote_object.quote.split(''))) {
      index = 0;
      clearInterval(interval);
      interval = setInterval(type_out, 10, index, chosen_quote_object.author.split(''), author_line, book_line);
      return;
    }
    index = 0;
    typing_sound.pause();
    clearInterval(interval);
    running = 0;
    return;
  }
  line.innerHTML += text[letter];
  index++;
}

function write_quote() {
  // typing_sound.play();
  running = 1;
  const q = quotes[Math.floor(Math.random() * quotes.length)],
    author = q.author.split(''),
    quote = q.quote.split(''),
    book = q.book.split('');
  chosen_quote_object = q;
  interval = setInterval(type_out, 10, index, chosen_quote_object.quote.split(''), quote_line);
}