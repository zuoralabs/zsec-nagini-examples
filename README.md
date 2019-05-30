# Examples for using Nagini

Nagini examples, showing some common use cases, such as proving post conditions for for-loops.
See also the official Nagini examples.


# Setup tips

Installation on Linux and Windows is covered in the official Nagini README.
For installation on Mac, follow the same steps as installation for Linux, except
you need to set some env vars when using pip:
~~~
export MACOSX_DEPLOYMENT_TARGET=10.14
CFLAGS=-stdlib=libc++ pip install nagini
~~~
Modify the deployment target as necessary.
(see [ref](https://stackoverflow.com/questions/53033202/cvxpy-stlibc-installation-error-on-macos-mojave))


## PyCharm plugin and Nagini Server

You can improve speed and debug crashes using a Nagini server.

1. Make a "nagini directory" containing the following:
   - `src/`
   - `src/nagini_translation` that links to `nagini_translation` under your python environment's `site-packages`
   - `src/nagini_contracts` that links to `nagini_contracts` under your python environment's `site-packages`

2. The Nagini settings in PyCharm, set the nagini path to the "nagini directory" you just created.
   Also set the path to `silicon.jar` to the one in `nagini_translation`. For example:
   ~~~
   <env>/lib/python3.7/site-packages/nagini_translation/resources/backends/silicon.jar
   ~~~
   
3. Also under Nagini settings, check the box to use a Nagini server.
    
4. Run the Nagini server. It's useful to run it under ipython[^1], so you can debug it
   when it crashes. 
   ~~~
   ipython -i -- $(which nagini) --server file_to_verify.py
   ~~~
   You will need to restart the server after each crash.
   
[^1]: install via pip if you don't have it. To debug crashes, type %debug.
   
Note that if you crash Nagini, the plugin may say that verification was successful. I have
observed Nagini crashing when contracts have the wrong number arguments. It has also crashed on `int()` because
it expects `int` to have an argument.
