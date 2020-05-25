#########################
Automatic Tarsnap Backups
#########################

Quick & dirty package to maintain a rolling set of `Tarsnap`_ backups.
Tested on Python 3.7 & 3.8.

.. _Tarsnap: https://www.tarsnap.com/

Installation
============

For the author's (macOS 10.15) system.
We're going to:

- Use the system Python;
- Install into a virtualenv;
- Run from launchd.

We'll start by setting up the virtualenv::

   $ /usr/bin/python3 -m venv ~/sw/venv/jdsnap
   $ . ~/sw/venv/jdsnap/bin/activate

Now install jdsnap into the new environment.
Note that it's pulling in its dependencies::

   $ python setup.py install

At this point, it should be possible to run jdsnap *without* setting up the virtualenv::

   $ ~/sw/venv/jdsnap/bin/jdsnap  # ... and away we go.

And so at this point we can drop the following into ``~/Library/LaunchAgentes/org.jdswinbank.jdsnap``::

   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>ProgramArguments</key>
       <array>
           <string>/Users/jds/sw/venv/jdsnap/bin/jdsnap</strong>
           <string>--tarsnap</string>
           <string>/opt/local/bin/tarsnap</string>
           <string>--config</string>
           <string>/Users/jds/.jdsnap.json</string>
       </array>
       <key>Label</key>
       <string>org.swinbank.jdsnap</string>
       <key>KeepAlive</key>
       <false/>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Minute</key>
           <integer>0</integer>
           <key>Hour</key>
           <integer>11</integer>
       </dict>
       <key>StandardOutPath</key>
       <string>/Users/jds/sw/log/jdsnap.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/jds/sw/log/jdsnap.err</string>
   </dict>
   </plist>
