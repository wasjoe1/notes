# 6_shading

## 6.1 shading

use __surface normals__ to __shade__

1. what is surface normal?
2. what is shading?

surface normal - vector that is perpendicular to the surfacve at the point of intersection
* "point of intersection" - is the coordinate where a ray fired intersected with the sphere
* for sphere, outward normal is the direction of the hit point minus the sphere (`P - C`, where P is the hit point & C is the center)
* image for the earth it would be the center of the earth to you (if u are the hit point)

shading - calculate color & intensity of a pixel based on the interaction between light(ray) & a surface


### design decisions

main decisions in mind:
- unit vector or non-unit vector of rays
- which direction should surface normal vector point to? (theres 2 main ways, 180 degs difference from each)

#### unit-vector rays

##### Discussion

Context: when figuring how bright the pixel is, we use the dot product of the (`ray vector` . `surface normal vector`)

Q. do we want to use arbitrary length vectors OR normalize to unit length?

1. if unit-length ever required, then might as well do it up front once instead of over & over
    => not a strong argument tbh imo since we want to see that there are multiple existing use cases first before abstraction
2. we do require unit-vectors in several places => (refer to below)
3. using geometry instead, we can just divide by the radius instead of using square root => not very valid too since we would need to square root the radius?

- in ray tracing, we typically normalize vectors to length = 1
    - if no normalization is done, brightness of sphere will depend on how big the sphere is rather than just the angle of the light
    - dependence on size of sphere is coz of how we calculate the normal vector: `hit_point - center`
    - the ray relative to the radius's magnitude will need to be adjusted => easier to just normalzie everything to unit vector 1
        => coz we want a magnitude value out of 1.0 (relative to all other points of intersection)

note:
* dot product of parallel opposite vectors always return 1!
    => dot product formula is: |A| x |B| x cos(deg)
    => if A & B length is 1, then |dot product| <= 1
* normalizing vector is expensive
    => because of expensive square root operation
    => add/ subtract/ multiply typically fast => 1-2 CPU clock cycles
    => division/ square root is iterative => 10-50 times longer (assuming 2 clock cycles, worst case = 100 clock cycles)

##### Implementation

Based on the text book:
"A common trick used for visualizing normals
is to map each component to the interval from 0 to 1,
and then map (𝑥,𝑦,𝑧) to (red,green,blue)"

breaking down the above sentence:

- "visualizing normals" - means to take the normal vector at every specific point where a ray hits the shape (sphere) & turn that vector's direction into color
    => this is what literally "shading by normal" means
    => we are using the magnitude + direction of normals and giving that shape color
    => in geometry math, it makes more sense to "visualize normals" rather than "visualize the shape"
- "map each component to the interval from 0 to 1"
    => each component refers to the 3 components (x,y ,z)
    => map from [-1. 1] for unit vectors TO [0, 1]
- "map (𝑥,𝑦,𝑧) to (red,green,blue)"
    => this is just a representation for r, g, b using the vector's values (magnitude + direction)
    => in this text book, the values remain [0, 1] & are only converted to [0, 255] at the end

(having not done math in abit, this did not make sense initially. let us proceed with implementation)

implementation:
- get the unit vector of normal
- get the hit point (not just whether we hit or not) => convert to double instead of bool
    * dont worry about negative values of t yet => just assume object is always infront of camera first
    * also assume closes hit point is the one we want (smallest t)
    * what should be a non hit? 
(compute & visualize n)

## 6.2 simplfy ray sphere intersection code

(dont see a point in simplifying; skip)

## 6.3 abstraction for hittable objects

- use abstract class "hittable" for anything a ray might hit

- class hittable
    - hit(const &ray) => have an interval tmin to tmax (ray only counts if tmin < t < tmax)

## 6.4 front face & back face

remembering the side of the face that the ray is pointing at the object

## 6.5 list of hittable objects

### composite pattern
Q. why do we need list of hittable objects? cant we just place the hittable objecst in a hittable list
like `hittable[]`

ŵo initialization: `int arr[x]`
ŵ initialization: `int arr[] = {1,2,3,4,...}`

* arrays are fixed size so they cant be changed once declared

Ans: instead of writing a complex loop to check every object, u can just call ___.hit()
    `hittable_list` handles who is closest internally whle keeping the main render loop clean

Q. hittable class is not a is-a r/s with hittable object thought
Ans: strictly speaking its true. BUT in graphics programming, we use *Composite Pattern*

*Composite Pattern*
- uniformity - (pattern's primary goal) => client code should be able to cll same method on single item (leaf) or group (composite) without checkign object type
- part-whole hierarchies => recursive structures where a complex WHOLE object is made up of PARTS (which themselves might be complext objs)
- tree structure - model assumes a recursive data structure

component - abstract base or interface that declares common methods
leaf - primitive element of the hierarchy that implements the component interface but has no children
composite - container that stores child components & implements the interface by delegating the work to its children

* in our case, the *sphere* is the *leaf*, and *hittable_list* is the *composite*

### shared pointer

```cpp
#include <memory>

using std::make_shared;
using std::shared_ptr;

std::vector<shared_ptr>
// recommended way: use make_shared
std::shared_ptr<MyStruct> ptr1 = std::make_shared<MyStuct>(10, 20);
// aleternative: explicit constructor
std::shared_ptr<MyStruct> ptr2 = new MyStuct(10, 20);
```

- both are tools for automatic MEM mgmt - auto delete objects when they are no longer used
- shared_ptr - smart pointer that utilizes reference counting
    - using raw pointers require manual deletion
    - shared pointer keeps reference count
        => every time the shared_ptr referenced value is assigned to another shared_ptr/ copied, count goes up
        => every time the shared_ptr goes out of scope (when function ends), count goes down
        => when count is 0, object is auto deleted
- `make_shared<T>(args...)` - allocates MEM for both the obj & the control block (reference count) in a single heap allocation
    - reduce MEM allocations from 2 to 1
        - using `new`,
        (1) `new T` asks the OS for memory for the object
        (2) pointer is then passed to smart pointer(shared_ptr), which it then asks the OS for MEM to hold the control block
        - using `make_shared<T>`
        (1) calculates the size of T plus the size of the control block.  immediately asks for 1 block of MEM
        * faster since only uses 1 memory allocation system call && also improves cache locality
        * control block => contains small, dynamically allocated structure in MEM that manages lifetime of the object (strong ref count, weak ref count, custom deleted, custom allocator)
    - better exception safety
        => i.e. `foo(shared_ptr<int>(new int(42)), bar())` if bar() throws exception after new int(42) is created, but b4 pointer is maanged, MEM leak can occur
    * thus better performance & exception safety compared to `new`
    * the preferred way to create the object that the smart pointer will manage

## 6.6 New cpp features

- `make_shared<T>(args...)` - returns a shared_ptr<T> => so u can just use auto
- std::vector - auto grows as more values are added
- using - tells compiler that we are getting shared_ptr & make_shared from the std library
    => we dont need to prefix with std:: every time we reference them

## 6.7 Common constants & utility functions

- only need *infinity* for now
- throw our own definition of *pi* in => used later
- include the *cpp std usings* here as well
- include *degreest_to_radius* utility functions
- include common headers
    custom header files: `color.h`, `ray.h`, `vec3.h`
    std header files: `cmath`, `iostream`, `limits`, `memory`

* these program files are included first so all other header files can implicitly assume are included

## 6.8 interval class

### contains vs surrounds

contains is inclusive => [min, max]
surrounds is exclusive => (min, max)

Q. why do we need both?

Ans:
*surrounds* is used for *hit detection*. => boundaries are not valid
    => a ray hitting exactly at the origin would __pass__ `contains` (t = 0), but __fails__ `surrounds`
    => we dont want to use contains to avoid __shadow acne__
*contains* is used when boundaries are valid
    => i.e. clamping intensity of RGB values (i.e. RGB values are between [0,1])
