# Project SwaRail

The theme of this project is Automatic Traffic Control (Both Centralized and Decentralized).


## How security is handled in this project

The key focus of security in this project is on all the lives of people that travel in trains everyday. To make sure this system runs without any security vulnerabilities, we use the following protocols.


### Security of Human Beings

To make sure that our travellers are safe, following guards are present in this project

- Guard of Invisibility : It removes the occupied and booked track circuits from graph itself, so that next algorithm can't even progress to that path knowing that there is no track ahead

- Guard of Authority : Even few minutes checks that there isn't any changes that are unauthorized in a section

- Guard of Booking : Once booked, a booking cannot be undone become a train traverses a track and thus its signals and crossovers also can be touched

- Guard of Emergency : If station master (or computer) deems a particular situation as an emergency situation, the guard of Emergency makes sure that 


### Security for our servers

There is no need to worry for the security of our centralized server since they only share us info related to schedule of an entering train and we share them current location of the train which are both not an internal stuff.


## Additional problems of Indian Railways which can be solved using this project

- Automatic Trains : We can now truly make Automatic Trains (which directly communicate with these systems instead of detecting signals on the track) (these trains can use AI to detect if there is any further obstruct or not ... but AI cannot be trusted to detect track signals on a running train)

- Real-Time Location Detection : We can now establish actual Real-Time Train location system that is very accurate. Accurate up to track circuits level. The important thing is there is nothing we have to do much for this, its automatically done with this project. With just 2-3 extra lines of code, we can send the real-time location of a train to central authority/server.

- Real-Time Future Details : With this software, we can even tell very very accurately that which path the train has taken, how much distance is remaining to reach next station and which platform it will be comming on, and how much is the ETA of a train on this path

- Non Auto-Pilot : This software can also be run without "Auto-Pilot" mode. This project is based on commands, so in "Auto-Pilot" mode, the computer itself trigger those commands and without this mode, Station master can manually put commands if required.

- Speed of Trains : we can now focus on increase speed of our existing trains and software will make sure they can get the most out of their high speeds by maximizing horizontal movements.


## How does booking takes places of trains based on priority within a section?

Trains which satisfy the following conditions are giving priority in booking :-

- Trains whose delay in reaching the current station was high (A) (It should be high)
- Trains whose time remaining for departure is very low (B) (It should be low)
- The amount of time it was standing without any booking even after its hault time is over (C) (It should be high)
- The highest priority will be giving to those trains which are standing at some outer and no at stations, this is a mesure to makes sure there is no deadlock within the tracks (D = some very high value)
(D = 0 if its not standing on outer)

We use priority queue in which each trains priority depends on (A - B + C + D). That is A-B should be as high as possible to get the train highest priority in booking tracks


## How does the platform for next station is choosen? (Since this is NP-Hard problem ~ similar to TSP)

The next platform to reach is decided based on following conditions :-

- The next platform within a station should not be occupied or booked till now
- The next platform should be the least used one till now, to avoid trains using platforms that are on main line
- It should have enough length to accomodate train, if none of the platforms are long enough, then choose the one which can maximumly accomodate it , i.e., the platform with maximum track circuit length

## Algorithm to choose a route going through all the stations (double-directed satisfaction)

- find connectivity between all platforms using repetitive BFS over all platforms to all other platforms and find which platform is connected to which other platform in both directions
- then lets say you have to go from Source to target or set of targets through some stations ( Source --> Station_1 --> Station_2 --> ....... --> Station_n --> {target} )
- start from target or set of targets ({target}) and in a reverse order keep finding connectivity of target to station_n platforms and from those platforms to station_(n-1) platforms and so on upto set of source platforms
- this will given a subgraph of original graph with connection between set of targets and set of source
- repeat the process with the single source we have towards the direction of target (i.e., now in reverse direction from previous search)
- this will again filter our subgraph to a sub-subgraph where we have connectivity from single source to one or more targets
- now follow this subgraph by finding shortest path from station to station and thus the route is formed.


## How does route of a train is booked?

Route of a train is booked based on following conditions :-

- For train to not stop, or reduce its speed on track, the route is booked in such a way that the train traverses maximum of horizontal length, i.e., minimize the use of crossovers as much as possible.

- Although horizontal movement is highly prioritize, we will still keep the distance of the route as metric if required to minimize distance as well.

- The route should not contain any track circuit which is occupied or booked

- There will be no hault better two stations or within a section (or in booking), since within a section there isn't too much long tracks that we should opt for haults in between, even if required, we can later on modify the algorithm to generate "tracks" from track circuits. Tracks will combine all track circuits which are ONLY connected to each other in a single lane manner and does not contain any crossovers. Later on which booking paths, we can make sure that trains stop in between only on tracks which have length >= train length and can then re-new their booking for further journey.