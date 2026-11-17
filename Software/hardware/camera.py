
import time
import threading

#steven's eyes wohoo
class StevenCamera:

    def __init__(self, width=1280, height=720, fps=15):

        self.width = width
        self.height = height
        self.fps = fps

        self.camera = None
        self.cv2 = None

        self.running = False
        self.available = False

        self.lock = threading.Lock()
        self.error = None

    def start(self):

        if self.running:
            return

        try:
            import cv2
            from picamera2 import Picamera2

            self.cv2 = cv2
            self.camera = Picamera2()

            configuration = self.camera.create_video_configuration(
                main={
                    "size": (self.width, self.height),
                    "format": "RGB888"
                }
            )

            self.camera.configure(configuration)
            self.camera.start()

            self.running = True
            self.available = True
            self.error = None

        except Exception as error:

            self.available = False
            self.running = False
            self.error = str(error)

            if self.camera is not None:
                try:
                    self.camera.close()
                except Exception:
                    pass

            self.camera = None
            raise RuntimeError(
                f"Could not initialise Steven's camera: {error}"
            ) from error

    def get_frame(self):

        if not self.running or not self.available:
            return None

        try:
            with self.lock:

                frame = self.camera.capture_array()

                success, encoded_frame = self.cv2.imencode(
                    ".jpg",
                    frame,
                    [self.cv2.IMWRITE_JPEG_QUALITY, 80]
                )

                if not success:
                    return None

                return encoded_frame.tobytes()

        except Exception as error:
            self.error = str(error)
            return None

    def generate_frames(self):

        frame_interval = 1 / self.fps

        while self.running and self.available:

            start_time = time.monotonic()
            frame = self.get_frame()

            if frame is not None:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + frame
                    + b"\r\n"
                )

            elapsed = time.monotonic() - start_time
            time.sleep(max(0, frame_interval - elapsed))

    def get_status(self):

        return {
            "available": self.available,
            "running": self.running,
            "resolution": f"{self.width}x{self.height}",
            "fps": self.fps,
            "error": self.error
        }

    def stop(self):

        self.running = False
        self.available = False

        if self.camera is not None:

            try:
                self.camera.stop()
                self.camera.close()

            except Exception as error:
                self.error = str(error)

            finally:
                self.camera = None
