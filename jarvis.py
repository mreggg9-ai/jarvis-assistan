
import datetime
import webbrowser
import urllib.parse

# Optional voice output
try:
    import pyttsx3
    speaker = pyttsx3.init()
    speaker.setProperty("rate", 170)
except Exception:
    speaker = None

def speak(text):
    print("JARVIS:", text)

    if speaker:
        try:
            speaker.say(text)
            speaker.runAndWait()
        except Exception:
            pass

def run_jarvis():
    speak("Hello boss! JARVIS is online.")
    speak("Type help to see what I can do.")

    while True:
        command = input("\nYou: ").strip().lower()

        if command in ("exit", "quit", "shutdown"):
            speak("Goodbye boss!")
            break

        elif command == "help":
            speak(
                "Commands: time, date, google, youtube, "
                "search followed by a topic, help, exit."
            )

        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak("The time is " + now)

        elif "date" in command:
            today = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today's date is " + today)

        elif command == "google":
            webbrowser.open("https://www.google.com")
            speak("Opening Google.")

        elif command == "youtube":
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.")

        elif command.startswith("search "):
            query = command[7:].strip()

            if query:
                url = (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote_plus(query)
                )
                webbrowser.open(url)
                speak("Searching Google for " + query)
            else:
                speak("Please tell me what to search for.")

        else:
            speak("I don't know that command yet. Type help.")

if __name__ == "__main__":
    run_jarvis()
 
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>My Jarvis Assistant</title>
</head>
<body style="background:#101820;color:#00ffcc;text-align:center;font-family:Arial;padding:40px">
  <h1>🤖 JARVIS</h1>
  <h3 id="status">Click Start Listening</h3>
  <button onclick="startJarvis()">Start Listening</button>
  <button onclick="stopJarvis()">Stop</button>
  <p id="heard">Waiting for you...</p>

<script>
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition;
let active = false;
let awake = false;

function speak(text) {
  document.getElementById("status").textContent = text;
  speechSynthesis.cancel();
  speechSynthesis.speak(new SpeechSynthesisUtterance(text));
}

function startJarvis() {
  if (!SpeechRecognition) {
    speak("Speech recognition is not supported. Please try Chrome.");
    return;
  }

  if (active) return;
  active = true;
  awake = false;

  recognition = new SpeechRecognition();
  recognition.lang = "en-IN";
  recognition.continuous = true;
  recognition.interimResults = false;

  recognition.onresult = function(event) {
    const text = event.results[event.results.length - 1][0]
      .transcript.toLowerCase().trim();

    document.getElementById("heard").textContent = "Heard: " + text;

    if (!awake) {
      if (text.includes("hey jarvis")) {
        awake = true;
        speak("I'm listening, boss. What do you need?");
      }
      return;
    }

    awake = false;

    if (text.includes("youtube")) {
      speak("Opening YouTube");
      window.open("https://www.youtube.com", "_blank");
    } else if (text.includes("google")) {
      speak("Opening Google");
      window.open("https://www.google.com", "_blank");
    } else if (text.includes("time")) {
      speak("The time is " +
        new Date().toLocaleTimeString("en-IN"));
    } else if (text.includes("date")) {
      speak("Today is " +
        new Date().toLocaleDateString("en-IN"));
    } else if (text.startsWith("search ")) {
      const query = text.substring(7);
      speak("Searching Google");
      window.open(
        "https://www.google.com/search?q=" +
        encodeURIComponent(query), "_blank");
    } else {
      speak("Sorry boss, I don't know that command yet.");
    }
  };

  recognition.onerror = function(event) {
    document.getElementById("status").textContent =
      "Microphone: " + event.error;
  };

  recognition.onend = function() {
    if (active) {
      try { recognition.start(); } catch (e) {}
    }
  };

  try {
    recognition.start();
    speak("Jarvis is ready. Say Hey Jarvis.");
  } catch (e) {
    active = false;
    speak("Could not start listening. Please try again.");
  }
}

function stopJarvis() {
  active = false;
  awake = false;
  if (recognition) recognition.stop();
  speechSynthesis.cancel();
  document.getElementById("status").textContent = "Jarvis stopped";
}
</script>
</body>
</html>
