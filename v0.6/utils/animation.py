"""
Animation utility class
"""


class Animation:
    """Handles frame-based animations"""

    def __init__(self, frames, frame_duration):
        """
        Args:
            frames: List of frame data
            frame_duration: Number of game ticks per frame
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.timer = 0

    def update(self):
        """Update animation, advance to next frame if needed"""
        self.timer += 1
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_frame(self):
        """Get current frame data"""
        return self.frames[self.current_frame]

    def reset(self):
        """Reset animation to first frame"""
        self.current_frame = 0
        self.timer = 0

    def set_frame(self, frame_index):
        """Jump to specific frame"""
        self.current_frame = frame_index % len(self.frames)
        self.timer = 0
