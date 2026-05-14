# 7_moving_camera_code

- move scene-render code into `camera` class
- responsible for 2 things:
    1. construct & dispatch rays into the world
    2. use results of rays to construct rendered image

- camera will be default constructed
- public variables modified via assignment
- then initialized via `initialize()`

public methods:
`initialize()`
`render()`

private methods:
`get_ray()`
`ray_colour()`

main() function:
- creates a camera & sets default values
- calls render()
    => preps camera for rendering & excute render loop
    * render() calls initialize() internally

* NOTE:
public members allow users to customize the image width & aspect ratio
private members allow initialize() to be called internally as data set can be shared with the render() public method
