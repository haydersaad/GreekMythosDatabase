# GreekMythosDatabase
A SQL database containing the characters and relationships in Greek Mythos. Simple web API to view and edit database also included.

Database based on the following ERD:
![alt text](https://github.com/haydersaad/GreekMythosDatabase/blob/main/web_api.py)


My entities contain immortals such as gods, deities and titans as well as mortals, which include Greek kings, heroes and women.
Further entities include locations of characters in the world, their powers, and their pets.
Relationships include parent-child, master-slave, pet-owner, murderer-victim, etc. There are also a few relationships
that are shared between entities, for example, location is for a hero as well as for a god.

Some relationips are many-to-many, for example, one woman may be affiliated with multiple kings and/or heroes, and some
relationships are one-to-many/many-to-one, for example, every titan had one god as their murderer.
Some relationships involve total participation, for example, every god must have atleast one or more powers.
