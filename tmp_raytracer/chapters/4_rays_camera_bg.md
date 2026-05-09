# 4_rays_camera_bg

ray class
ray function p(t) = A + tB
A - ray origin
B - ray diretion
t - real number (double)


## 2 ratios (image & viewport)
- 2 different ratios
    - image (aspect) ratio - proportional r/s between widt h& height (i.e. 16:9) focusing on the shapre
    - viewport (aspect) ratio - ratio of the visible screen area

    * basically image is the acutal object, while the viewport is like the screen
        i.e. rectangle img && square viewport
        object-fit: cover => img fills entire square but with its sides cut-off
        object-fit: contain => img is visible inside square but have extra filler blank space in the viewport
        object-fit: fill => no cutoff nor filler, but img is distorted

- easier to set width, then use aspect ratio, to find height
    * MUST ensure height is at least 1 (> 1)

(refer to the viewport & image components below for better understanding)

## Components

rays shot from `"eye" (camera)` -> through the `viewport` -> to the `3D scene` (sphere) -> then rendered as an image
* rays are not shot at the image, its at the objects in 3D scene through the viewport

[ray/camera]
- ray is a starting pt + direction => moving point that starts at a specific location
- ray tracer
    - sends rays through pixels (at starting points)
    - & computes color seen in the direction of those rays

    steps:
    1. calc ray from the "eye" through the pixel
    2. determine which objects the ray intersects
    3. compute a color for the closest intersection point

[image]
- use non-square image
    => better for debugging because x & y are independent variables that will show u the error when swapped
    i.e. a square's width & height are the same so if u swapped x & y, u may not notice the error
        but if when using rectangle OR circle, u will definitely see the error
    - use 16:9 aspect ratio (image width: height)

[view-port]

- virtual view port => rays are sent from the camera through here, to the 3D scene
- it is a virtual rectangle in the 3D world, a grid of pixels

- "if pixels are spaced the same distance horiontally as they are vertically, the viewport that bounds them will have the same aspect ratio as the rendered image"
    * this means that the diff between each viewport ray (both horizontally & vertically) are the same when mapped to the image pixels
    * i.e.
        BAD:
            100x100 viewport && 150x100 image
            (smaller w)         (larger w)
        - shoot 150 rays (horizontally) => 1.5 rays per unit of space on the viewport
          shoot 100 rays (vertically) => 1 rays per unit of space on the viewport
          * (width) needed to squeeze 150 rays into 100 px img
        - a circle that is 50x50 on the viewport, will be 75x50 unit rays
            * thus the circle will look elongated on the image width
            * this takes the square *WINDOW* & paint it on a *RECTANGLE* 

        OKAY: (but low res)
            1000 x 1000 view port && 100 x 100 image
            (larger)                 (smaller)
        - less number of rays for more number of units on the viewport
            * each ray is shot every 10 units (because 1000/ 100 = 10units)
            * during final render, colour of 1 ray of every 10 units will be used
        - photo will seem low res (becoz higher res template, but low res rays)

        OKAY: (but high res)
            10 x 10 view port && 100 x 100 image
            (smaller)                 (larger)
        - more number of rays for less number of units on the viewport
            * 10 rays are shot every 1 unit of distance on viewport (because 100/ 10 = 10rays per unit)
            * during final render, colour of 10 ray colours are used for 10 img px, but representing 1 unit in viewport
        - photo will seem high res (becoz higher res rays, but low res template)

        GOOD
            100 x 100 view port && 100 x 100 image
        - viewport *unit* is *1:1* with img *px*

[3D-scene]

- the 3D space where objects are actually placed in