unified-migration-theory
========================

Dependencies
------------
[Python](http://www.python.org/)
[Paramiko](http://www.lag.net/paramiko/)


Summary
-------
The basic idea is to define and execute a migration from one instance of a website to another. For example from your test server to your production server. The current version assumes using sftp, but copying locally would not be hard to add.

So here's the deal:

<pre>
- bin
	- migrate.py: does the work
- sites
	- [site-id]: associates a local site with a remote site
		- properties.json: configuration file
		- migrations
			[migration-id]:
				def.txt: Defines a migration. It's based on the output of 
					<code>git diff --name-status [commit]</code>, I'll get into that.
				backup/: will be generated based on the files and directoies you want to delete or modify
			...
</pre>

A lot of error checking needs to be added, but you basically call

<code>
python bin/migrate.py [site-id] [migration-id]
</code>

and assuming 

* ~/sites/[site-id]/migrations/[migration-id] exists
* as does ~/sites/[site-id]/properties.json
* as does ~/sites/[site-id]/migrations/[migration-id]/def.txt


### ~/sites/[site-id]/properties.json:

<pre>
{
        "host": "example.com",
        "port": 22,
        "password": "password, if ommitted, you will be prompted (once I implement it). Looking into key-based auth",
        "username": "username, may integrate into host. e.g., username@example.com",
        "remoteroot": "/full/path/to/remote/webroot",
        "localroot":  "/full/path/to/local/webroot"
}

### ~/sites/[site-id]/migrations/[migration-id]/def.txt
<pre>
A  file/to/add.ext
D  file/to/delete.ext
M  file/to/modify.ext
</pre>


