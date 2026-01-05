
import re

# Sample input string
input_string = """

                                    // Get the proxied playback URL
                                    engine.getProxiedUrl("https://si.videoapne.to/bdohxn4p7bboxuzvta474gkxtfyg5xmxxuv6gu7mu46gqsrke
nnd2qvdyfgq/v.mp4").then((url) => {
                                        var player = jwplayer("video_player").setup({
                                        file: url,  // Replace with your actual MP4 file URL
                                        image: "https://si.videoapne.to/i/01/00021/d6w9264w0i6h.jpg", // Poster image for the playe
r
                                        autostart: false, // Enable autoplay
                                        mute: false, // Ensure the video is not muted by default
                                        width: "100%",  // Player width is 100% of the container
                                        height: "480px", // Set fixed height to 480px
                                        aspectratio: "16:9", // Ensures the video maintains a 16:9 aspect ratio
                                        cast: {
                                            autohide: false, // Hide the cast button when casting is not available
                                            button: true // Display the cast button
                                        },
                                        controls: true, // Ensure controls are visible
                                        responsive: true, // Makes the player responsive
                                        skin: "skin1", // Optional: Custom skin
                                        playbackRateControls: true, // Optional: Add playback rate controls
                                        stretching: 'uniform' // Ensures video maintains its aspect ratio
                                        });

"""

# Regular expression to find 'token' key and extract its value
pattern = r'\"(https?://[^\"]+)\"'
match = re.search(pattern, input_string)

# Check if a match is found and extract the token
if match:
    token = match.group(1)  # Extract the token value
    print(f"Extracted token: {token}")  # Print the token
else:
    print("Token not found.")
