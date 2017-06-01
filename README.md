Title: ABabe

# Introduction
ABabe is a library with some uitils to deal grid site
 structures.

# Installation
1. From source

    ::: console
    $ cd ABabe
    $ pip install .
    $ pip install -U .

# How to use

1. grid generator with no duplicate structure

    ::: yaml
    # lattice shape of grid
    # triflat for plant triangle grid
    lattice: triflat
    
    # base is the element of full padding grid
    base: B
    
    # grid size -- seq are depth width lenght
    grid_size: [1, 4, 4]
    
    # speckle -- the element of filled site
    speckle: G
    
    # how many site are filled with speckle
    number: 3
    
    # the output filetype
    output: normal
    
    # ON or OFF the is_speckle_disjunct restriction
    restriction: True

    ::: console
    python utils/grid_gen.py -f setting.yaml





All new features; ml; and documentations are in the 
nightly branch which hiden from public shallowly.
All devel should first be merge to the nightly, and 
then to master when technically and authorized allowed.

1. bcc as primitive cell

a bcc of a conventional cell can be transformed to the
one atom primitive cell by Rotation matrix P:
P = -0.5 -0.5  0.5
    -0.5  0.5 -0.5
    -0.5  0.5  0.5



2. algorithom of the sites ordered generator.

function site_ordered_generator:
    input: a generator of repeated cstructures
    output: a generator of non-repeated cstructures

    set_isostructure = set()
    for cstru in gen_repeat_cstru:
        if cstru not in set_isostructure:
            yield cstru
            append cstru's isostructure into set_isostructure

function update_set_isostru:
    input: a cstru; the present set_isostructure; parent's ops
    output: a new set_isostructure

    cstru to a cell cell_cstru
    cell_cstru transform to all isostructure by its parent structure's ops
    isostructures_cstru should be a set now

    join the isostructure_cstru and set_isostructure to new_set_isostructure

## TODO
    Periodic strucutres distinguish. 6x6 triangle gird, with no double-atoms
    connected.
