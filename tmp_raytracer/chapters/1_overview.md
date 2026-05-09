# Overview

## why ray tracing?
- write all code => helps with cpp familiarisation (i am using this project to learn cpp concepts & get familiar with cpp syntax)
- no use of external API (get familiar with std lib abilities)

## indirect lighting
indirect lighting - light that reaches an object after bouncing off 1 or another surface

## ray tracer (concept) :> path tracer (implementation)
- ray tracer in this context is a path tracer
    => ray tracer - rendering system that calculates an image by athematically simulating the path of light as it interacts with virtual objects
    => most basically, shoot rays from a virtual camera into a 3D scene to see what it ssuppose to see
        => (backward ray tracing) shooting rays from camera
        => (forward ray tracing) shoot rays from sun & use camera to pick it up
        * seems counter-intuitive but we use backward ray tracing => dont really do forward coz we are not interested in photons that dont reach camera anyways (wasted calculations)

- author specifies that we building a path tracer
- path tracer vs generic ray tracer
    - path tracer uses single algo for the entire rendering process (shadows, reflections & lighting)
    - is the closes digital approximation to actual light

## why cpp
- fast, portable & most production movie & video game renderes are written in cpp
- most modern cpp features are avoided
- inheritance & opereator overloading are useful

## providing code
- author initially didnt provide code online
- but decided to do so later on coz of subtle errors; helpful to compare code

## philosophies
- implement concepts
- cpp in a C-like manner => future books also uses this for continuity
- 96 chars per line => i will follow this for the project, though if i do find enough
    motivation (& interest) to make this project better aside from just being a tutorial,
    i might consider using 80 characters to align with google's cpp styling guide

## project structure
books/ - 3 books
images/ - contains cimages & figures of the books => can use to compare to my results
style/ - css for books & site
src/ -
src/<books> - final source code for each book