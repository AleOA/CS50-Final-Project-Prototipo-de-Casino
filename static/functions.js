let counter = 0;
function increment()
{
    counter++
    document.querySelector("#result").innerHTML = counter;
}

var wasSubmitted = false;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let current_number = 0.00;
async function start_multiplier(game_multiplier)
{
    while (current_number < game_multiplier){
        if (current_number == 0.00){
            if (wasSubmitted == true){
                break
            }
            current_number += 1;
            document.getElementById("uptrend_multiplier").value = (Math.round(current_number * 100) / 100).toFixed(2);
            document.querySelector("#live_game").innerHTML = (Math.round(current_number * 100) / 100).toFixed(2);
            await sleep(100)
        } else if (current_number < 5.00 && current_number >= 1.00){
            if (wasSubmitted == true){
                break
            }
            let increment = 0.01;
            current_number += increment;
            document.getElementById("uptrend_multiplier").value = (Math.round(current_number * 100) / 100).toFixed(2);
            document.querySelector("#live_game").innerHTML = (Math.round(current_number * 100) / 100).toFixed(2);
            await sleep(100);
        } else if (current_number >= 5.00 && current_number <= 10.00){
            if (wasSubmitted == true){
                break
            }
            let increment = 0.01;
            current_number += increment;
            document.getElementById("uptrend_multiplier").value = (Math.round(current_number * 100) / 100).toFixed(2);
            document.querySelector("#live_game").innerHTML = (Math.round(current_number * 100) / 100).toFixed(2);
            await sleep(50);
        } else if (current_number > 10.00){
            if (wasSubmitted == true){
                break
            }
            let increment = 0.01;
            current_number += increment;
            document.getElementById("uptrend_multiplier").value = (Math.round(current_number * 100) / 100).toFixed(2);
            document.querySelector("#live_game").innerHTML = (Math.round(current_number * 100) / 100).toFixed(2);
            await sleep(25);
        }


    }

    if (wasSubmitted == false){
        document.getElementById("uptrend_multiplier").value = "JUEGO TERMINADO!";
        document.getElementById("click_cash_out").submit();
    }
}

var x = null;
var y = null;


let start_game_time = 5;
function countdown()
{
    if (start_game_time > 0.1){
        start_game_time = start_game_time - (Math.round(0.1 * 100) / 100).toFixed(2);
        document.querySelector("#descontar").innerHTML = (Math.round(start_game_time * 100) / 100).toFixed(2);

    } else {
        document.querySelector("#descontar").innerHTML = "Jugando";
        document.getElementById("retirar_apuesta").disabled = false;

        clearInterval(x);

    }

}

function check_zero()
{
    if (start_game_time == 5){
        var x = window.setInterval(countdown, 100);
        setTimeout(function() { start_multiplier(game_multiplier); }, 5000);
    }
}

function myFunc() {
    return game_multiplier
}



function checkBeforeSubmit(){
  if(!wasSubmitted) {
    wasSubmitted = true;
    return wasSubmitted;
  }
  return false;
}

function play() {
        var audio = document.getElementById("audio");
        audio.play();
      }

var backgroundmusic = true

function playbackgroundmusic() {
    var backmusic = document.getElementById("backgroundmusic");
    if (backgroundmusic == true){
        backgroundmusic = false;
        backmusic.pause();
        document.getElementById("music").value = "Reanudar Musica";
    } else {
        backgroundmusic = true;
        backmusic.play();
        document.getElementById("music").value = "Pausar Musica";
    }

}

function check_input(quantity)
{
    var bt = document.getElementById("betbutton");
    if (quantity.value != ""){
        bt.disabled = false;
    } else{
        bt.disabled = true;
    }
}