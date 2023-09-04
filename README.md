# Planar Truss Analysis
Before transitioning to a career in Computer Science, I pursued my studies as a third-year Civil Engineering student. During this time, I constantly pondered how I could leverage my coding skills within the realm of my academic pursuits, seeking to create something valuable not only for myself but also for fellow students. One particular structural aspect that captivated my interest was the truss.

As the culmination of my coursework in the CS50 and CS50P courses on EdX, I embarked on a project to develop a Python-based 2D Truss Analysis program. This software is designed to comprehensively analyze truss structures, providing insights into support reactions, node displacements, and even presenting a visual representation of the deformed structure.

I firmly believe that this tool will prove invaluable to second and third-year Civil Engineering students enrolled in Structural Analysis courses. It will assist them in validating their manual calculations, fostering a deeper understanding of the subject matter.

This repository serves as a centralized hub housing all the project's implementation files.

## What is a truss ?
![A bridge using a truss as base structure to supports loads.](/images/RRTrussBridgeSideView.jpg)

To understand the functionality of this program, it's essential to grasp the concept of a truss. A truss is essentially an assembly of structural members, typically beams, interconnected at nodes, forming a stable framework. In simpler terms, trusses consist of bars arranged within a two-dimensional Cartesian system. They are a prevalent structural element found in applications such as steel buildings and bridges, including examples like railway bridges and transmission towers.

Trusses can exist in two primary forms: as 2D trusses, entirely confined to a single plane, or as 3D trusses, which extend into three-dimensional space. Specifically, when all the truss members and applied loads are situated within a single plane, we refer to it as a plane truss.

## What are the components of the truss?
A truss fundamental components are: 
- The **nodes or joints**, where the loads and support reactions are applied.
- The **members or beams**, which are connected only at their ends by frictionless hinges in plane trusses 
and by frictionless ball-and-socket joints in space trusses. In a truss, they are subjected only to axial 
forces (compression or tension).

## Computational requirements:
* Prior to undertaking any computations, it's imperative to evaluate the internal stability of a truss. This evaluation ensures that the truss, when detached from its supports, maintains its shape and remains a structurally rigid entity. In this context, 'internal' pertains to the count and configuration of the members intrinsic to the truss itself.

It's worth noting that instability resulting from inadequate external support or incorrect placement of external supports is termed 'external instability.

> [!NOTE]
> The internal stability of a determinate plane truss is assessed by this equation :
> **m + r = 2j** 

Where :   
- **m** : number of members or beams
- **r** : number of support reactions
- **j** : number of nodes or joints

> [!NOTE]
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

In this program, we employ the Stiffness Method, specifically the displacement method, to conduct truss analysis.

The Stiffness Method necessitates breaking down the structure into discrete finite elements and designating their endpoints as nodes. In the context of truss analysis, these finite elements correspond to individual truss members, while the nodes signify the joints or connections. We determine the force-displacement characteristics of each element and subsequently interrelate them through the force equilibrium equations established at the nodes. These interconnected relationships are then consolidated into what is referred to as the structure's **stiffness matrix**, denoted as ***K**.

Once the stiffness matrix is defined, we can ascertain the unknown displacements of the nodes under any given load applied to the structure. With knowledge of these displacements, we can subsequently compute both the external and internal forces within the structure by leveraging the force-displacement relations for each individual member.
