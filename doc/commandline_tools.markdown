
# How to build batch processing commandline Tools

This guide explains how to write commandline tools for processing data in a repeated, batch oriented fashion.
An example would be reading new entries from a database table, sending them out as messages and marking the 
database rows as `processed`.

Tools should follow the [crash early, crash often][crasearly] design principle.

[crashearly]: http://blogs.23.nu/c0re/offensive-programming-crash-early-crash-often/


## Robustness

The tool should be alble to be innerupted anywhere during processing without generation data which needs
manual intervention.

Messages should be identified by a an unique id. For incomming Messages the tool should detect
and suppress duplicate IDs if the tool uses persistent storage. If not, it may process
duplicate IDs without special consideration.

The tool may generate duplicate messages, but *must never never loose messages*. The typical pattern to
archive this is

    01: inmessage = source.read_message()
    02: outmessage = process_message(inmessage)
    03: write_journal(inmessage) # see below
    04: destination.write(outmessage)
    05: write_debug_info(outmessage) # see below
    06: source.mark_done(inmessage)

This pattern works with databases (e.g. DB2), Messaging Systems (e.g. RabbitMQ) and the file system
(e.g. [Maildir][maildir]). It should limint message los to hardware failures and very servere software
failures.

[maildir]: http://www.qmail.org/qmail-manual-html/man5/maildir.html

Observe that [py-amqplib][amqplib], the library we use for sending messages to RabbitMQ *does not always
report errors during writing messages* but only on the *next* queue operation.You can mitigate this
problem by sending a message during `write_debug_info()` which will throw an expection if an error during
`destination.write(outmessage)` occures. That ensures `source.mark_done(inmessage)` is only called on
successful transmission of the message to the destination.

[amqplib]: http://code.google.com/p/py-amqplib/


## Logging

We want to keep logs for error diagnosis and restore operations after an failure. For the restore operations
tools that change state in the system should generate a logfile/journal which could be used to exactly
recreate the steps the tool took. This is similar to a filesystem [journal][journal] or a database [redo
log][redolog]/[Binary Log][binlog]. In most instances this can be each input message processed by the tool.

[journal]: http://en.wikipedia.org/wiki/Journaling_file_system
[redolog]: http://en.wikipedia.org/wiki/Redo_log
[binlog]: http://dev.mysql.com/doc/refman/5.1/en/binary-log.html

### Journaling

Best practice is to save JSON encoded, [NetStrings][netstringio] framed messages. Example code looks like
this:

    logdata = json.dumps(doc, sort_keys=True, separators=(',',':'))
    nstring = NetStringIO.NetStringIO(open(options.log, 'a'))
    nstring.write(logdata)
    nstring.file.close()

Observe that this message is not totally save, especially for messages bigger than the FS-buffer or Page
size. Concurrent access to the log file can lead to mixed records in the file. Usually this risk can be
accepted since there sould be only a single instance of the tool running on a host. If this is differently
for your tool you might want to use a different logfile for each running instance.

### Diagnostic Logging

Diagnostic logging should happen to [stdout][stdout]. We assume that framework like [supervise][daemontools]
or [Monit][monit] capture the output if not running interactively. If not in debugging mode output should be
relatively terse and not more than one line per message processed.

[stdout]: http://en.wikipedia.org/wiki/Standard_streams#Standard_output_.28stdout.29

The tool should always give a startup message and if possible an exit message.


## Commandline

Most tools should come with at least the following a set of options:

* `--log` where to write the logfile to. This logfile should have the character of a [journal][journal]
  or [redo log][redolog]. Typically containing all messages processed encoded as [NetStrings][netstringio].
  The log should contian no startup and housekeeping messages.
* `--continuous` never exit but run continously. Typically used in conjunction with [supervise][daemontools]
  or [Monit][monit]. Does *not* fork into background. We assume that stdout is logged somewhere.
* `--sleep` this many seconts between processing attempts when running `--continuous`. Should be a prime
  number. "53" might be a good default value.
* `--quiet` generate no output expect when an error occurs. Mainly for use in cron jobs.
* `--debug` generate excessive output making only sense to coders.
* `--dry-run` actually don't change anything
* `--maxnum` don't process more than maxnum messages and exit after that many messages have been processed.
  Helpful for development.

[netstringio]: http://github.com/hudora/huTools/blob/master/huTools/NetStringIO.py
[daemontools]: http://cr.yp.to/daemontools.html
[monit]: http://mmonit.com/monit/

Positional parameters should be avaoided unless their meaning is very obvious.

Example code might look like this:

    parser = optparse.OptionParser()
    parser.description = ('Uebernimmt Umlagerungsauftraege aus der Soft-Schnittstelle ISK00 und '
                         + 'erzeugt Warenzugangsmeldungen')
    parser.set_usage('usage: %prog [options]')
    parser.add_option('--log', default='/var/log/ic2wms_einlagerungen.log',
                      help='Wo sollen die Nachrichten protokolliert werden? [%default]')
    parser.add_option('--continuous', action='store_true',
                      help='Run continuously forever')
    parser.add_option('--sleep', type="int", default=47,
                      help='Pause zwischen Durchlaeufen, wenn --continuous verwendet wird [%default s]')
    parser.add_option('--quiet', action='store_true', help='UEbliche Ausgaben unterdruecken')
    parser.add_option('--debug', action='store_true', help='Debugging Informationen ausgeben')
    parser.add_option('--dry-run', action='store_true', help='Keine Nachrichten absenden und loeschen')
    parser.add_option('--maxnum', type='int',
                      help='Maximale Anzahl der zu transferierenden Datensaetze [default: unlimited]')
    
    options, args = parser.parse_args()
    if args:
        parser.error("incorrect number of arguments")
