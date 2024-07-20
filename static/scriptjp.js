function showMessageBubble() {
    const bubblemsg = document.getElementById('message-bubble');
    bubblemsg.classList.add('message-bubble-visible');
    }
    
function translat() {
    const text = document.getElementById('message-input').value;
    const name = document.getElementById('name').value
    const post = document.getElementById('post').value; 
    const chatMessages = document.getElementById('chat-messages');
    const bubblemsg = document.getElementById('message-bubble')
    const popbubble = document.getElementById('message-bubble')
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'message';
    userMessageElement.textContent = `You: ${text}`;
    bubblemsg.appendChild(userMessageElement)
    
    fetch('/translatjp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text, name: name, post: post })
    })
    .then(response => response.json())
    .then(data => {
        if (data.serial_number) {
            fetch('/speechjp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ serial_number: data.serial_number, name: name, post: post})
            })
            .then(response => response.json())
            .then(data => {
                if (data.audio_url) {
                    const audioDiv = document.createElement('div');
                    const audio = new Audio(data.audio_url);
                    audio.controls = false;
    
                    const playPauseButton = document.createElement('button');
                    playPauseButton.className = 'audio-control';
                    playPauseButton.innerHTML = "<img src='static/img/unmute.jpeg' alt='Pause'>";
                    let isPlaying = false;
    
                    playPauseButton.addEventListener('click', function() {
                        if (!isPlaying) {
                            audio.play();
                            playPauseButton.innerHTML = "<img src='static/img/unmute.jpeg' alt='Pause'>";
                            isPlaying = true;
                        } else {
                            audio.pause();
                            playPauseButton.innerHTML = "<img src='static/img/muted.jpeg' alt='Play'>";
                            isPlaying = false;
                        }
                    });
    
                    audio.addEventListener('play', function() {
                        playPauseButton.innerHTML ="<img src='static/img/unmute.jpeg' alt='Pause'>";
                        isPlaying = true;
                    });
    
                    audio.addEventListener('pause', function() {
                        playPauseButton.innerHTML = "<img src='static/img/muted.jpeg' alt='play'>";
                        isPlaying = false;
                    });
    
                    audioDiv.className = 'audio-controls';
                    audioDiv.appendChild(playPauseButton);
                    audioDiv.appendChild(audio);
                    bubblemsg.appendChild(audioDiv);
                }
            });
    
            const translatedText = data.translated_text;
            const translatedMessageElement = document.createElement('div');
            translatedMessageElement.className = 'message';
            translatedMessageElement.textContent = `${translatedText}`;
            bubblemsg.appendChild(translatedMessageElement);
    
            showMessageBubble();
        }
    });
}

function transparent() {
const bubblemsg = document.getElementById('message-bubble');
bubblemsg.classList.remove('message-bubble-visible');
}
function moveMessages() {
const bubblemsg = document.getElementById('message-bubble');
const chatMessages = document.getElementById('chat-messages');
// Move all messages from bubblemsg to chatMessages
while (bubblemsg.firstChild) {
    chatMessages.appendChild(bubblemsg.firstChild);
}
transparent();
}
function showchat() {
document.getElementById('show').addEventListener('click', function() {
const chatContainer = document.getElementById('chat-container');
chatContainer.classList.toggle('chat-container-visible');
});
}

document.getElementById('next').addEventListener('click', moveMessages);

const myModelViewer = document.getElementById('myModelViewer');
myModelViewer.cameraOrbit = '0deg 90deg 2m';
myModelViewer.cameraTarget = '20m 59m 700m';
myModelViewer.cameraFov = '60deg';