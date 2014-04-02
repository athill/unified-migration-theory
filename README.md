unified-migration-theory
========================

Status
------
Ran into issues with this and postponed it, but am working on it. Long way to go. I've created [DirStructures](https://github.com/athill/DirFixtures) to aid in testing and it seems to actually work. The next step is [Migrater](https://github.com/athill/unified-migration-theory/blob/migrater/README.migrater.md), which will add/copy/delete the files, abstracting out the differences of whether the target is accessed locally or via ftp, sftp, etc. I'll publish that as soon as local migrations are working, at the very least (I think I'm close).

UMT is meant to be an abstration over Migrater. I may rethink the command line interface and required directory structure below. Hopefully get Migrater posted soon, as it's the real engine.

Dependencies
------------
[Python](http://www.python.org/)
[Paramiko](http://www.lag.net/paramiko/)


Summary
-------
Goal: To create a system to easily define a migration from one instance of a project to another. For example, moving from a test environment to a production environment. Additionally, to allow easy recovery from a given migration, to support various methods of migration (local, sftp, ftp, etc.), and to allow output from versioning system reports (currently, git), but extend it to allow shortcuts for hand-written files or additional directives to those generated.

Background
----------
This started with a script I wrote in [Apach Ant](http://ant.apache.org/). 

The script has a "migration" parameter that indicates the name of a directory (folder) in a pre-defined "migrations" directory.

The appropriately named folder in the migrations directory contains four files:
- includes.txt - These are ant-based patterns to include 
- excludes.txt - ibid, but exclude
- properties  - where you're copying from, where you're copying to, etc.
- README.txt  - Purpose of migration and anything not covered by the script (e.g. database updates)

So you set up your properties and your includes, run the ant script and boom: requested files are backed up from 'production', files from 'test' replace or are added to 'production', and then the backups and definition are archived for future reference.


that takes a migration definition based on 
The basic idea is to define and execute a migration from one instance of a website to another. For example from your test server to your production server. The current version assumes using sftp, but copying locally would not be hard to add.

	So here's the deal:

	- bin
		- migrate.py: does the work
	- sites
		- [site-id]: associates a local site with a remote site
			- properties.json: configuration file
			- migrations
				[migration-id]
					def.txt: Defines a migration. It's based on the output of 
						<code>git diff --name-status [commit]</code>, I'll get into that.
					backup/: will be generated based on the files and directoies you want to delete or modify
				...
		...

A lot of error checking needs to be added, but you basically call

	python bin/migrate.py [site-id] [migration-id]

and assuming 

* ~/sites/[site-id]/migrations/[migration-id] exists
* as does ~/sites/[site-id]/properties.json
* as does ~/sites/[site-id]/migrations/[migration-id]/def.txt


### ~/sites/[site-id]/properties.json:

	{
	        "host": "example.com",
	        "port": (optional, default: 22),
	        "password": "password, if ommitted, you will be prompted (once I implement it). Looking into key-based auth",
	        "username": "username, may integrate into host. e.g., username@example.com",
	        "remoteroot": "/full/path/to/remote/webroot",
	        "localroot":  "/full/path/to/local/webroot"
	}


### ~/sites/[site-id]/migrations/[migration-id]/def.txt

	A  file/to/add.ext
	D  file/to/delete.ext
	M  file/to/modify.ext
	...

This can be achieved in Git, for example, by 

	git diff --name-status HEAD^ HEAD

To retreive the list of changes (input for def.txt) in the correct format. `--name-status` provides the accepted format, `HEAD^` pulls all changes in the last commit. See [git-diff(1)](https://www.kernel.org/pub/software/scm/git/docs/git-diff.html)

