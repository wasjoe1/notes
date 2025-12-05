#!/usr/bin/env python3

class parent():
    class_var = "class_var_val"
    def __init__(self):
        self.instance_var = "instance_var_val"
    
    def scream_class_var(self):
        print("im the parent")
        print("class variable: ", parent.class_var)
    
    def scream_instance_var(self):
        print("im the parent")
        print("instance variable: ", self.instance_var)

class child(parent):
    # good practice to include the initialization of the parent so that any variables
    # that the parent use can be used in the child
    def __init__(self,):
        super().__init__() # init parent

    # this will throw an error as the parent is not initialized
    # & there wil be no instance variable when calling "super().scream_instance_var()"
    # def __init__(self,):
    #     pass

    def scream_class_var(self):
        print("parent will be screaming ...")
        super().scream_class_var()
        print("im the child & i overrided the parent")
    
    def scream_instance_var(self):
        print("parent will be screaming ...")
        super().scream_instance_var()
        print("im the child & i overrided the parent")

def main():
    bby = child()
    bby.scream_class_var()
    bby.scream_instance_var()

if __name__ == "__main__":
    main()