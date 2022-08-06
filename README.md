# Export Apple Podcasts to hierarchical OPML

Uses Podcasts database from `~/Library/Group Containers/*.groups.com.apple.podcasts/Documents/MTLibrary.sqlite` and export to OPML with varios options for hierarchy.

## Use it in the command line
```shell
python3 -m macOS_podcasts -g station --target $HOME --prefix my-podcasts
```

Or simply:

```shell
python3 -m macOS_podcasts
```

## Extended help

```
usage: macOS_podcasts [-h] [--db PODCASTS_DB] [-g GROUP] [--trees | --no-trees] [--target TARGET] [--prefix PREFIX]

Export macOS Podcasts to OPML

optional arguments:
  -h, --help            show this help message and exit
  --db PODCASTS_DB      Path to Podcasts app database.
  -g GROUP, --group GROUP
                        Group podcasts in the outline by station, author or apple_category. Defaults to apple_category.
  --trees, --no-trees   Export to one hierarchical file (default), or to one file per group. (default: False)
  --target TARGET       Target folder for exported OPML files. Default is current folder.
  --prefix PREFIX       File name prefix for each OPML file. Default is «macOS-Podcasts»
```

## Sample OPML
Exported OPML will group your podcasts by `station`, `author` or `apple_category`. Here is an example grouped by `station`:

```xml
<?xml version='1.0' encoding='utf-8'?>
<opml version="1.0">
	<head>
		<title>macOS Podcasts</title>
	</head>
	<body>
		<outline type="group" text="macOS Podcasts: station is News">
			<outline type="rss" text="The Daily" xmlUrl="http://rss.art19.com/the-daily" htmlUrl="https://www.nytimes.com/the-daily"/>
			<outline type="rss" text="The Intelligence from The Economist" xmlUrl="https://rss.acast.com/theintelligencepodcast" htmlUrl="https://theintelligence.economist.com"/>
			<outline type="rss" text="Today in Focus" xmlUrl="https://www.theguardian.com/news/series/todayinfocus/podcast.xml" htmlUrl="https://www.theguardian.com/news/series/todayinfocus"/>
		</outline>
		<outline type="group" text="macOS Podcasts: station is Music">
			<outline type="rss" text="Caipirinha Appreciation Society" xmlUrl="http://cas.podomatic.com/rss2.xml" htmlUrl="https://www.podomatic.com/podcasts/cas"/>
			<outline type="rss" text="Brasil Abstrato" xmlUrl="https://abstra.to/feed/" htmlUrl="https://abstra.to"/>
		</outline>
	</body>
</opml>
```

Use `--trees` to export multiple OPML files, one per group.

# About
Hacked and created by [Avi Alkalay](https://linkedin.com/in/avibrazil), Data Scientist

Project page: [github:avibrazil/macOS-podcasts-export](https://github.com/avibrazil/macOS-podcasts-export)