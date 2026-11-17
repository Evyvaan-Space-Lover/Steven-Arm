
const servoControls = document.getElementById("servo-controls");
const emergencyStopButton = document.getElementById("emergency-stop");
const resetStopButton = document.getElementById("reset-stop");

const SERVO_COUNT = 6;

// Create one slider for each servo.
for (let channel = 0; channel < SERVO_COUNT; channel++) {
    const container = document.createElement("div");

    const label = document.createElement("label");
    label.textContent = `Servo ${channel + 1}: `;

    const value = document.createElement("span");
    value.textContent = "90°";

    const slider = document.createElement("input");
    slider.type = "range";
    slider.min = 0;
    slider.max = 180;
    slider.value = 90;

    slider.addEventListener("input", () => {
        value.textContent = `${slider.value}°`;
    });

    slider.addEventListener("change", async () => {
        try {
            const response = await fetch(`/api/servo/${channel}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    angle: Number(slider.value)
                })
            });

            if (!response.ok) {
                const error = await response.json();
                alert(error.detail || "Motor command failed.");
            }
        } catch (error) {
            alert("Could not connect to Steven's server.");
        }
    });

    label.appendChild(value);
    container.appendChild(label);
    container.appendChild(document.createElement("br"));
    container.appendChild(slider);

    servoControls.appendChild(container);
}

// Emergency stop.
emergencyStopButton.addEventListener("click", async () => {
    try {
        const response = await fetch("/api/emergency-stop", {
            method: "POST"
        });

        if (!response.ok) {
            alert("Emergency stop request failed.");
        }
    } catch (error) {
        alert("Could not connect to Steven's server.");
    }
});

// Reset emergency stop.
resetStopButton.addEventListener("click", async () => {
    try {
        const response = await fetch("/api/reset-emergency-stop", {
            method: "POST"
        });

        if (!response.ok) {
            const error = await response.json();
            alert(error.detail || "Could not reset emergency stop.");
        }
    } catch (error) {
        alert("Could not connect to Steven's server.");
    }
});


// cam con

const cameraFeed = document.getElementById("camera-feed");
const cameraStatus = document.getElementById("camera-status");

async function connectCamera() {

    try {

        const response = await fetch("/api/camera/status");
        const status = await response.json();

        if (status.available) {

            cameraFeed.src = "/camera/stream";
            cameraStatus.textContent =
                `Camera connected: ${status.resolution} at ${status.fps} FPS`;

        } else {

            cameraStatus.textContent =
                "Camera unavailable: " + (status.error || "No camera detected.");

        }

    } catch (error) {

        cameraStatus.textContent =
            "Could not connect to camera server.";

    }
}

connectCamera();

