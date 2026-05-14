# 9_diffuse_materials

## geometry understanding

### 9.1 simple diffuse material
- diffuse materials (aka matte) - non-shiny, matte surface
    - scateers incoming light evenly in all directions regardless of *angle of incidence*

- 2 ways to display *geometry* & *materials*
    1. decouple <= we go with this
        - allow assignment of different multiple materials to spheres & vice versa
    2. couple
        - allows procedural objects

- diffuse objects
    - dont emit their own light, take color of surrounding BUT modulate it with their own color
    - light reflected off diffuse surface has random direction
    - light can also be absorbed
        => darker surface absorb more light (hence darker)

- intuitive material
    - light bounces ray off in all directions equally

- random vector generation (concept)
    - there are analytical methods to do this, but we are using a straight forward method below
    - need to manipulate random vector to only get results on the surface of a hemisphere
        => use algo: *rejection method*
        => repeatedly generate random samples until we produce a valid sample (within criteria)
            (reject bad samples until valid 1 is found)

- random vector generation (implementation)
    0. have a unit sphere around the point of intersection
    1. generate random vector inside unit sphere
    2. normalize this vector to extend it to the sphere surface
    3. invert normalized vector if it falls on the wrong hemisphere
        => use fot produt against surface normal (+ve is valid, -ve need to invert)

- random vector generation: *floating point abstraction leak*
    - floating point numbers have finite precision
    - very small value can cause __underflow to 0__ when __squared__
        => when normalizing vector, we need to find length of vector via __square operation__
        => for floating point numbers in cpp: *(+-)vector / 0.0 == (+-)infinity* (for ints it will crash)
                                              *0.0 / 0.0 == nan* 

### 9.2 limit number of child rays

* ensures ray_color doesnt recursively call infinitely when there are multiple surfaces trapping the ray

### 9.3 fix shadow acne

* thing is when we calculate intersection point of ray & the surface, theres potential for rounding errors
    - this cause some ray intersections to be above / *below* the surface
    - if its below, the reflected ray might re-intersect with the surface causing *shadow acne*
        => for bounce ray(our book): effect is color darkens
            - recursive path tracer => secondary rays scatter to collect ambient bounce light
            - material absorbs half the light energy at each bounce (coz of color * 0.5 => "higher color" means darker/ close to black)
            - ray gets trapped in infinite loop of colliding with itesel until value drops to 0
        => for shadow ray: lights are bounced off surface & reflected into camera, this means light bounced back into sphere & is 100% in shadow from the light source

### 9.4 True lambertian reflection

* make scattering more "real"

- in reality, rays are scattered nearer to the surface normal than being evenly distributed
- create this distribution by shifting sphere to the "top" of the surface (its the tangent unit sphere on the outside of the sphere (P + n))
    then get a random point in that sphere (notice how the points WILL be closer to the surface normal vector)
- will get a similar image with differences:
    1. shadows are more pronounced, material slightly darker
        => more rays scattered towards normal since less light bounce back to camera;
        => for shadows, more light bounce straight up which is not towards the camera, hence area underneath the sphere is darker
    2. spheres are tinted blue from the sky after change
        => more rays are shot directly into background (blue) hence more blue


### 9.5 Gamma correction for accurate color intensity

* make our color accurate

- now our image at 50% appears too dark (when comparing 100% and 0%, its not the expected midway darkness)
- why?
    - current render programs assume "gamma corrected" image
    - but our image is currently in the linear space
- need to transform our image to gamma space

* just need to know to transform our image to gamma sapce because its good

### others

glossary terms:
- angle of incidence - "angle from which the light hits it" there should be a term for this angle right?
    => formally: angle between incoming light ray & the surface normal
- hemisphere - 1 half of a sphere
- surface normal - vector normal to the surface; in sphere: vector representing direction from center of sphere to current point on the surface
- random normalized unit vector - this is created from the point of hit on the hemisphere (to be used to compared against the surface normal)