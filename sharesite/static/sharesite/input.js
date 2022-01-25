var index = 1;

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
        if(symbol == "⬜" || symbol == "⬛"){
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

function getGridString() {
  result = "";
  for (var i = 0; i < 30; i++) {
    result = result + $("#input-box-" + (i + 1)).data("val");
  }
  return result;
}

function populateGrid(grid_str) {
  grid_str = grid_str.toUpperCase();
  num_words = Math.ceil(grid_str.length/5);
  for (var i = 0; i < num_words; i++) {
    guess = grid_str.slice(i*5, i*5 + 5);
    word = correctWord;    
    for (var j = 0; j < guess.length; j++) {
      grid_idx = i*5+j+1;
      $("#input-box-" + grid_idx).text(guess[j]);
      $("#input-box-" + grid_idx).data("val", guess[j]);
      $("#input-box-" + grid_idx).removeClass("empty");
      if(correctWord[j] == guess[j]){
        $("#input-box-" + grid_idx).addClass("correct");
        word = word.replace(guess[j], "");
      }
    }
    for (var j = 0; j < guess.length; j++) {
      grid_idx = i*5+j+1;
      if(correctWord[j] != guess[j]){
        if(word.indexOf(guess[j]) != -1){
          $("#input-box-" + grid_idx).addClass("semi-correct");
          word = word.replace(guess[j], "");
        } else {
          $("#input-box-" + grid_idx).addClass("incorrect");
        }
      }
    }
  }
}

function clearGrid() {
  for (var i = 0; i < 30; i++) {
    $("#input-box-" + (i + 1)).text("");
    $("#input-box-" + (i + 1)).data("val", "");
    $("#input-box-" + (i + 1)).removeClass("correct");
    $("#input-box-" + (i + 1)).removeClass("semi-correct");
    $("#input-box-" + (i + 1)).removeClass("incorrect");
    $("#input-box-" + (i + 1)).addClass("empty");
  }
}

function gridToTextbox() {
  $("#dummy-box").val(getGridString());
}

function textboxToGrid() {
  $("#dummy-box").val($("#dummy-box").val().toUpperCase().replace(/\s/g, ''))
  clearGrid();
  populateGrid($("#dummy-box").val());
  if($("#dummy-box").is(":focus")) {
    $(".current").removeClass("current");
    index = $("#dummy-box")[0].selectionStart;
    $("#input-box-" + index).addClass("current");
  }

}

$('document').ready(function(){
  $("#form-submit").click( function(e) {
    if(grid == "") {
      data = getGridString();
      if(data == "" || data.length % 5 != 0){
        e.preventDefault();
        return;
      }
      $("<input />").attr("type", "hidden")
          .attr("name", "grid")
          .attr("value", data)
          .appendTo($("#wordle-data"));
    } else {
      $("<input />").attr("type", "hidden")
          .attr("name", "operation")
          .attr("value", "clear")
          .appendTo($("#wordle-data"));
    }
    $("#wordle-data").submit()
  });

  if(grid != "") {
    populateGrid(grid);
  } else {
    document.addEventListener('keydown', function(event) {
      if(!$("#dummy-box").is(":focus")) {
        $(".current").removeClass("current");
        if(event.key.toUpperCase() == "BACKSPACE") {
          if(index > 1){
            index--;
          }
          $("#input-box-" + index).text("");
          $("#input-box-" + index).data("val", "");
        }
        if(event.key.match(/^[a-z]$/i) && !event.ctrlKey && !event.metaKey && !event.altKey) {
          $("#input-box-" + index).text(event.key.toUpperCase());
          $("#input-box-" + index).data("val", event.key.toUpperCase());
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
        gridToTextbox();
        textboxToGrid();
      }
    });

    $("#dummy-box").click(function() {
      $(".current").removeClass("current");
      index = $("#dummy-box")[0].selectionStart;
      $("#input-box-" + index).addClass("current");
    });

    $(".tile").click(function() {
      $(".current").removeClass("current");
      $(this).addClass("current");
      index = $(this).data("tile");
      $("#dummy-box").focus();
      $("#dummy-box")[0].setSelectionRange(index, index);
    });

    document.addEventListener('paste', (event) => {
      $("#test").text("paste");
      let paste = (event.clipboardData || window.clipboardData).getData('text');
      handlePaste(paste);
      event.preventDefault();
    });

    $("#input-box-1").addClass("current");
  }
});

// function decodeWord(result) {
//   regexStr = ""
//   possibleLetters = correctWord.split("");
//   for (var i = 0; i < result.length; i++) {
//     if (result[i] == "X") {
//       regexStr += correctWord[i];
//       idx = possibleLetters.indexOf(correctWord[i]);
//       if(idx !== -1) {
//         possibleLetters.splice(idx, 1);
//       }
//     } else if (result[i] == "O") {
//       regexStr += "[" + possibleLetters.join("") + "]";
//     } else {
//       regexStr += "[^" + possibleLetters.join("") + "]";
//     }
//   }
//   regexStr = regexStr.toLowerCase();
//   console.log(regexStr);
//   const regex = new RegExp(regexStr, 'g');
//   matchedWords = possibleWords.filter(str => str.match(regex));
//   console.log(matchedWords);
// }