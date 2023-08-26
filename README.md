# 2D_Truss_Analysis
As a Final Project of the following CS50 and CS50P courses on EdX, I decided to implement 
a 2D Truss Analysis program in python. This repository regroups all the files of the project's 
implementation.

## What is a truss ?
![A bridge using a truss as base structure to supports loads.](/images/RRTrussBridgeSideView.jpg)

To know what this program is doing, first we need to know what is a **Truss**. A truss is an assembly 
of members such as beams, connected by nodes, that creates a rigid structure. In other words, they 
are basically bars oriented in two dimensional cartesian systems. Trusses are very common type of 
structures used in steel buildings and bridges. Eg. Railway bridges, transmission towers. These could 
be entirely entirely in a plane – 2D trusses trusses or spatial spatial – 3D trusses. Specially, if 
all the members of a truss and the applied loads lie in a single plane, the truss is called a _plane truss_.

## What are the components of the truss?
A truss fundamental components are: 
- The **nodes or joints**, where the loads and support reactions are applied.
- The **members or beams**, which are connected only at their ends by frictionless hinges in plane trusses 
and by frictionless ball-and-socket joints in space trusses. In a truss, they are subjected only to axial 
forces (compression or tension).

## Computational requirements:
* Before any computation, the internal stability of a truss must be assessed. Meaning that the number and 
geometric arrangement of its members is such that the truss does not change its shape and remains a rigid 
body when detached from the supports. The term _internal_ is used here to refer to the number and arrangement 
of members contained within the truss. The instability due to insufficient external supports or due to improper 
arrangement of external supports is referred to as _external_.

> The internal stability of a determinate plane truss is assessed by this equation :
> **m + r = 2j** 

Where :   
- **m** : number of members or beams
- **r** : number of support reactions
- **j** : number of nodes or joints

> **m + r > 2j** is also stable, but is considered ***statically indeterminate***, case which will not be treated by 
our program.

* We consider a truss to be *statically determinate if the forces in all its members, as well as all the external 
reactions, can be determined by using the equations of equilibrium*.

## Equations of Condition for Plane Truss
The types of connections used to connect rigid portions of internally unstable structures 
provide equations of condition that, along with the three equilibrium equations, can be 
used to determine the reactions needed to constrain such structures fully. Such equations 
are :
- Because an internal hinge cannot transmit moment, it provides an equation of condition :
    + $\sum{M} = 0$, which is the sum of the moments in all nodes.
- Since these parallel (horizontal) bars cannot transmit force in the direction perpendicular 
to them, this type of connection provides an equation of condition:
    + $\sum{F} = 0$, which is the sum of forces in each nodes.

## Method of Computation
In this program, we use the **Stiffness Method**, more precisely the **displacement method** to 
analyze the truss. 

Application of the stiffness method requires subdividing the structure into a series of discrete 
finite elements and identifying their end points as nodes. For truss analysis, the finite elements 
are represented by each of the members that compose the truss, and the nodes represent the joints.
The force-displacement properties of each element are determined and then related to one another 
using the force equilibrium equations written at the nodes. These relationships, for the entire 
structure, are then grouped together into what is called the structure *stiffness matrix ***K****.

Once it is established, the unknown displacements of the nodes can then be determined for any given 
loading on the structure. When these displacements are known, the external and internal forces in 
the structure can be calculated using the force-displacement relations for each member.
