const recordBtn = document.getElementById("record-btn");
const status = document.getElementById("status");
const translation = document.getElementById("translation");

let mediaRecorder;
let audioChunks = [];

recordBtn.addEventListener("click", async () => {
    if (!mediaRecorder) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const formData = new FormData();
            formData.append("audio", audioBlob, "cat-sound.wav");

            status.textContent = "Processing...";
            const response = await fetch("/process-audio", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            translation.textContent = data.translation || "Could not understand.";
            status.textContent = "Press the button to record again.";
        };
    }

    if (mediaRecorder.state === "inactive") {
        audioChunks = [];
        mediaRecorder.start();
        recordBtn.textContent = "⏹️ Stop";
        status.textContent = "Recording...";
    } else {
        mediaRecorder.stop();
        recordBtn.textContent = "🎙️ Record";
    }
});
