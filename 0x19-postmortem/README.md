# Postmortem

During the project 19 of the ALX System Engineering & DevOps, at 18:00 GMT in Ghana, there was an outage on an isolated Ubuntu 14.04 container running an Apache web server. Several GET requests on the server resulted in a 500 Internal Server Error. The response was expected to be an HTML file defining a simple Holberton WordPress site.

## Debugging Process
The issue was discovered by a brilliant team member, Amoaful upon opening the project around 18:20 GMT. Amoaful, my other self, is a skilled debugger proceeded immediately to solving the problem.

- First, he checked the running processes using the `ps aux` command. He discovered the ` root ` and the ` www-data ` of the `apache2` processes were properly running.
- Next, he examined the `sites-available` directory of the `/etc/apache2/` and determined the web server was serving contents from the `/var/www/html/`.
- In one terminal, he initiated a `strace` process on the PID of the Apache `root`. In a second terminal, he initiated requests to the server using the `curl` command. The `strace` gave no useful information.
- Amoaful repeated the step 3 on the PID of the `www-data` process. The `strace` revelead an `-1 ENOENT (No such file or directory)` error when attempting to access the file `/var/www/html/wp-includes/class-wp-locale.phpp`.
- With an undivided attention, he walked through the `/var/www/html/` directory, one file at a time, using Vim pattern matching to identify the erroneous `.phpp` file extension. Surprisingly, he found the offending bug in the `wp-settings.php` file on line 137, `require_once( ABSPATH . WPINC . '/class-wp-locale.php' );`.
- With a deep breath, he deleted the trailing `p` from the line.
- He executed another `curl` command on the server which produced a 200 A-ok response!
- To automate such debugging process in the future, he wrote a Puppet manifest to fix the error.

In summary, the error in the `wp-settings.php` of the WordPress app caused the loading of the `class-wp-locale.phpp` to crash. This file, contained in the `wp-content` was supposed to be `class-wp-locale.php.` The whole adventure was to remove the trailing `p` to fix the issue.

## Prevention
- Testing, as was discovered after a lengthy discussion would have blacklisted the error early in the development stage. It is therefore crucial to test as much as the development goes on to remedy any unforseen situations.

- Utilizing status monitoring. It is important to enable some uptime-monitoring services such as the [UptimeRobot](https://uptimerobot.com/) to alert any outage of the website.