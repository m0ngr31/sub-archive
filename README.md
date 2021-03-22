# Sub Archive

## What this is
This project is meant to be a simple way to view submissions and comments from subreddits that have been removed for one reason or another, or as a way to have a mirror of an active subreddit. I made this to view a few subreddits that got banned for various reasons.

## What this isn't
A way for someone to resurrect "hate" subreddits. You know who you are. Having said that, not every removed sub was hateful or violent. Reddit admins have banned plenty of subreddits (and it is their right to do so) and will continue to do so.


# Setup

Before you can run the server, you need to make a backup of a subreddit you want with [Timesearch](https://github.com/voussoir/timesearch).

## Timesearch
After you've followed the instructions to get Timesearch running, you can run these commands to create an archive:

```bash
python timesearch.py get_submissions -r your_sub_here
python timesearch.py get_comments -r your_sub_here
```

Repeat the above step for each subreddit you would like to backup.

This will create a different SQLite database file for each subreddit. Let's merge them together into one:
```bash
mkdir dbs
# copy the first one into a new folder
cp subreddits/your_sub_here/your_sub_here.db dbs/archive.db
# Run this command for each of the other subreddits you've archived
python timesearch.py merge_db --from subreddits/your_sub_here2/your_sub_here2.db --to dbs/archive.db
```

Now you have the archive the server needs to work.

# Running
The simpliest way to get this working is by using Docker and mapping the `/app/db` folder to the directory where your archive lives.

# TODO
* Create favicon
* Show dates on comments/submissions
* Enable search functionality
* Add to DockerHub
* Nicer styling for subreddits/comments
* Have user profile pages
