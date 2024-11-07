var $messages = $('.messages-content'),
    d, h, m,
    id = generateSessionId();  // Generate id when page loads

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    showLoadingMessage();  // Show loading animation before displaying the first message
    setTimeout(function() {
      firstMessage();  // Display first message after the loading animation
    }, 2000); // 2 seconds delay for the first message
  }, 100);
});

function generateSessionId() {
  // Generate a unique session ID (for example, a random string or UUID)
  return 'sess_' + Math.random().toString(36).substr(2, 9);
}

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate() {
  d = new Date();

  let hours = addLeadingZero(d.getHours());
  let minutes = addLeadingZero(d.getMinutes());

  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + hours + ':' + minutes + '</div>').appendTo($('.message:last'));
  }
}

// Helper function to add a leading zero if needed
function addLeadingZero(num) {
  return (num < 10 ? '0' : '') + num;
}

function insertMessage() {
  let msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();

  // Send the message to the server with a delay before showing loading animation
  sendMessageToServer(msg);
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
});

function sendMessageToServer(message) {
  // Use setTimeout to delay showing the loading message
  setTimeout(function() {
    showLoadingMessage(); // Show loading message after the specified delay
  }, 2000); // 2 seconds delay

  $.ajax({
    url: '/process',  // Your server endpoint
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ "message": message, "id": id }),
    success: function(response) {
      // Handle the response from the server and display it
      receiveMessage(response.response);  // Assuming server returns {response: "message"}
    },
    error: function() {
      console.error('Error in sending message.');
      // Optionally hide loading message or show an error message
      hideLoadingMessage();
    }
  });
}

function receiveMessage(message) {
  // Hide loading message once we get a response
  hideLoadingMessage();
  $('<div class="message new"><figure class="avatar"><img src="static/assets/profile.png" /></figure>' + message + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  updateScrollbar();
}

function firstMessage() {
  // Display the first message "Hi there, I'm Komiljon and you?" after generating the session ID
  let firstMsg = "Salom! Mening ismim Jahongir. Sizga qanday yordam berishim mumkin?";
  hideLoadingMessage();  // Remove loading message before displaying the first message
  $('<div class="message new"><figure class="avatar"><img src="static/assets/profile.png" /></figure>' + firstMsg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  updateScrollbar();

  // Note: The first message is displayed only and not sent to the server
}

function showLoadingMessage() {
  // Show a loading animation or message while waiting for a response
  $('<div class="message loading new"><figure class="avatar"><img src="static/assets/profile.png" /></figure><span>Loading...</span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();
}

function hideLoadingMessage() {
  // Remove the loading message after getting the response or before showing the first message
  $('.message.loading').remove();
}