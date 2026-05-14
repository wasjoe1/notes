# 8_antialiasing

## understanding geometry context

- aliasing (issue) - harsh "stair step" or "jaggies" at edges
    => typically when camera takes pic, there usually isnt jaggies along edges
    => because edge pixels are blend of some foreground + some background
    * foreground - part of a scene that appears nearest to the viewer

- anti-aliasing (soln) - filters / technique applied to the image to reduce hard pixelatin on curves & diagonals
    by blending edge pixels with the background

- (current) currently we are doing "point sampling"
    => single ray through the center of each pixel
    => issue: its too distinct
    i.e. checkerboard far away with 4 rays on an 8x8 black & white grid
        rays might intersect only white OR black tiles OR odd combination
        in real life thought, we see a gray board

- (todo/ done) need to sample the light falling around the pixel, then integrate those samples to approx. the true continuous result
    - how? sample square region centered at the pixel that extends halfway to each of the 4 neighbouring pixels
    - within that square region now, we will shoot __random rays__ => need a random function
    
    * sample - a ray shot from the camera
        => in anti-aliasing, multiple samples are used to represent a pixel

* essentially, sample miltiple points within the pixel's square region & get the average of those sampled points

## implementation

- (random double) genereating random double number => need `double get_random()`
    <cstdlib> is the legacy C method of creating it
    - implemented as a very simple linear congruential generator (LCG)
    - lower bits of LCG are highly predictable & repeat quickly
    - uses RAND_MAX => `std::rand()` returns a value between 0 to & RAND_MAX(32_767)

    <random> is the canonical cpp way to handle random numbers
    - uses std::mt19937 (mersenne twister engine) => period length 2^19937 - 1 before sequence ever repeats
    - avoids using RAND_MAX => capped at 32_767 (very small)
        => sphere scatter paths become highly digitized & lack fine precision

- (sampling points) need to write pixel color by *averaging* multiple samples colors
    => clamp => to ensure value within [0, 1] => actually wouldnt all values be within [0,1] though?

- () why clamp [0.0, 0.999]? `static const interval intensity(0.000, 0.999);`
    => prevent off-by-one array indexing or truncation??
    => integer truncation - truncates the decimal portion completely (not rounding! just removal of decimal points)
    => noteiced that its coz the later implenentation used 256 instead of 255, so we set to 0.999 instead of 1