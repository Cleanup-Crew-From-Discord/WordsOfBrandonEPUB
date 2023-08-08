# Words of Brandon - EPUB Edition

*"Cleanup-Crew-From-Discord, Amateur Programmer, wore white on the day he was to code an abomination"*

On a day of somewhat below average intelligence, I decided that I wanted the entirety of the Words of Brandon on my old Kindle to read whenever I pleased.

This is honestly kind of pointless, given the constantly updating nature of WoB, but I wanted to give it a shot anyways.

And so, I wrote ***this*** mashup of bash and python.

In order, it
* wgets each page of Q&A sessions
* from each page, gets links for each session and places them all in one link file
* checks if there are no new links from last time it was ran, exits if there aren't
* cleans out the old files
* wgets every single link in the link file to html, and removes some problematic characters and tags
* reads the html and extracts the needed info (event name and date, questions asked by questioners, question spacing) to a smaller, more streamlined HTML file
* sorts each html file by date
* generates table of contents page, table of contents file, and contents.opf file
* Wraps all files into an ebook stamped with the current date

## Getting Started

Installing and running yourself is completely unnecessary* if you just want the storming ebook, check the releases tab for that!

<sup><sub>*not yet, I don't have auto updates working yet</sub></sup>

### Prerequisites 

* Linux distribution with python3
    * currently no support for Windows, but you can always just grab the latest ebook or run WSL.
    * support will come eventually in the form of a fully Python codebase, but this is pretty low priority
* 100MB or so of disk space (will go DOWN as optimization improves)
* Functional RAM and CPU
* Internet (duh)

### Installation

* clone repo
* cd into created folder

tada!

## Usage

* `./fullScrape.sh` let it run and it will spit out an ebook
* `./useOldData.sh` recreate ebook from existing data
* `./fullScrapeSAFE.sh` quits if no new Q&A's have been posted. Ideal for automation purposes

Cover art is located in `outBook/OEBPS/cover.jpg`, feel free to change it
## Roadmap

- [WIP] Cleanup codebase
    - [ ] Remove all bash
    - [ ] Make directory structure less chaotic
    - [ ] Merge py files 
- [ ] Add insert pages for the release of each work, to provide a "stopping point" for spoilers
- [ ] Make a better looking default cover
- [ ] Choose a license

## Contributing

As much as I love FOSS, this is currently a learning project just for me.

Once I get the code to a state I can be somewhat proud of, I may open it up for others to contribute to.

For now, though, I'm still getting my footing with Github and I'd like to go it alone with this project.

## Everything else

I am not affiliated with Brandon Sanderson or anyone at wob.coppermind.net. I am merely a crazy monkey with some knowledge of scraping

No license yet, I need to read up on them more