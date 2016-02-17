    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech API not supported in your browser. Please upgrade to latest version.');
    }
    else {
      console.log('speech api supported');
      var recognition = new webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "en-IN"; 
      recognition.maxAlternatives = 3;

      recognition.onstart = function() {
        // Listening (capturing voice from audio input) started.
        // This is a good place to give the user visual feedback about that (i.e. flash a red light, etc.)
        console.log('started');
      };

      recognition.start();

      document.addEventListener('DOMContentLoaded', function () {
        console.log('DOM Loaded');
        $('#start_img').click(function() {
          console.log('clicked');
          recognition.start();
        });
      }, false);

      recognition.onend = function() {
        // If you wish to achieve continuous recognition – you can write a script to start the recognizer again here.
        console.log('ended');
        recognition.stop();
        $('#start_img').click();
      };

      recognition.onerror = function(event) { 
        console.log(event);
        recognition.stop();
      }

      recognition.onresult = function(event) {
        if (typeof(event.results) === 'undefined') {
          recognition.stop();
          return;
        }

        for (var i = event.resultIndex; i < event.results.length; ++i) {      
          if (event.results[i].isFinal) { 
            // Final results
            console.log("final results: " + event.results[i][0].transcript);
            $('#result').text(event.results[i][0].transcript);
            talkToBackend(event.results[i][0].transcript.toLowerCase());
          } 
          // else if((event.results[i][0].transcript.toLowerCase() == 'heera') || (event.results[i][0].transcript.toLowerCase() == 'veera') || (event.results[i][0].transcript.toLowerCase() == 'error') || (event.results[i][0].transcript.toLowerCase() == 'ara') || (event.results[i][0].transcript.toLowerCase() == 'aura') || (event.results[i][0].transcript.toLowerCase() == 'horror')) {
          //   console.log('calling ara');
          //   talkToBackend(event.results[i][0].transcript.toLowerCase());
          //   break;
          // }
          else {
            // You can use these results to give the user near real time experience.
            console.log("interim results: " + event.results[i][0].transcript);
            $('#result').text(event.results[i][0].transcript);
          } 
        }
      }

      var talkToBackend = function(cmd) {
        console.log({'cmd':cmd});
        $.ajax({
          type: "POST",
          url: 'http://127.0.0.1:5000/',
          data: JSON.stringify({'cmd': cmd}),
          dataType: 'json',
          contentType: "application/json; charset=utf-8",
          error: function(e) {
            console.log(e.responseText);
          },
          success: function (data) {
            console.log(data);
          }
        });
      }
    }

    /*var xhr = new XMLHttpRequest();
xhr.open('GET', 'https://developer.chrome.com/static/images/chrome-logo_2x.png', true);
xhr.responseType = 'blob';
xhr.onload = function(e) {
  var img = document.createElement('img');
  img.src = window.URL.createObjectURL(this.response);
  document.body.appendChild(img);
};
xhr.send();*/


