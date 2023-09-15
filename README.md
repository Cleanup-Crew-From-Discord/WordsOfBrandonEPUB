# Words of Brandon - EPUB Edition - TESTING BRANCH

## Code in this branch likely doesn't work

*"Cleanup-Crew-From-Discord, Amateur Programmer, wore white on the day he was to code an abomination"*

On a day of somewhat below average intelligence, I decided that I wanted the entirety of the Words of Brandon on my old Kindle to read whenever I pleased.

This is honestly kind of pointless, given the constantly updating nature of WoB, but I wanted to give it a shot anyways.

And so, I wrote ***this***.

In order, it
* scrapes each page of Q&A sessions
* from each page, extracts links for each Q&A session and places them all in one link file
* checks if there are no new links from last time it was ran, exits if there aren't
* cleans out the old files
* scrapes the HTML every single link in the link file, reads the HTML, and extracts the needed info (event name and date, questions asked by questioners, question spacing) to a smaller, more streamlined HTML file (a page file)
* sorts each page file by date
* generates table of contents page, table of contents file, and contents.opf file
* Wraps all files into an ebook stamped with the current date

## Getting Started

Installing and running yourself is completely unnecessary* if you just want the storming ebook, check the releases tab for that!

<sup><sub>*not yet, I don't have auto updates working yet</sub></sup>

### Prerequisites 

* Python3
     * urllib3 module (`python3 -m pip install urllib3`)
* 100MB of disk space (uses way less than this, ~5MB by default, but with --full and the passage of time that may change)
* Functional RAM and CPU
* Internet (duh)

### Installation

* clone repo
* cd into created folder
* run the python file 

tada!

## Usage

* run the file to get the most recent annotations, and re-zip without ripping if no new ones have been found
* launch args:
  * --force: re download all files no matter what
  * --full: save every WoB page, not just annotations. Saves under a different file name
  * --use-old-files: rezip from already grabbed files, don't check for new ones
  * --use-old-links: reuse old links file without checking for new links
  * --crash-on-no-new-links: exit out with error code if no new links are detected (for automation)
  * --quiet: no print statements

Cover art is located in `outBook/OEBPS/cover.jpg`, feel free to change it
## Roadmap

- [X] Cleanup codebase
    - [X] Remove all bash
    - [X] Make directory structure less chaotic
    - [X] Merge py files 
- [X] Add different launch arguments
- ~~[ ] Add insert pages for the release of each work, to provide a "stopping point" for spoilers~~
    - [X] Instead, allow and remove pages based on the associated tags
- [ ] Possibly improve the formatting of the book / table of contents
- [ ] Make a better looking default cover
- [ ] Choose a license

## Contributing

As much as I love FOSS, this is currently a learning project just for me.

Once I get the code to a state I can be somewhat proud of, I may open it up for others to contribute to.

For now, though, I'm still getting my footing with Github and I'd like to go it alone with this project.

## Everything else

I am not affiliated with Brandon Sanderson or anyone at wob.coppermind.net. I am merely a crazy monkey with some knowledge of scraping

No license yet, I need to read up on them more
