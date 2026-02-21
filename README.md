# Dynamic-Grass-FABRIK-like-implementation
Dynamic Grass (FABRIK-like Implementation)
I made both with grass-to-grass collision version/ without grass-to-grass collision for performance and visual comparison
After 2 years of competitive programming, I wanted to explore real-time simulation and physics-based animation using PyGame again.
This is my 11th small project, not perfect, but I’m starting to see progress in building interactive systems.

Update 0.1:
- Fixed grass flipped upside down
- More variation (thickness, height, grass color)

Update 0.2:
    Bug fixes:
    - fixed jittering
    - fixed blades flipping over
    New features:
    - added mouse pointer indicator
    - added bottom edge snapping
    - added adding + delete grass blades
    - added chunk visualization
    - added pseudo wind

Update 0.3:
    Optimization:
    - Only check the current chunk and its left/right adjacents
    - Limited blades-per-chunk to 50
    - Created both versions in separate folders for reference (I had both uploaded in this repository, so you can check them out)

Complexity:
- with grass-to-grass collision: O(local * local + chunks * local)
- without grass-to-grass collision: O(local + chunks * local)
