var index = 1;

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

function populateGrid(grid_str) {
  grid_str = grid_str.toUpperCase();
  for (var i = 0; i < grid_str.length; i++) {
    $("#input-box-" + (i + 1)).text(grid_str[i]);
    $("#input-box-" + (i + 1)).data("val", grid_str[i]);
    $("#input-box-" + (i + 1)).removeClass("empty");
    if(grid_str[i] == correctWord[(i) % 5]) {
      $("#input-box-" + (i + 1)).addClass("correct");
    } else if (correctWord.indexOf(grid_str[i]) !== -1) {
      $("#input-box-" + (i + 1)).addClass("semi-correct");
    } else {
      $("#input-box-" + (i + 1)).addClass("incorrect");
    }
  }
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
  $(".current").removeClass("current");
  index = $("#dummy-box")[0].selectionStart;
  $("#input-box-" + index).addClass("current");

}

function addEventToGrid(keyEvent) {
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
  gridToTextbox();
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
        addEventToGrid(event);
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