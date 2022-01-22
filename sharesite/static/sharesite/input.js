var index = 1;
var correctWord = "PRICK";

function getGridString() {
  result = "";
  for (var i = 0; i < 30; i++) {
    result = result + $("#input-box-" + (i + 1)).data("val");
  }
  return result;
}

function decodeWord(result) {
  regexStr = ""
  possibleLetters = correctWord.split("");
  for (var i = 0; i < result.length; i++) {
    if (result[i] == "X") {
      regexStr += correctWord[i];
      idx = possibleLetters.indexOf(correctWord[i]);
      if(idx !== -1) {
        possibleLetters.splice(idx, 1);
      }
    } else if (result[i] == "O") {
      regexStr += "[" + possibleLetters.join("") + "]";
    } else {
      regexStr += "[^" + possibleLetters.join("") + "]";
    }
  }
  regexStr = regexStr.toLowerCase();
  console.log(regexStr);
  const regex = new RegExp(regexStr, 'g');
  matchedWords = possibleWords.filter(str => str.match(regex));
  console.log(matchedWords);
}

function handlePaste(paste) {
  paste = paste.toUpperCase().split("\n");
  if(paste[0].slice(0,6) == "WORDLE"){
    grid = paste.slice(2);
    for (var i = 0; i < grid.length; i++) {
      char_loc = 0;
      for (const symbol of grid[i]){
        if(symbol == "🟩"){
          tile = $("#input-box-" + (i * 5 + char_loc + 1));
          tile.removeClass("empty");
          tile.addClass("correct");
          tile.text(correctWord[char_loc]);
          tile.data("val", correctWord[char_loc]);
        }
        if(symbol == "🟨"){
          tile = i * 5 + char_loc + 1;
          tile = $("#input-box-" + (i * 5 + char_loc + 1));
          tile.removeClass("empty");
          tile.addClass("semi-correct");
          tile.data("val", ".");
        }
        if(symbol == "⬜"){
          tile = i * 5 + char_loc + 1;
          tile = $("#input-box-" + (i * 5 + char_loc + 1));
          tile.removeClass("empty");
          tile.addClass("incorrect");
          tile.data("val", " ");
        }
        char_loc++;
        index = i * 5 + char_loc + 1;
        $(".current").removeClass("current");
        $("#input-box-" + index).addClass("current");
      }
    }
  }
}

$('document').ready(function(){
  document.addEventListener('keyup', function(event) {
    $("#dummy-box").val("");
  });

  document.addEventListener('keydown', function(event) {
    $("#dummy-box").val("");
    $(".current").removeClass("current");
    if(event.key.toUpperCase() == "BACKSPACE") {
      if(index > 1){
        index--;
      }
      $("#input-box-" + index).text("");
      $("#input-box-" + index).data("val", "");
      $("#input-box-" + index).removeClass("correct");
      $("#input-box-" + index).removeClass("semi-correct");
      $("#input-box-" + index).removeClass("incorrect");
      $("#input-box-" + index).addClass("empty");
    }
    if(event.key.match(/^[a-z]$/i) && !event.ctrlKey && !event.metaKey && !event.altKey) {
      $("#input-box-" + index).text(event.key.toUpperCase());
      $("#input-box-" + index).data("val", event.key.toUpperCase());
      $("#input-box-" + index).removeClass("empty");
      $("#input-box-" + index).removeClass("correct");
      $("#input-box-" + index).removeClass("semi-correct");
      $("#input-box-" + index).removeClass("incorrect");
      if(event.key.toUpperCase() == correctWord[(index - 1) % 5]) {
        $("#input-box-" + index).addClass("correct");
      } else if (correctWord.indexOf(event.key.toUpperCase()) !== -1) {
        $("#input-box-" + index).addClass("semi-correct");
      } else {
        $("#input-box-" + index).addClass("incorrect");
      }
      if(index <= 30){
        index++;
      }
    }
    $("#input-box-" + index).addClass("current");
  });

  $(".tile").click(function() {
    $(".current").removeClass("current");
    $(this).addClass("current");
    index = $(this).data("tile");
  });

  document.addEventListener('paste', (event) => {
    let paste = (event.clipboardData || window.clipboardData).getData('text');
    handlePaste(paste);
    event.preventDefault();
  });

  $("#input-box-1").addClass("current");  
});
