SimpleFileDrop
==============
SimpleFileDrop is a lightweight Docker container that lets you easily host some
files on your server.

For example, you can store your `.bashrc`, `.vimrc`, and `.emacs` files on your
server, so that you always have instant access to them. Plus, no need to deal
with FTP or SCP: simply configure SimpleFileDrop with Dropbox or Google Drive
and sync when you need to.

Setup
-----
First, create a ZIP file containing the files you want hosted, then:

- If you're using Dropbox, place it in your Public directory and get the direct
  link to it, or
- If you're using Google Drive, place it wherever, change the sharing settings
  to allow viewing by anyone with the URL, and get the link that's used when you
  "download" the file.

Now, you can run it. The image is stored in the public registry and should get
automatically pulled.

    docker run -d -e "APP_ARCHIVE_URL=https://dropb..." olegv/simplefiledrop

If you want, you can also set a few other environment variables: `APP_PORT`,
`APP_STORE_PATH` (where your files are stored; `/var/www` by default), and
`APP_RELOAD_PATH` (the special URL that causes SimpleFileDrop to update based on
your archive).

Usage
-----
When the server first starts, there's nothing in the `/var/www` directory. You
need to trigger an update, so simply visit the `/reload_now` page to update the
file drop.

Whenever you need to update your server, simply update the archive on your
Dropbox or Google Drive folder, and revisit the reload URL!
