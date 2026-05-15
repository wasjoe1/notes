# 10_metal

## 10.1: abstract class for materials

for objects to have different materials, can do either
1. type
2. abstract class

* in this book, we go with *abstract class*

### example of both

```cpp
// 1.type: single class containing ALL possible material types & properties
struct UniversalMaterial {
    enum MaterialType { LAMBERTIAN, METAL, DIELECTRIC, EMISSIVE };
    MaterialType type;

    // Base properties (Used by almost everything)
    Color albedo;
    
    // Metal properties (Ignored by glass/matte)
    double roughness;
    double metallic;

    // Glass/Dielectric properties (Ignored by metal/matte)
    double refraction_index;
    Color transmittance;

    // Light source properties (Ignored by non-emitters)
    Color emission_color;
    double emission_intensity;
};

// 2. abstract class: abstract class that new materials can inherit
// PARENT material class
class Material {
public:
    virtual ~Material() = default;

    // The two critical actions a ray tracing material must perform:
    virtual bool scatter(
        const Ray& ray_in, const HitRecord& rec, Color& attenuation, Ray& scattered
    ) const = 0;
};

// CHILD class: matte/diffuse surfaces
class Lambertian : public Material {
public:
    Lambertian(const Color& albedo) : albedo(albedo) {}

    bool scatter(const Ray& ray_in, const HitRecord& rec, Color& attenuation, Ray& scattered) const override {
        Vector3 scatter_direction = rec.normal + random_unit_vector();
        scattered = Ray(rec.p, scatter_direction);
        attenuation = albedo;
        return true;
    }
private:
    Color albedo;
};
```

### how they work

- for 1, type is set to specific material i.e. `type = METAL` then program runs switch statement to decide variables to use or ignore
    - example usage: (can see forgetting to init a field is a problem)
        ```cpp
        // Create a Matte Red Plastic Sphere
        UniversalMaterial red_plastic;
        red_plastic.type = UniversalMaterial::LAMBERTIAN;
        red_plastic.albedo = Color(0.9, 0.1, 0.1);
        // (roughness, metallic, and refraction_index are ignored)

        // Create a Shiny Gold Metallic Sphere
        UniversalMaterial gold_metal;
        gold_metal.type = UniversalMaterial::METAL;
        gold_metal.albedo = Color(1.0, 0.84, 0.0);
        gold_metal.metallic = 1.0;
        gold_metal.roughness = 0.1;
        // (refraction_index is ignored)
        ```
    - soln1: use good default values that are okay for every type
    - soln2: factory pattern, have 

- for 2, compiler only knows pointer `Material* ptr` & calls `.scatter()` on the material

## 10.2: Data structure to describe ray-object intersections

* this sub-chapter discusses
    (1) "use arguments" vs "encapsulated type" for hit_record
    (2) addition of material into hittable class & hit_record

### "use arguments" vs "encapsulated type" for hit_record

"encapsulated type" - use a class/ struct to store all the variables that we want to use in a function later

```cpp
// Encapsulated Type
struct HitRecord {
    Point3 p;          // Exact 3D coordinates of the hit
    Vector3 normal;    // Surface normal vector at the hit point
    double t;          // Distance along the ray line
    bool front_face;   // Whether the ray hit the outside or inside
};

// example function using HitRecord
bool scatter(const Ray& ray_in, const HitRecord& rec, Color& attenuation, Ray& scattered) {
    // Access data via the container
    Vector3 my_normal = rec.normal;
    Point3 hit_point = rec.p;
    // ... other logic ...
}
```

"use arguments" - pass every parameter line by line into a function

```cpp
// Function with arguments of "data struct"
bool scatter(
    const Ray& ray_in, 
    const Point3& hit_point,    // Extracted out of HitRecord
    const Vector3& normal,      // Extracted out of HitRecord
    double t,                   // Extracted out of HitRecord
    bool front_face,            // Extracted out of HitRecord
    Color& attenuation, 
    Ray& scattered
) {
    // Access data directly from the input arguments
    Vector3 my_normal = normal;
    Point3 my_p = hit_point;
    // ... other logic ...
}
```

* ultimately matter of taste - "encapsulated type" might incur tiny performance cost due to construct/ copy ops, BUT is more readable
                            vs "use args" have 0 overhead where values can be passed directly via registers, BUT is less readable

## 10.3: modeling light scatter & reflectance

- albedo - fractional reflectance
    => vary with material color
    => vary with incident viewing direction (direction of incoming ray)

- Lambertian (diffuse) reflectance
    - can either always scatter & attenuate light according to its reflectance R
    - OR sometimes scatter with (probability 1-R) with no attenuation
    - OR can be mixture of both?
    * in our case, wwe choose to always scatter

- 0 direction vector
    - if random unit vector generated is opposite of normal unit vector, they will cancel each other out & create a 0 direction unit vector
    - this leads to bad scenarios later (in `hit()` of `sphere.h`, when calculating discriminant, we have potential of calculating 0 / 0; infinities & NaNs)
    - need to ignore these vectors => text book just replaces them with normal unit vector

glossary:
* scatter - physical behavior of a light ray (0 scatter means ray stops & dies; scatter is either yes or no; binary)
* attenuation - mean how much the light is absorbed or scattered away when interacting with a surface (0 attenuation means all light absorbed so object is just black)

## 10.4: mirrored light reflection

* essentially create polished metals class that reflects ray perfectly on the surface

## 10.5: scene with metal spheres

* create more spheres of different materials (metal/ reflective & lambertian/ matte materials)

## 10.fuzzy reflection

* add a fuzz factor, that pushes the reflected ray by a bit
    => this mimics rougher surfaces that do not have exact reflection
    => higher the deflection, the "rougher" the surface

* with heigh fuzziness, a real photon would hit the side wall of a tiny crack on the metal surface & get trapped
    hence the implementation is:
    `return (dot(scattered.direction(), rec.normal) > 0);`
    when the scatter and normal direction are in the same direction function returns false
    this is when the reflected ray and normal are in opposite directions
    we dont want to just invert the reflected ray but we are going to absorb the ray (trapped inside the metal)