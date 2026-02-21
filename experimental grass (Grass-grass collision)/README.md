----------------------------------------------------------DYNAMIC GRASS (FABRIK-like Implementation)------------------------------------------------------------------
                                                                    Grass-to-grass collision
                                                                    
After 2 years of competitive programming, I wanted to explore real-time simulation and physics-based animation using PyGame again. This is my 11th small project, not perfect, but I’m starting to see progress in building interactive systems.

Core idea:
    - Use FABRIK for spacing from root to tip
    - Use FABRIK for spacing from tip to player when in range
    - Use Hooke's law to snap the blades back to its origin when player isnt in range
    - SHM to create swaying motion for grass blades

Why the chunks?:
    - I did not want the program to constantly check for collision on every chunks so we check individually on each chunks

    - O(checking_local_blades^2 + Chunks*Local_baldes)

    - For this version, I made blade to blade collision -> checking_local_blades^2

    - The reason why I did not cover the whole 3x3 area is that when a blade is created, it would get automatically snapped to the bottom edge of its current chunk
    - Therefore no need for 3x3, we only need to check the current chunk and its left/right adjacent chunks

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
    - Only check current chunk and its left/right adjacents