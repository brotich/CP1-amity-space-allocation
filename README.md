# CP1-amity-space-allocation
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f8d08f57520f495db9ac118809c63ee8)](https://www.codacy.com/app/brian-rotich/CP1-amity-space-allocation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-brotich/CP1-amity-space-allocation&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/f8d08f57520f495db9ac118809c63ee8)](https://www.codacy.com/app/brian-rotich/CP1-amity-space-allocation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-brotich/CP1-amity-space-allocation&amp;utm_campaign=Badge_Coverage) 
[![Build Status](https://travis-ci.org/andela-brotich/CP1-amity-space-allocation.svg?branch=develop)](https://travis-ci.org/andela-brotich/CP1-amity-space-allocation)

## Introduction

A Simple Python CLI that allocates persons `staff` or `fellow` to `Offices` and/or `Living Space` available at `Amity` facility

### features
* create and allocate `Offices` and `Living Space`
* create and allocate `Fellows` and `Staff` members
* print allocations to stdout. (optionally save to filename)
* print unallocated persons. (optionally save to filename)
* relocate a person to another room
* print persons allocated to a particular room

## Setting Up

Reccomended python version `python 2.7.12`. The program has limitted support `python 3` (untested)

* Make a folder in home dir:
		
		$ mkdir ~/work-dir
		$ cd ~/work-dir

* Clone this repo:

 		$ git clone https://github.com/andela-brotich/CP1-amity-space-allocation.git
 		$ cd ~/CP1-amity-space-allocation

* (Optional) Create and activate a virtual enviroment
		
		$ virtualenv venv --python=python2
		$ . venv/bin/activate

* Install project requirements

		pip install -r requirements.txt


* Launch the app using

		(venv)$ python run -i

## Commands available for Interactive mode
Below is a description of command available in the interative mode. Type `help` at anytime to list all commands or `<command> help` for usage on a single `command`

*  `create_room <room_type> <room_name>...`

    This create a room or a list of rooms where `room_type` can either be `office` or
 `living`.
   Example usage:
   
   		(amity) create_room office carmelot
		Created OFFICE rooms: carmelot
		(amity) create_room living shell
		Created LIVING rooms: shell

* `add_person <first_name> <last_name> <role> [<wants_accommodation>]`

  create a new person of role either `staff` or `fellow` and allocate to a random room: i.e `staff` is allocated `office` while `fellow` is allocate `office` and optionally a living space if requested

  Example usage:
  
	 	(amity) add_person Brian test Fellow 
	 	Fellow Brian test created successfully
	 	allocated office space at carmelot 
	 	
	 	(amity) add_person Brian test Fellow 
		Fellow Brian test created successfully
		allocated office space at carmelot
		
		(amity) add_person Shem Rodgers Fellow y 
		Fellow Shem Rodgers created successfully
		allocated office space at carmelot 
		allocated living space at shell

* `reallocate_person <person_id> <new_room_name>`

   Move a person with `person_id` to `new_room_name`.
   
   Constraints: 
   - can only move allocate person to room of same type i.e office to office and living space to living space
   - the new room should have atleast one vacant space
   - staff cannot be relocated to living spaces
   
 
  Example Usage:
  
  		(amity) reallocate_person FL001 valhalla
		 FL001 relocated from carmelot to valhalla
  
* `load_people <file_name>`

    add people to the program by reading a txt file as shown in the sample
 
    
    Sample file `data.txt`
    
		    OLUWAFEMI SULE FELLOW Y
		    DOMINIC WALTERS STAFF
		    SIMON PATTERSON FELLOW Y
		    MARI LAWRENCE FELLOW Y
		    LEIGH RILEY STAFF
		    TANA LOPEZ FELLOW Y
		    
   Example usage:
   
		   (amity) load_people data.txt
		    Loaded Persons
		    |    | ID    | NAME            | ROLE   | ACCOMM.   |
		    |----+-------+-----------------+--------+-----------|
		    |  1 | FL003 | TANA LOPEZ      | Fellow | Y         |
		    |  2 | ST001 | LEIGH RILEY     | Staff  | ----      |
		    |  3 | FL004 | MARI LAWRENCE   | Fellow | Y         |
		    |  4 | FL005 | SIMON PATTERSON | Fellow | Y         |
		    |  5 | ST002 | DOMINIC WALTERS | Staff  | ----      |
		    |  6 | FL006 | OLUWAFEMI SULE  | Fellow | Y         |
		    
* `print_allocations [<file_name>]`

    Prints a list of current person allocated in the rooms. (optional) `file_name` writes the data to the file 

    Example usage
    
	    (amity) print_allocations 
		Offices
		    carmelot
		        | ID    | NAME            | ROLE   |
		        |-------+-----------------+--------|
		        | FL002 | Shem Rodgers    | Fellow |
		        | FL003 | TANA LOPEZ      | Fellow |
		        | FL005 | SIMON PATTERSON | Fellow |
		        | ST002 | DOMINIC WALTERS | Staff  |
		        | FL006 | OLUWAFEMI SULE  | Fellow |
		    valhalla
		        | ID    | NAME          | ROLE   |
		        |-------+---------------+--------|
		        | FL001 | Brian test    | Fellow |
		        | ST001 | LEIGH RILEY   | Staff  |
		        | FL004 | MARI LAWRENCE | Fellow |
		Living Spaces
		    shell
		        | ID    | NAME            | ROLE   |
		        |-------+-----------------+--------|
		        | FL002 | Shem Rodgers    | Fellow |
		        | FL003 | TANA LOPEZ      | Fellow |
		        | FL004 | MARI LAWRENCE   | Fellow |
		        | FL005 | SIMON PATTERSON | Fellow |


* ` print_unallocated [file_name]`

   print a list of unallocated persons to the screen (optional) `file_name` writes the data to the file

  Sample Usage

    		(amity) print_unallocated save.txt
			Unallocated Persons
			    1. Staff
			        All Staff Allocated
			    2. Fellows
			        |    | ID    | NAME           | OFFICE   | LIVING SPACE   |
			        |----+-------+----------------+----------+----------------|
			        |  1 | FL006 | OLUWAFEMI SULE | carmelot | ---            |
			        |  2 | FL001 | Brian test     | valhalla | ---            |
			Successfully wrote data to /Users/brianrotich/andela/checkpoint/CP1-amity-space-allocation/save.txt

* `print_room <room_name>`

   Prints the names of occupants in`room_name` on the screen.
   
   Example Usage
   
		   (amity) print_room shell
		    Room: SHELL(Living Space)
		      Occupants: 
		      |    | ID    | NAME            | ROLE   |
		      |----+-------+-----------------+--------|
		      |  1 | FL002 | Shem Rodgers    | Fellow |
		      |  2 | FL003 | TANA LOPEZ      | Fellow |
		      |  3 | FL004 | MARI LAWRENCE   | Fellow |
		      |  4 | FL005 | SIMON PATTERSON | Fellow |
   
* `save_state [sqlite_database]`

    Save state of app to sqlite database: `amity.sqlite` . (optional) save to custom `sqlite_db` name
    
* `load_state <sqlite_database>`

    Loads application state from the specified database into 
    the application. default loads `amity.sqlite`
    
    Below is a sample session:
    
    	(amity) load_state
		Successfully loaded state from amity.sqlite

* `quit`

    This exits the application.
    
## Demo Video

[![asciicast](https://asciinema.org/a/96755.png)](https://asciinema.org/a/96755)