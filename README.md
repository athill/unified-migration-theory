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