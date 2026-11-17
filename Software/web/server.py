
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from hardware.motor_controller import MotorController
from hardware.camera import StevenCamera


STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Steven", version="0.1.0", description="Steven's Web API and nothing else really. fyi i really like space, astrophysics, and astronomy. i also like to make things. this is one of those things.")

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

motor_controller = MotorController()
camera = StevenCamera()



class ServoCommand(BaseModel):
    angle: float



@app.get("/")
def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/status")
def get_status():
    return motor_controller.get_status()


@app.post("/api/servo/{channel}")
def set_servo(channel: int, command: ServoCommand):

    try:
        position = motor_controller.set_angle(
            channel,
            command.angle
        )

        return {
            "success": True,
            "channel": channel,
            "position": position
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except RuntimeError as error:
        raise HTTPException(status_code=409, detail=str(error))


@app.post("/api/emergency-stop")
def emergency_stop():

    motor_controller.emergency_stop()

    return {
        "success": True,
        "message": "Emergency stop activated."
    }


@app.post("/api/reset-emergency-stop")
def reset_emergency_stop():

    try:
        motor_controller.reset_emergency_stop()

        return {
            "success": True,
            "message": "Emergency stop reset."
        }

    except RuntimeError as error:
        raise HTTPException(status_code=409, detail=str(error))


@app.on_event("startup")
def initialise_camera():

    try:
        camera.start()

        print("Steven camera initialised.")

    except Exception as error:

        print(f"Steven camera unavailable: {error}")


@app.get("/api/camera/status")
def get_camera_status():

    return camera.get_status()


@app.get("/camera/stream")
def camera_stream():

    if not camera.available:
        raise HTTPException(
            status_code=503,
            detail="Steven's camera is currently unavailable."
        )

    return StreamingResponse(
        camera.generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.on_event("shutdown")
def shutdown_system():

    camera.stop()

    print("Steven camera stopped.")
